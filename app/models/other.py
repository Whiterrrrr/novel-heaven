from datetime import datetime
from .base import db

class KeyWord(db.Model):
    __tablename__ = 'keyword'
    
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(20), unique=True)
    is_hot = db.Column(db.Boolean, default=False)
    
    @property
    def usage_count(self):
        return db.session.query(ArticleKeyword).filter_by(keyword_id=self.id).count()

class ArticleKeyword(db.Model):
    __tablename__ = 'article_keyword'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'))
    keyword_id = db.Column(db.Integer, db.ForeignKey('keyword.id', ondelete='CASCADE'))
    
    __table_args__ = (
        db.UniqueConstraint('article_id', 'keyword_id', name='uq_article_keyword'),
    )


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
        default=datetime.now,
        index=True
    )

    user = db.relationship('User', back_populates='comments')
    article = db.relationship('Article', back_populates='comments')

    def __repr__(self):
        return f'<Comment by User {self.user_id} at {self.time}>'

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.user.username,
            'content': self.context,
            'time': self.time.isoformat()
        }


class Tipping(db.Model):
    __tablename__ = 'tipping'

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

    amount = db.Column(db.Integer, nullable=False)

    time = db.Column(
        db.DateTime,
        default=datetime.now,
        index=True
    )

    user = db.relationship('User', back_populates='tippings')
    article = db.relationship('Article', back_populates='tippings')

    def __repr__(self):
        return f'<Tipped {self.amount} by User {self.user_id} at {self.time}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'time': self.time.isoformat()
        }
        
        
class Like(db.Model):
    __tablename__ = 'like'
    
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
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow
    )
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'article_id', name='uq_user_article_like'),
    )
    
    user = db.relationship('User', back_populates='likes')
    article = db.relationship('Article', back_populates='likes')
    
    def __repr__(self):
        return f'<Like user={self.user_id} article={self.article_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'article_id': self.article_id,
            'created_at': self.created_at.isoformat()
        }