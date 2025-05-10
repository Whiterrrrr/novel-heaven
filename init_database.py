import json
from pathlib import Path
from app import create_app
from app.models import db
from app.models import *

BASE_DIR = Path(__file__).parent
SAMPLE_DIR = BASE_DIR / "book_sample"

app = create_app()

def init_test_categories():
    return [
        {"id": 1, "name": "Fantasy"},
        {"id": 2, "name": "Urban"}, 
        {"id": 3, "name": "SciFi"}, 
        {"id": 4, "name": "Wuxia"},
        {"id": 5, "name": "Thriller"},
        {"id": 6, "name": "Historical"},
        {"id": 7, "name": "Gaming"}, 
        {"id": 8, "name": "ACGN"},
        {"id": 9, "name": "WesternFantasy"},
        {"id": 10, "name": "Infinite"},
        {"id": 11, "name": "SystemTravel"}, 
        {"id": 12, "name": "AncientRomance"}, 
        {"id": 13, "name": "Mecha"}, 
        {"id": 14, "name": "Cthulhu"}, 
        {"id": 15, "name": "Others"}  
    ]

def init_users():
    with app.app_context():
        db.create_all()
        db.session.query(Comment).delete()
        db.session.query(ReadingRecord).delete()
        db.session.query(BookShelf).delete()
        db.session.query(Chapter).delete()
        db.session.query(ArticleKeyword).delete()
        db.session.query(KeyWord).delete()
        db.session.query(CreationList).delete()
        db.session.query(Article).delete()
        db.session.query(Category).delete()
        db.session.query(User).delete()
        db.session.query(Tipping).delete()
        for data in init_test_categories():
            category = Category(**data)
            db.session.add(category)
        db.session.commit()

        authors = [
            {
                "username": "ZHENG_Kexin",
                "email": "1155173723@link.cuhk.edu.hk",
                "password": "200211zkx",
                "is_author": True,
                "gender": "F"
            },
            {
                "username": "QI_Haomin",
                "email": "qi_haomin@example.com",
                "password": "qi_password",
                "is_author": True,
                "gender": "M"
            },
            {
                "username": "XU_Chenyan",
                "email": "xu_chenyan@example.com",
                "password": "xu_password",
                "is_author": True,
                "gender": "M"
            }
        ]

        readers = [
            {
                "username": "LIN_Dachaun",
                "email": "1155191482@link.cuhk.edu.hk",
                "password": "lindachuan",
                "gender": "M"
            },
            {
                "username": "YANG_Zihao",
                "email": "1155191399@link.cuhk.edu.hk",
                "password": "yangzihao",
                "gender": "M"
            }
        ]

        for user_data in authors + readers:
            DBOperations.create_user(
                user_data["username"], 
                user_data["email"], 
                user_data['password'],
                user_data['gender'],
                user_data.get("is_author", False),
            )


def process_books():
    with app.app_context():
        for author_dir in SAMPLE_DIR.iterdir():
            author_name = author_dir.name
            author_user = DBOperations.get_user_by_username(author_name)

            for book_dir in author_dir.iterdir():
                meta_file = book_dir / "article_info.json"
                with open(meta_file, "r", encoding="utf-8") as f:
                    book_data = json.load(f)

                article = DBOperations.create_article(
                    author_user.id,
                    {
                        "article_name": book_data["article_name"],
                        "cat_id": book_data["cat_id"],
                        "status": book_data["status"],
                        "intro": book_data["intro"]
                    },
                    book_data.get("article_keywords", [])
                )

                chapters_dir = book_dir / "chapter"
                for idx, ch_file in enumerate(sorted(chapters_dir.glob("chapter*.txt")), 1):
                    with open(ch_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    DBOperations.create_chapter(
                        article.id,
                        {
                            "chapter_name": f"第{idx}章",
                            "text_path": str(ch_file.relative_to(BASE_DIR)),
                            "word_count": len(content),
                            "status": "published"
                        }
                    )


def init_interactions():
    with app.app_context():
        articles = DBOperations.get_latest_articles(limit=100)
        lin = DBOperations.get_user_by_username("LIN_Dachaun")
        yang = DBOperations.get_user_by_username("YANG_Zihao")

        # 阅读记录
        for article in articles:
            DBOperations.update_reading_progress(
                user_id=lin.id,
                article_id=article.id,
                chapter_id=1,
                duration_hours=2.5
            )
            DBOperations.update_reading_progress(
                user_id=yang.id,
                article_id=article.id,
                chapter_id=3,
                duration_hours=5.0
            )
            DBOperations.make_like(article.id)
            DBOperations.add_article_view(article.id)
            DBOperations.add_to_bookshelf(lin.id, article.id)
            DBOperations.add_to_bookshelf(yang.id, article.id)

        comments = [
            (lin.id, "这本书的设定太棒了！"),
            (yang.id, "期待后续章节更新！"),
            (lin.id, "文笔还可以再精炼些")
        ]
        tippings = [
            (lin.id, 5),
            (yang.id, 10),
            (lin.id, 5)
        ]
        for article in articles:
            for user_id, content in comments:
                DBOperations.create_comment(
                    user_id=user_id,
                    article_id=article.id,
                    content=content
                )
            for user_id, tip in tippings:
                DBOperations.create_tipping(
                    user_id=user_id,
                    article_id=article.id,
                    amount=tip
                )

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        print("=== 开始初始化数据库 ===")
        init_users()
        
        process_books()
        print("书籍数据导入完成")
        
        init_interactions()
        print("交互数据生成完成")
        
        search_result, _, _, _ = DBOperations.search_books('宫廷', search_by_keyword=True)
        print(search_result)
        keylist_result = DBOperations.keytag_list('宫廷')
        print(keylist_result)
        article_statistics = DBOperations.get_article_statistics(search_result[0].id)
        print(article_statistics)
        