import pytest
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from app.models import *
from app import create_app
from app.models import db
from pathlib import Path
SAMPLE_DIR = Path(__file__).parent / "chapter_sample"
TXT_FILES = [str(f) for f in SAMPLE_DIR.glob("*.txt")]

def init_test_categories():
    """返回测试用分类数据"""
    return [
        {"id": 1, "name": "玄幻奇幻"},
        {"id": 2, "name": "都市生活"}, 
        {"id": 3, "name": "科幻未来"}, 
        {"id": 4, "name": "武侠仙侠"},
        {"id": 5, "name": "悬疑惊悚-犯罪心理"},
        {"id": 6, "name": "历史军事"},
        {"id": 7, "name": "游戏竞技"}, 
        {"id": 8, "name": "二次元"},
        {"id": 9, "name": "西方奇幻"},
        {"id": 10, "name": "无限流"},
        {"id": 11, "name": "系统快穿"}, 
        {"id": 12, "name": "古言宅斗"}, 
        {"id": 13, "name": "星际机甲"}, 
        {"id": 14, "name": "克苏鲁"}, 
        {"id": 15, "name": "其他"}  
    ]
    
@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        db.session.query(BookShelf).delete()
        db.session.query(ReadingRecord).delete()
        db.session.query(Comment).delete()
        db.session.query(Chapter).delete()
        db.session.query(Article).delete()
        db.session.query(User).delete()
        db.session.query(Category).delete()
        db.session.query(ArticleKeyword).delete()
        db.session.query(KeyWord).delete()
        
        for data in init_test_categories():
            category = Category(**data)
            db.session.add(category)
        db.session.commit()
    return app

