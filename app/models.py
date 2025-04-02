from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    gender = db.Column(db.String(1))
    password_hash = db.Column(db.String(128))
    is_author = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    balance = db.Column(db.Integer, default=0)
    
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
            'gender': self.gender,
            'email': self.email,
            'is_author': bool(self.is_author),
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'balance': float(self.balance) if self.balance else 0.0
        }
    

class ReadingRecord(db.Model):
    __tablename__ = 'reading_record'
    
    id = db.Column(db.Integer, primary_key=True)
    
    article_id = db.Column(
        db.Integer, 
        db.ForeignKey('article.id'),
        nullable=False,
        index=True
    )
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id'),
        nullable=False,
        index=True
    )
    latest_reading_chapter_id = db.Column(
        db.Integer, 
        db.ForeignKey('chapter.id'),
        index=True
    )
    
    article_name = db.Column(db.String(200))
    latest_reading_time = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    cumulative_reading_time = db.Column(db.Numeric(10, 2), default=0.0) 
    
    user = db.relationship('User', back_populates='reading_record')
    article = db.relationship('Article', back_populates='reading_record')
    chapter = db.relationship('Chapter', back_populates='reading_record')
    
    def __repr__(self):
        return f'<ReadingRecord user={self.user_id} article={self.article_id}>'
    
    def update_reading(self, chapter_id, duration_hours):
        self.latest_reading_chapter_id = chapter_id
        self.cumulative_reading_time += duration_hours
        self.latest_reading_time = datetime.utcnow()


class CreationList(db.Model):
    __tablename__ = 'creation_list'
    
    id = db.Column(db.Integer, primary_key=True)
    
    author_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id'),
        nullable=False
    )
    article_id = db.Column(db.Integer, nullable=False)
    article_name = db.Column(db.String(200))
    create_date = db.Column(db.Date)
    latest_update_time = db.Column(db.Date)
    latest_update_chapter_name = db.Column(db.String(100))
    views = db.Column(db.Integer)
    
    author = db.relationship(
        'User',
        back_populates='creation_lists'
    )
    
    def __repr__(self):
        return f'<CreationList {self.article_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'article_name': self.article_name,
            'author_id': self.author_id,
            'article_id': self.article_id,
            'create_date': self.create_date.isoformat() if self.create_date else None,
            'latest_update_time': self.latest_update_time.isoformat() if self.latest_update_time else None,
            'latest_chapter': self.latest_update_chapter_name,
            'views': self.views
        }


class Article(db.Model):
    __tablename__ = 'article'
    
    id = db.Column(db.Integer, primary_key=True)
    
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),  # 添加数据库级联
        nullable=True # False?
    )
    cat_id = db.Column(
        db.Integer, 
        db.ForeignKey('category.id'),
        nullable=False,
        index=True
    )
    
    article_name = db.Column(db.String(200), nullable=False)
    cat_name = db.Column(db.String(50))
    chapter_number = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='serialized')
    
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    latest_update_time = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    latest_update_chapter_name = db.Column(db.String(200))
    
    is_published = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    intro = db.Column(db.Text)  # CLOB -> Text
    word_count = db.Column(db.Integer, default=0)
    
    author = db.relationship(
        'User', 
        back_populates='articles'
    )
    category = db.relationship(
        'Category', 
        back_populates='articles'
    )
    bookshelves = db.relationship(
        'BookShelf', 
        back_populates='article',
        cascade='all, delete-orphan'
    )
    
    chapters = db.relationship(
        'Chapter', 
        back_populates='article',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    reading_record = db.relationship(
        'ReadingRecord', 
        back_populates='article',
        lazy='dynamic'
    )
    comments = db.relationship(
        'Comment', 
        back_populates='article',
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<Article {self.article_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'article_name': self.article_name,
            'author_id': self.author_id,
            'latest_chapter': self.latest_update_chapter_name,
            'word_count': self.word_count,
        }


class BookShelf(db.Model):
    __tablename__ = 'book_shelf'
    
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id'),
        nullable=False,
        index=True
    )
    article_id = db.Column(
        db.Integer, 
        db.ForeignKey('article.id'),
        nullable=False,
        index=True
    )
    
    article_name = db.Column(db.String(200))
    
    user = db.relationship(
        'User', 
        back_populates='bookshelves'
    )
    article = db.relationship(
        'Article', 
        back_populates='bookshelves'
    )
    
    def __repr__(self):
        return f'<BookShelf user={self.user_id} article={self.article_id}>'


class Chapter(db.Model):
    __tablename__ = 'chapter'
    
    id = db.Column(db.Integer, primary_key=True)
    
    article_id = db.Column(
        db.Integer, 
        db.ForeignKey('article.id'),
        nullable=False,
        index=True
    )
    
    chapter_name = db.Column(db.String(200), nullable=False)
    word_count = db.Column(db.Integer, default=0)
    latest_update_time = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    text_path = db.Column(db.String(200))
    is_draft = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='published')
    
    article = db.relationship(
        'Article', 
        back_populates='chapters'
    )
    reading_record = db.relationship(
        'ReadingRecord',
        back_populates='chapter',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Chapter {self.chapter_name} of Article {self.article_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'chapter_name': self.chapter_name,
            'word_count': self.word_count,
            'update_time': self.latest_update_time.isoformat(),
            'is_draft': self.is_draft
        }


class KeyWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(20))
    count = db.Column(db.Integer, default=0)
    is_hot = db.Column(db.Boolean, default=False)


class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    articles = db.relationship(
        'Article', 
        back_populates='category',
        lazy='dynamic'
    )


class Comment(db.Model):
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id'),
        nullable=False,
        index=True
    )
    article_id = db.Column(
        db.Integer, 
        db.ForeignKey('article.id'),
        nullable=False,
        index=True
    )
    
    context = db.Column(db.Text, nullable=False)
    time = db.Column(
        db.DateTime, 
        default=datetime.utcnow,
        index=True
    )
    
    user = db.relationship('User', back_populates='comments')
    article = db.relationship('Article', back_populates='comments')
    
    def __repr__(self):
        return f'<Comment by User {self.user_id} at {self.time}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.context,
            'time': self.time.isoformat()
        }

# TODO: add other necessary classes 
# class SignIn(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     date = db.Column(db.Date, default=datetime.utcnow().date)  # 记录签到日期（不含时间）

#     # 唯一约束：每个用户每天只能签到一次
#     __table_args__ = (db.UniqueConstraint('user_id', 'date', name='uq_user_date'),)

#     user = db.relationship('User', backref='sign_ins')

# class Trade(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 打赏者
#     to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    # 作者
#     article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
#     amount = db.Column(db.Integer, nullable=False)  # 打赏金额（单位：虚拟币）
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)

#     from_user = db.relationship('User', foreign_keys=[from_user_id], backref='sent_transactions')
#     to_user = db.relationship('User', foreign_keys=[to_user_id], backref='received_transactions')
#     article = db.relationship('Article', backref='transactions')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))