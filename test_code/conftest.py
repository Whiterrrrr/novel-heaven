# conftest.py
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from datetime import datetime
from app import create_app
from app.models import db, User, Article, Chapter, Comment, ReadingRecord, BookShelf

@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# conftest.py
@pytest.fixture(scope='function')
def init_database(app):
    with app.app_context():
        # 清空所有表数据，避免主键冲突
        db.session.query(BookShelf).delete()
        db.session.query(ReadingRecord).delete()
        db.session.query(Comment).delete()
        db.session.query(Chapter).delete()
        db.session.query(Article).delete()
        db.session.query(User).delete()
        db.session.commit()  # 确保删除操作提交

        # 创建测试作者用户
        author = User(
            id=1001,
            username='启夫微安',
            email='qifuwei@an.com',
            gender='M',
            is_author=True,
            joined_at=datetime(2023, 1, 1),
            last_seen=datetime(2023, 10, 20),
            balance=1000
        )
        author.set_password("qifuwei_secure_password")
        db.session.add(author)

        # 创建书籍数据
        article = Article(
            id=2001,
            author_id=1001,
            cat_id=1,
            article_name='兽人永不为奴！',
            cat_name='星际小说',
            chapter_number=5,
            status='连载中',
            create_time=datetime(2023, 1, 1),
            latest_update_time=datetime(2023, 10, 15),
            latest_update_chapter_name='第一章 消失的上将',
            is_published=True,
            views=15000,
            likes=3,
            intro='星际战将斯诺德·艾斯温格在兽化中失控...',
            word_count=50000
        )
        db.session.add(article)

        reader_a = User(id=1002, username='读者A', email='reader_a@test.com', gender='F')
        reader_b = User(id=1003, username='读者B', email='reader_b@test.com', gender='M')
        reader_c = User(id=1004, username='读者C', email='reader_c@test.com', gender='F')
        db.session.add_all([reader_a, reader_b, reader_c])

        # 创建章节（必须添加）
        chapter1 = Chapter(
            id=3001, 
            article_id=2001, 
            chapter_name='第一章 消失的上将', 
            word_count=10000,
            latest_update_time=datetime(2023, 1, 5),
            text_path='/text/chapter1.txt',
            is_draft=False,
            status='已发布'
        )
        chapter2 = Chapter(
            id=3002, 
            article_id=2001, 
            chapter_name='第二章 兽型试炼场', 
            word_count=8000,
            latest_update_time=datetime(2023, 3, 12),
            text_path='/text/chapter2.txt',
            is_draft=False,
            status='已发布'
        )
        db.session.add_all([chapter1, chapter2])

        # 创建评论（必须添加）
        comment1 = Comment(
            id=5001, 
            user_id=1002, 
            article_id=2001, 
            context='笑死了，上将变狗怂母狮这段太沙雕了！',
            time=datetime(2023, 10, 16, 14, 30)
        )
        comment2 = Comment(
            id=5002, 
            user_id=1003, 
            article_id=2001, 
            context='星际直播设定超带感，求更新！',
            time=datetime(2023, 10, 16, 15, 45)
        )
        db.session.add_all([comment1, comment2])

        # 创建阅读记录（必须添加）
        reading_record1 = ReadingRecord(
            id=6001, 
            user_id=1002, 
            article_id=2001,
            latest_reading_chapter_id=3001,
            latest_reading_time=datetime(2023, 10, 16, 14, 0),
            cumulative_reading_time=4.5
        )
        reading_record2 = ReadingRecord(
            id=6002, 
            user_id=1003, 
            article_id=2001,
            latest_reading_chapter_id=3002,
            latest_reading_time=datetime(2023, 10, 16, 15, 30),
            cumulative_reading_time=6.2
        )
        db.session.add_all([reading_record1, reading_record2])

        # 创建章节、评论、阅读记录等数据（略）
        db.session.commit()
    yield db