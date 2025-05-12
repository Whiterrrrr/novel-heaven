import decimal
from datetime import datetime

import pytz

from .base import db

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
    chapter_number = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='ongoing')
    
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
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    comments = db.relationship(
        'Comment', 
        back_populates='article',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    tippings = db.relationship(
        'Tipping',
        back_populates='article',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __init__(self, author_id, create_time, latest_update_time, latest_update_chapter_name, **kwargs):
        self.author_id=author_id
        self.create_time=create_time
        self.latest_update_time=latest_update_time
        self.latest_update_chapter_name=latest_update_chapter_name
        super(Article, self).__init__(**kwargs)

    
    def __repr__(self):
        return f'<Article {self.article_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.article_name,
            'category': self.category.name,
            "article_name": self.article_name,
            "author":self.author.username
            #'latest_chapter': self.latest_update_chapter_name,
            #'word_count': self.word_count,
        }
    def to_dict1(self):
        return {
            'id': self.id,
            'title': self.article_name,
            'author':self.author.username,
            'status':self.status
            
        }
    def to_dict2(self):
        return {
            "id": self.id,
            "article_name": self.article_name,
            "status": self.status,
            "word_count": self.word_count,
            "latest_update_time":self.latest_update_time,
            "intro": self.intro,
            "author":self.author.username,
            "category":self.category.name,
            "views": self.views,
            "likes": self.likes
        }
        
class Chapter(db.Model):
    __tablename__ = 'chapter'
    
    id = db.Column(db.Integer, primary_key=True)
    
    article_id = db.Column(
        db.Integer, 
        db.ForeignKey('article.id'),
        nullable=False,
        index=True
    )

    chapter_id = db.Column(db.Integer, nullable=False)
    
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
        back_populates='chapter'
    )
    
    def __repr__(self):
        return f'<Chapter {self.chapter_name} of Article {self.article_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'chapter_name': self.chapter_name,
            'word_count': self.word_count,
            'update_time': self.latest_update_time.isoformat(),
            'is_draft': self.is_draft,
        }
        
        
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
        default=datetime.now(pytz.utc),
        onupdate=datetime.now(pytz.utc)
    )
    cumulative_reading_time = db.Column(db.Numeric(10, 2), default=0.0) 
    
    user = db.relationship('User', back_populates='reading_record')
    article = db.relationship('Article', back_populates='reading_record')
    chapter = db.relationship('Chapter', back_populates='reading_record')
    
    def __repr__(self):
        return f'<ReadingRecord user={self.user_id} article={self.article_id} chapter={self.latest_reading_chapter_id}>'
    
    def update_reading(self, chapter_id, duration_hours):
        def flaot_to_decimal(value):
            return decimal.Decimal(str(value)).quantize(decimal.Decimal('0.00'), rounding=decimal.ROUND_HALF_UP)
        self.latest_reading_chapter_id = chapter_id
        self.cumulative_reading_time += flaot_to_decimal(duration_hours)
        self.latest_reading_time = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'article_id': self.article_id,
            'article_name':self.article_name,
            'latest_reading_chapter_id':self.latest_reading_chapter_id,
            'cumulative_reading_time':self.cumulative_reading_time,
            'latest_reading_time': self.latest_reading_time.isoformat()
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'article_id':self.article_id
        }