class TestDBOperations:
    
    def test_register_new_user_success(self, app):
        """测试新用户注册成功"""
        with app.app_context():
            db.session.query(BookShelf).delete()
            db.session.query(ReadingRecord).delete()
            db.session.query(Comment).delete()
            db.session.query(Chapter).delete()
            db.session.query(Article).delete()
            db.session.query(User).delete()
            db.session.query(CreationList).delete()
            db.session.commit()
            
            # 用户1 ZHENG Kexin，作者用户
            result = DBOperations.create_user(
                'ZHENG Kexin', '1155173723@link.cuhk.edu.hk', '200211zkx'
            )
            user = DBOperations.get_user_by_username('ZHENG Kexin')
            assert user is not None
            assert user.check_password('200211zkx')
            
            result = DBOperations.update_user_settings(
                user.id, 
                {
                    'username': 'Zheng Kexin', 
                    'gender': 'F',
                    'is_author': 1
                }
            )
            assert result == (True, "设置更新成功")
            updated_user = User.query.get(user.id)
            assert updated_user.gender == 'F'
            
            with app.test_request_context():
                result = DBOperations.authenticate_user(
                    '1155173723@link.cuhk.edu.hk', 
                    '200211zkx'
                )
                
                assert result[0] is True
                assert result[2] == "登录成功"
                
                user = db.session.get(User, result[1].id)
                assert user.email == '1155173723@link.cuhk.edu.hk'
                
                article_data = {
                    'article_name': '兽人永不为奴！',
                    'cat_id': 1,
                    'status': '连载中',
                    'intro': """星际战将，艾斯温格家族掌权人斯诺德*艾斯温格上将，四年前，在兽化过程中血脉失控，
                        血脉过于强劲，上将在兽化的瞬间就丧失了人类记忆。
                        攻击所有在他面前的人和兽，
                        酣畅淋漓的一场战斗，消失在了中央星系人造返祖兽型试炼场。
                        艾斯温格家族心急如焚，无数次进场寻找，
                        家族优秀兽血继承人试图召唤，都未能成功。
                        上将的信号都是偶尔出现，迅速断连，全联邦技术人员出手都无法捕捉上将信号。
                        三年前，联邦最高军事法庭，决定开启星际直播。
                        拥有兽血的星际天才们在全联邦关注下，一一完成血脉融合，回归文明社会，
                        依旧没有联邦公民期待已久的上将身影。
                        艾斯温格家族即将放弃，
                        某天，人造生态园，兽型试炼场出现了一只狗怂狗怂的母狮。
                        奇迹出现了。
                        消失已久的上将他求偶了。"""
                }
                article_keywords = ['星际', '甜文', '直播', '沙雕']

                article = DBOperations.create_article(user.id, article_data, article_keywords)
                assert article is not None
                assert article.article_name == '兽人永不为奴！'
                assert article.author_id == user.id
                
                db_article = db.session.get(Article, article.id)
                assert db_article is not None
                assert db_article.cat_id == 1

                creation = CreationList.query.filter_by(article_id=article.id).first()
                assert creation.article_name == '兽人永不为奴！'
                assert creation.author_id == user.id
                
                chapter_data1 = {
                    "chapter_name": "第一章",
                    "word_count": 5000,
                    "text_path": TXT_FILES[0],
                    "status": "published",
                    "is_draft": False
                }
                
                chapter_data2 = {
                    "chapter_name": "第二章",
                    "word_count": 5000,
                    "text_path": TXT_FILES[1],
                    "status": "published",
                    "is_draft": False
                }
                
                chapter_data3 = {
                    "chapter_name": "第三章",
                    "word_count": 5000,
                    "text_path": TXT_FILES[2],
                    "status": "serialized",
                    "is_draft": True
                }
                success, chapter1 = DBOperations.create_chapter(
                    article.id,
                    chapter_data1
                )
            assert success is True
            assert chapter1.chapter_name == "第一章"
            assert Path(chapter1.text_path).exists()  # 验证文件真实存在

            updated_article = db.session.get(Article, article.id)
            assert updated_article.chapter_number == 1
            assert updated_article.latest_update_chapter_name == "第一章"
            assert (datetime.utcnow() - updated_article.latest_update_time) < timedelta(seconds=1)
        
            success, chapter2 = DBOperations.create_chapter(
                article.id,
                chapter_data2
            )
            
            success, chapter3 = DBOperations.create_chapter(
                article.id,
                chapter_data3
            )
            
            result = DBOperations.delete_chapter(chapter2.id)
            assert result == True
            
            latest_article = DBOperations.get_latest_articles()
            assert latest_article[0].id == article.id
            
            # 用户2 3： LIN Dachaun & YANG Zihao，普通读者用户
    
            result2 = DBOperations.create_user(
                'LIN Dachaun', '1155191482@link.cuhk.edu.hk', 'lindachuan'
            )
            result3 = DBOperations.create_user(
                'YANG Zihao', '1155191399@link.cuhk.edu.hk', 'yangzihao'
            )
            user_lindachuan = DBOperations.get_user_by_username('LIN Dachaun')
            user_yangzihao = DBOperations.get_user_by_username('YANG Zihao')
            
            DBOperations.update_user_settings(user_lindachuan.id, {'gender': 'M', 'is_author': 0})
            DBOperations.update_user_settings(user_yangzihao.id, {'gender': 'M', 'is_author': 0})
            
            DBOperations.add_article_view(article.id)
            DBOperations.add_article_view(article.id)
            DBOperations.add_to_bookshelf(user_lindachuan.id, article.id)
            DBOperations.add_to_bookshelf(user_yangzihao.id, article.id)
            comment1 = DBOperations.create_comment(user_lindachuan.id, article.id, "写的什么玩意依托...")
            comment2 = DBOperations.create_comment(user_yangzihao.id, article.id, "我觉得还不错啊，至少很猎奇")
            DBOperations.delete_book_from_shelf(user_lindachuan.id, article.id)
            DBOperations.update_reading_progress(user_yangzihao.id, article.id, chapter3.id, 3)
            
            like_result, total_likes = DBOperations.make_like(article.id)
            assert like_result == True
            assert total_likes == 1