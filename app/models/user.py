from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .base import db

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):

    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    authorname = db.Column(db.String(10), index=True, unique=False)
    email = db.Column(db.String(100), index=True, unique=True)
    gender = db.Column(db.String(1))
    password_hash = db.Column(db.String(128))
    is_author = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    balance = db.Column(db.Integer, default=0)
    token = db.Column(db.String(128))
    
    creation_lists = db.relationship(
        'CreationList',
        back_populates='author', 
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    articles = db.relationship(
        'Article',
        back_populates='author',
        lazy='dynamic',
        cascade='all, delete-orphan',  # 添加级联删除
        passive_deletes=True  # 允许数据库级联
    )
    bookshelves = db.relationship(
        'BookShelf', 
        back_populates='user',
        lazy='dynamic'
    )
    reading_record = db.relationship(
        'ReadingRecord', 
        back_populates='user',
        lazy='dynamic'
    )
    comments = db.relationship(
        'Comment', 
        back_populates='user',
        lazy='dynamic'
    )
    tippings = db.relationship(
        'Tipping',
        back_populates='user',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'authorname': self.authorname,
            'gender': self.gender,
            'email': self.email,
            'is_author': bool(self.is_author),
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'balance': float(self.balance) if self.balance else 0.0
        }