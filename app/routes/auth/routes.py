from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User
from app.routes.auth import auth_bp
from app.routes.auth.forms import LoginForm, RegistrationForm
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