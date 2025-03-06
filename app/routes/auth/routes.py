from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User
from app.routes.auth import auth_bp
from app.routes.auth.forms import LoginForm, RegistrationForm, SettingsForm
import datetime

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


@auth_bp.route('/settings', methods=['GET', 'POST'])
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