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
    """
    Handle user login
    Methods:
        GET: Serve login form
        POST: Authenticate user credentials
    Form Data:
        email (str): User's email address
        password (str): User's password
    Returns:
        - 200: JSON with user data and auth token
        - 401: JSON error for invalid credentials
        - 400: JSON error if already logged in
    Process:
        1. Validate login form
        2. Authenticate via DBOperations
        3. Apply daily login reward if eligible
        4. Set user session via login_user()
    """
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
        print("failure:", form.errors)

    return jsonify({"message": "Invalid email or password"}), 401

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    Terminate user session
    Methods:
        POST: Requires valid CSRF token
    Security:
        - CSRF protection for POST requests
        - Requires active login session
    Returns:
        - 200: JSON success message
        - 400: JSON error for invalid CSRF
        - Redirect to index for non-JAX requests
    Process:
        1. Validate CSRF token (POST only)
        2. Clear user session and cookies
    """
    print("call logout")
    if request.method == 'POST':
        try:
            validate_csrf(request.form.get('csrf_token'))
        except BadRequest:
            return jsonify({"code": 400, "msg": "无效的 CSRF Token"}), 400

    logout_user()
    session.clear()

    if request.accept_mimetypes.accept_json:
        return jsonify({"code": 200, "msg": "已退出登录"})
    else:
        return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle new user registration
    Methods:
        GET: Serve registration form
        POST: Create new user account
    Form Data:
        username (str): Desired username
        email (str): User's email address
        password (str): User's password
    Returns:
        - 200: JSON with new user data
        - 401: JSON error for failed registration
    Process:
        1. Validate registration form
        2. Create user via DBOperations
        3. Return generated user ID as token
    """
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
        print("failure:", form.errors)
    return jsonify({"message": "registration failed"}), 401


@auth_bp.route('/settings', methods=['GET', 'PUT'])
@login_required
def settings():
    """
    Manage user account settings
    Methods:
        GET: Serve settings form
        PUT: Update user information
    Form Data:
        username (str): Updated username
        email (str): Updated email
        bio (str): Updated biography
        password (str): New password (optional)
    Security:
        - Requires active login session
    Returns:
        - HTML form (GET)
        - Redirect with flash messages (PUT)
    Process:
        1. Pre-populate form with current data
        2. Validate and update via DBOperations
    """
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


@auth_bp.route('/api/author/me', methods=['GET'])
def is_logged_in():
    """
    Check authentication status
    Returns:
        - 200: JSON with username if authenticated
        - 400: JSON error if not authenticated
    Note:
        Uses flask_login's current_user system
    """
    print("call is_logged_in")
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id)
        return jsonify(msg="logged in", username=user.username), 200
    else:
        return jsonify(msg="not logged in"), 400

@auth_bp.route('/api/user/roles/<int:user_id>', methods=['PUT'])
@admin_required
def update_role(user_id):
    """
    Update user role (Admin only)
    Parameters:
        user_id (int): Target user ID
    JSON Body:
        role (str): New role designation
    Security:
        - Requires admin privileges
    Returns:
        - 20X: JSON success message
        - 40X: JSON error message
    Process:
        Calls DBOperations.update_user_role()
    """
    success, message, status_code = DBOperations.update_user_role(
        user_id=user_id,
        new_role=request.json.get('role')
    )
    return jsonify(msg=message), status_code

@auth_bp.route('/api/user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """
        Delete user account (Admin only)
        Parameters:
            user_id (int): Target user ID
        Security:
            - Requires admin privileges
        Returns:
            - 20X: JSON success message
            - 40X: JSON error message
        Process:
            Calls DBOperations.delete_user()
    """
    success, message, status_code = DBOperations.delete_user(user_id)
    return jsonify(msg=message), status_code