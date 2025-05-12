from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, PasswordField, IntegerField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError, Optional
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='无效的邮箱格式')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空')
    ])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RenameForm(FlaskForm):
    authorName = StringField('new_name', validators=[])

class TippingForm(FlaskForm):
    tips = IntegerField('tips', validators=[])

class SettingsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(0, 500)])
    password = PasswordField('New Password', validators=[Optional(), Length(6, 128)])

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=20, message='用户名长度需在3-20个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='无效的邮箱格式')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, message='密码至少需要6个字符')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次密码不一致')
    ])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已被使用')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已被注册')