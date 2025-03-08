from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    gender = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    is_author = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    balance = db.Column(db.Integer, default=0)
    last_read_book = db.Column(db.String(140))
    creation_lists = db.relationship('CreationList', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    reading_progresses = db.relationship('ReadingProgress', backref='author', lazy='dynamic')
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SignIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)  # 记录签到日期（不含时间）

    # 唯一约束：每个用户每天只能签到一次
    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='uq_user_date'),)

    user = db.relationship('User', backref='sign_ins')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 打赏者
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    # 作者
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)  # 打赏金额（单位：虚拟币）
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系定义
    from_user = db.relationship('User', foreign_keys=[from_user_id], backref='sent_transactions')
    to_user = db.relationship('User', foreign_keys=[to_user_id], backref='received_transactions')
    article = db.relationship('Article', backref='transactions')

class ReadingProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    last_read_chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    last_read_date = db.Column(db.DateTime, default=datetime.utcnow)
    cumulative_reading_time = db.Column(db.Integer, default=0)

    article = db.relationship('Article', backref='reading_progresses')
    chapter = db.relationship('Chapter', backref='reading_progresses')

class CreationList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    book_name = db.Column(db.String(140))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    latest_update_time = db.Column(db.DateTime, default=datetime.utcnow)
    latest_update_section_name = db.Column(db.String(140))
    readership = db.Column(db.Integer, default=0)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    is_draft = db.Column(db.Boolean, default=True)
    introduction = db.Column(db.String(500))
    chapters = db.relationship('Chapter', backref='article', lazy='dynamic')

class BookShelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_name = db.Column(db.String(140))

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content_path = db.Column(db.String(500))
    order = db.Column(db.Integer, default=0)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    is_draft = db.Column(db.Boolean, default=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class KeyWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(20))
    count = db.Column(db.Integer, default=0)
    is_hot = db.Column(db.Boolean, default=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(30))
    cat_books = db.relationship('Article', backref='category', lazy='dynamic')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))