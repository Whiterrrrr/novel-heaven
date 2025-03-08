from flask import render_template, redirect, url_for, flash, jsonify, request, session
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf.csrf import validate_csrf
from werkzeug.exceptions import BadRequest

from app import db
from app.models import User
from app.routes.auth import auth_bp
from app.routes.auth.forms import LoginForm, RegistrationForm, SettingsForm
from datetime import datetime


def admin_required(fn):
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            return jsonify(msg="Admins only!"), 403
        return fn(*args, **kwargs)
    return wrapper

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.last_seen = datetime.utcnow()
            db.session.commit()
            
            # Daily login reward
            if user.last_reward.date() < datetime.utcnow().date():
                user.balance += 10
                user.last_reward = datetime.utcnow()
                db.session.commit()
                flash('获得每日登录奖励10金币！', 'success')
            
            return redirect(url_for('main.dashboard'))
        flash('无效的用户名或密码', 'danger')
    return render_template('auth/login.html', title='登录', form=form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # 如果是 POST 请求，验证 CSRF Token
    if request.method == 'POST':
        try:
            validate_csrf(request.form.get('csrf_token'))
        except BadRequest:
            return jsonify({"code": 400, "msg": "无效的 CSRF Token"}), 400

    # 执行退出
    logout_user()
    session.clear()  # 清除所有会话数据

    # 根据请求类型返回响应
    if request.accept_mimetypes.accept_json:
        return jsonify({"code": 200, "msg": "已退出登录"})
    else:
        return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='注册', form=form)


@auth_bp.route('/settings', methods=['GET', 'PUT'])
@login_required  # 确保用户已登录
def settings():
    form = SettingsForm(obj=current_user)  # 用当前用户数据填充表单

    if form.validate_on_submit():
        if User.query.filter(User.username == form.username.data, User.id != current_user.id).first():
            flash('Username already taken!', 'danger')
            return redirect(url_for('auth.settings'))

        if User.query.filter(User.email == form.email.data, User.id != current_user.id).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('auth.settings'))

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data

        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.commit()
        flash('Settings updated!', 'success')
        return redirect(url_for('auth.settings'))

    return render_template('auth/settings.html', form=form)

# 修改用户角色（管理员专用）
@auth_bp.route('/api/user/roles/<int:user_id>', methods=['PUT'])
@admin_required
def update_role(user_id):
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify(msg="User not found"), 404
    target_user.role = request.json.get('role')
    db.session.commit()
    return jsonify(msg="Role updated")

# 删除用户（管理员专用）
@auth_bp.route('/api/user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify(msg="User not found"), 404
    db.session.delete(target_user)
    db.session.commit()
    return jsonify(msg="User deleted"), 200