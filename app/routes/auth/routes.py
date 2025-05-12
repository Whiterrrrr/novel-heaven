from flask import render_template, redirect, url_for, flash, jsonify, request, session
from flask_login import logout_user, current_user, login_required, login_user
from flask_wtf.csrf import validate_csrf
from werkzeug.exceptions import BadRequest
from app import write_log
from app.models import *
from app.routes.auth import auth_bp
from app.routes.auth.forms import LoginForm, RegistrationForm, SettingsForm
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            return jsonify(msg="Admins only!"), 403
        return fn(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    #if current_user.is_authenticated:
        #return jsonify({"message": "Already logged in"}), 400
    
    form = LoginForm()
    print("call login", form.email.data, form.password.data)
    if True or form.validate_on_submit():
        print("form validated")
        success, user, message = DBOperations.authenticate_user(
            email=form.email.data,
            password=form.password.data,
            # remember=form.remember_me.data
        )
        
        if success:
            login_user(user)
            reward_given, amount = DBOperations.check_and_reward_daily_login(user)
            if reward_given:
                flash(f'获得每日登录奖励{amount}金币！', 'success')

            return jsonify({
                "token": user.balance,
                "user": {
                    "id": user.id,
                    "name": user.username,
                    "email": user.email
                }
            }), 200
        
        flash(message, 'danger')
    else:
        print("验证失败原因:", form.errors)

    return jsonify({"message": "Invalid email or password"}), 401


"""
import uuid

@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in"}), 400
    
    form = LoginForm()
    if True or form.validate_on_submit():
        success, user, message = DBOperations.authenticate_user(
            email=form.email.data,
            password=form.password.data,
        )
        if success:
            reward_given, amount = DBOperations.check_and_reward_daily_login(user)
            if reward_given:
                flash(f'获得每日登录奖励{amount}金币！', 'success')
                
            token = str(uuid.uuid4())
            user.token = token  # 你需要在 User 表里加一个 token 字段
            print(user.token)
            db.session.commit()

            return jsonify({
                "token": token,
                "balance": user.balance,
                "user": {
                    "id": user.id,
                    "name": user.username,
                    "email": user.email
                }
            }), 200
        else:
            return jsonify({"message": message}), 401
"""       


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
    print("call register", form.username.data, form.email.data, form.password.data)
    if True or form.validate_on_submit():
        print("form validated")
        success, user, message = DBOperations.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        
        if success:
            flash(message, 'success')
            return jsonify({
                "token": user.id,
                "user": {
                    "password": form.password.data,
                    "username": user.username,
                    "email": user.email
                }
            }), 200
        else:
            flash(message, 'danger')

    else:
        print("验证失败原因:", form.errors)
    return jsonify({"message": "registration failed"}), 401


@auth_bp.route('/settings', methods=['GET', 'PUT'])
@login_required
def settings():
    form = SettingsForm(obj=current_user)

    if form.validate_on_submit():
        update_data = {
            'username': form.username.data,
            'email': form.email.data,
            'bio': form.bio.data
        }
        
        if form.password.data:
            update_data['password'] = form.password.data

        success, message = DBOperations.update_user_settings(
            user_id=current_user.id,
            update_data=update_data
        )

        if success:
            flash(message, 'success')
        else:
            flash(message, 'danger')
        
        return redirect(url_for('auth.settings'))

    return render_template('auth/settings.html', form=form)

# 修改用户角色（管理员专用）
@auth_bp.route('/api/user/roles/<int:user_id>', methods=['PUT'])
@admin_required
def update_role(user_id):
    success, message, status_code = DBOperations.update_user_role(
        user_id=user_id,
        new_role=request.json.get('role')
    )
    return jsonify(msg=message), status_code

# 删除用户（管理员专用）
@auth_bp.route('/api/user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    success, message, status_code = DBOperations.delete_user(user_id)
    return jsonify(msg=message), status_code