from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_author = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    balance = db.Column(db.Integer, default=0)
    last_read_book = db.Column(db.String(140))
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

class BookShelf(db.Model):  # 修正：类名首字母大写
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_name = db.Column(db.String(140))

class ReadingProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 单一主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 外键关联用户
    book_id = db.Column(db.Integer, db.ForeignKey('article.id'))  # 外键关联文章
    last_read_chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))  # 外键关联章节
    last_read_date = db.Column(db.DateTime, default=datetime.utcnow)
    cumulative_reading_time = db.Column(db.Integer, default=0)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content_path = db.Column(db.String(500))
    order = db.Column(db.Integer, default=0)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    is_draft = db.Column(db.Boolean, default=True)  # 章节草稿状态
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class KeyWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(20))
    count = db.Column(db.Integer, default=0)
    is_hot = db.Column(db.Boolean, default=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(30))
    cat_books = db.relationship('Article', backref='category', lazy='dynamic')  # 修正：定义关系字段

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))