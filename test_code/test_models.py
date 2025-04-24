# from app.models import User, Article, Category, Comment, Chapter, ReadingRecord

# def test_author_creation(init_database):
#     author = User.query.get(1001)
#     assert author.username == '启夫微安'
#     assert author.is_author is True
#     assert author.check_password("qifuwei_secure_password") is True

# def test_article_relationship(init_database):
#     author = User.query.get(1001)
#     article = author.articles.first()
    
#     assert article.article_name == '兽人永不为奴！'
#     assert article.status == '连载中'
#     assert article.likes == 3

# def test_chapter_belongs_to_article(init_database):
#     article = Article.query.get(2001)
#     chapters = Chapter.query.filter_by(article_id=2001).all()
    
#     assert len(chapters) >= 2
#     assert chapters[0].chapter_name == '第一章 消失的上将'

# def test_comment_associations(init_database):
#     comment = Comment.query.get(5001)
#     user = User.query.get(1002)
#     article = Article.query.get(2001)
    
#     assert comment.user == user
#     assert comment.article == article
#     assert '沙雕' in comment.context

# def test_reading_record_updates(init_database):
#     record = ReadingRecord.query.get(6001)
#     user = User.query.get(1002)
    
#     assert user.reading_record.first() == record
#     assert record.cumulative_reading_time == 4.5

# def test_bookshelf_operations(init_database):
#     user = User.query.get(1003)
#     assert user.bookshelves.count() == 1
#     assert user.bookshelves.first().article_name == '兽人永不为奴！'