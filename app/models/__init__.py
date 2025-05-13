import pytz
from flask import session

from .base import db
from .user import *
from .book import *
from .other import *
from datetime import *
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

class DBOperations:
    @staticmethod
    def update_user_role(user_id, new_role):
        """
        update role management
        :param user_id: int
        :param new_role: str
        :return: (success: bool, message: str, status_code: int)
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found", 404
            
            user.role = new_role
            db.session.commit()
            return True, "Role updated", 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Database error: {str(e)}", 500

    @staticmethod
    def delete_user(user_id):
        """
        delete user, managed by admin
        :param user_id: int
        :return: (success: bool, message: str, status_code: int)
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found", 404
            
            db.session.delete(user)
            db.session.commit()
            return True, "User deleted", 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Database error: {str(e)}", 500

    @staticmethod
    def update_user_settings(user_id, update_data):
        """
        :param user_id: int
        :param update_data: dict
        :return: (success: bool, message: str)
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "用户不存在"

            if 'username' in update_data:
                if User.query.filter(
                    User.username == update_data['username'],
                    User.id != user_id
                ).first():
                    return False, "Username has been used "

            if 'email' in update_data:
                if User.query.filter(
                    User.email == update_data['email'],
                    User.id != user_id
                ).first():
                    return False, "email has been registered"

            allowed_fields = {'username', 'email', 'authorname', 'gender', 'password', 'is_author', 'joined_at', 'last_seen', 'balance'}
            for field, value in update_data.items():
                if field in allowed_fields:
                    if field == 'password':
                        user.set_password(value)
                    else:
                        setattr(user, field, value)

            db.session.commit()
            return True, "update suc"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"update fail: {str(e)}"
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def authenticate_user(email, password, remember=False):
        """
        authenticate
        :param email: std
        :param password: std
        :param remember: bool
        :return: (success: bool, user: User | None, message: str)
        """
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                return False, None, "no user"
            
            if not user.check_password(password):
                return False, None, "wrong password"
            
            # user.last_seen = datetime.utcnow()
            db.session.commit()
            session['user_id'] = user.id
            login_user(user, remember=remember)
            return True, user, "login suc"
        except SQLAlchemyError:
            db.session.rollback()
            return False, None, "wrong database"

    @staticmethod
    def check_and_reward_daily_login(user):
        """
        deliver daily login reward
        :param user
        :return: (reward_given: bool, amount: int)
        """
        try:
            print("call check_and_reward_daily_login")
            print(user.last_seen.date(), date.today())
            if user.last_seen.date() == date.today():
                return False, 0
            user.last_seen = datetime.now(pytz.utc)
            print("get reward")
            reward = 10
            if user.balance == None:
                user.balance = 0
                
            user.balance += reward
            db.session.commit()
            return True, reward
        
        except SQLAlchemyError:
            db.session.rollback()
            return False, 0

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_reading_progress(user_id, article_id=None):
        try:
            query = ReadingRecord.query.filter_by(user_id=user_id)
            if article_id:
                return query.filter_by(article_id=article_id).first()
            return query.all()
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def create_user(username, email, password, gender=None, is_author=False):
        print(User.query.filter((User.username == username) or (User.email == email)).first())
        if User.query.filter((User.username == username) or (User.email == email)).first() is not None:
            print("Email or username used")
            return None
        
        new_user = User(
            username=username,
            authorname='',
            email=email,
            gender=gender,
            joined_at=datetime.now(pytz.utc),
            last_seen=datetime.now(pytz.utc) - timedelta(days=1),
            is_author=is_author
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return True, new_user, "造人成功"
        except SQLAlchemyError as e:
            db.session.rollback()
            print("error code:", str(e))
            return None
    
    @staticmethod
    def get_latest_articles(limit=1):
        """
        注意这里返回的是一个list!
        """
        return Article.query.order_by(Article.latest_update_time.desc()).limit(limit).all()

    @staticmethod
    def create_comment(user_id, article_id, content):
        try:
            if not Article.query.get(article_id):
                return None

            new_comment = Comment(
                user_id=user_id,
                article_id=article_id,
                context=content
            )
            db.session.add(new_comment)
            db.session.commit()
            return new_comment
        except SQLAlchemyError:
            db.session.rollback()
            return None


    @staticmethod
    def create_tipping(user_id, article_id, amount):
        try:
            if not Article.query.get(article_id):
                print("invalid book id")
                return None

            new_tipping = Tipping(
                user_id=user_id,
                article_id=article_id,
                amount=amount
            )
            db.session.add(new_tipping)
            db.session.commit()
            return new_tipping
        except SQLAlchemyError as e:
            db.session.rollback()
            print("error code:", str(e))
            return None

        
    @staticmethod
    def get_article_comments(article_id, page=1, per_page=20, include_user_info=False):
        try:
            base_query = Comment.query.filter_by(article_id=article_id)

            if include_user_info:
                base_query = base_query.join(User, Comment.user_id == User.id)
                base_query = base_query.add_entity(User)

            pagination = base_query.order_by(Comment.time.desc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

            results = []
            for record in pagination.items:
                if include_user_info:
                    comment, user = record
                    result = comment.to_dict()
                    result['user'] = user.to_dict()
                else:
                    result = record.to_dict()
                results.append(result)

            return results, pagination.pages
        except SQLAlchemyError:
            return [], 0

    @staticmethod
    def get_article_tippings(article_id, page=1, per_page=20, include_user_info=False):
        try:
            base_query = Tipping.query.filter_by(article_id=article_id)

            if include_user_info:
                base_query = base_query.join(User, Tipping.user_id == User.id)
                base_query = base_query.add_entity(User)

            pagination = base_query.order_by(Tipping.time.desc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

            results = []
            for record in pagination.items:
                if include_user_info:
                    tipping, user = record
                    result = tipping.to_dict()
                    result['user'] = user.to_dict()
                else:
                    result = record.to_dict()
                results.append(result)

            return results, pagination.pages
        except SQLAlchemyError:
            return [], 0

    @staticmethod
    def delete_comment(comment_id, verify_user_id=None):
        try:
            comment = Comment.query.get(comment_id)
            if not comment:
                return False

            if verify_user_id and comment.user_id != verify_user_id:
                return False

            db.session.delete(comment)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def get_user_comments(user_id, days=None, limit=100):
        try:
            query = Comment.query.filter_by(user_id=user_id)
            
            if days:
                time_threshold = datetime.utcnow() - timedelta(days=days)
                query = query.filter(Comment.time >= time_threshold)

            comments = query.order_by(Comment.time.desc()).limit(limit).all()
            return [c.to_dict() for c in comments]
        except SQLAlchemyError:
            return []

    @staticmethod
    def get_user_tippings(user_id, days=None, limit=100):
        try:
            query = Tipping.query.filter_by(user_id=user_id)

            if days:
                time_threshold = datetime.utcnow() - timedelta(days=days)
                query = query.filter(Tipping.time >= time_threshold)

            tippings = query.order_by(Tipping.time.desc()).limit(limit).all()
            return [c.to_dict() for c in tippings]
        except SQLAlchemyError:
            return []

    @staticmethod
    def get_recent_comments(hours=24, limit=50):
        try:
            time_threshold = datetime.utcnow() - timedelta(hours=hours)
            
            query = db.session.query(Comment, Article.article_name)\
                .join(Article, Comment.article_id == Article.id)\
                .filter(Comment.time >= time_threshold)\
                .order_by(Comment.time.desc())\
                .limit(limit)

            return [{
                "comment": c[0].to_dict(),
                "article_title": c[1]
            } for c in query]
        except SQLAlchemyError:
            return []

    @staticmethod
    def get_recent_tippings(hours=24, limit=50):
        try:
            time_threshold = datetime.utcnow() - timedelta(hours=hours)

            query = db.session.query(Tipping, Article.article_name) \
                .join(Article, Tipping.article_id == Article.id) \
                .filter(Tipping.time >= time_threshold) \
                .order_by(Tipping.time.desc()) \
                .limit(limit)

            return [{
                "tipping": c[0].to_dict(),
                "article_title": c[1]
            } for c in query]
        except SQLAlchemyError:
            return []
          
    @staticmethod
    def get_bookshelf_data(user_id, with_article_info=False):
        try:
            query = BookShelf.query.filter_by(user_id=user_id)
            
            if with_article_info:
                query = query.join(Article, BookShelf.article_id == Article.id)
                query = query.add_columns(
                    Article.article_name,
                    Article.author_id,
                    Article.latest_update_time
                )
            
            return query.all()
        except SQLAlchemyError:
            return -2
        
    @staticmethod
    def get_chapter_data(chapter_id=None, article_id=None):
        try:
            if chapter_id:
                return Chapter.query.get(chapter_id)
            if article_id:
                return Chapter.query.filter_by(article_id=article_id).all()
            return None
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def get_articles_by_category(category_id=None, category_name=None, limit=20, offset=0):
        try:
            if not category_id and category_name:
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    return []
                category_id = category.id

            query = Article.query.filter_by(is_published=True)
            if category_id:
                query = query.filter_by(cat_id=category_id)

            articles = query.order_by(
                Article.latest_update_time.desc()
            ).limit(limit).offset(offset).all()
            
            return articles
        except SQLAlchemyError:
            return -2
            
    @staticmethod
    def get_category_hot_list(limit=10):
        try:
            return Category.query.join(Article).group_by(Category.id)\
                .order_by(db.func.count(Article.id).desc()).limit(limit).all()
        except SQLAlchemyError:
            return []

    @staticmethod
    def get_article_statistics(article_id):
        try:
            article: Article = Article.query.get(article_id)
            if not article:
                return None
                
            return {
                'id':article.id,
                'title':article.article_name,
                'author':article.author.username,
                'category':article.category.name,
                'updateTime':article.latest_update_chapter_name,
                'description':article.intro,
                #'views': article.views,
                'likes': article.likes,
                'status': article.status,
                #'comments': Comment.query.filter_by(article_id=article_id).count(),
                'favoritesCount': BookShelf.query.filter_by(article_id=article_id).count(),
                'tipsCount':sum(tipping.amount for tipping in article.tippings)
            }
        except SQLAlchemyError:
            return None
        
    @staticmethod
    def get_reading_history(user_id):
        try:
            return ReadingRecord.query.filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            return -1

    @staticmethod
    def add_to_bookshelf(user_id, article_id):
        try:
            article = Article.query.get(article_id)
            if not article:
                return None, False
            
            existing = BookShelf.query.filter_by(
                user_id=user_id,
                article_id=article_id
            ).first()
            
            if existing:
                return existing, True
            
            new_entry = BookShelf(
                user_id=user_id,
                article_id=article_id,
                article_name=article.article_name
            )
            db.session.add(new_entry)
            db.session.commit()
            return new_entry, False
        except SQLAlchemyError:
            db.session.rollback()
            return None, False

    @staticmethod
    def create_article(author_id, article_data, keywords=None):
        """
        创建文章并关联关键词
        :param author_id: 作者ID
        :param article_data: 文章数据字典
        :param keywords: 关键词列表（如：["星际", "机甲", "热血"]）
        :return: Article实例（失败时返回None）
        """
        try:
            author = db.session.get(User, author_id)
            print(author)
            if not author :#or not author.is_author:
                raise ValueError("无效的作者ID或用户非作者身份")
            print("call create_article")
            now = datetime.utcnow()
            article = Article(
                author_id=author_id,
                create_time=now,
                latest_update_time=now,
                latest_update_chapter_name="未发布章节",
                **article_data
            )
            db.session.add(article)
            db.session.flush()  # 获取article.id

            if keywords:
                for kw_text in set(keywords):
                    keyword = db.session.execute(
                        db.select(KeyWord)
                        .where(KeyWord.keyword == kw_text)
                    ).scalar_one_or_none()

                    if not keyword:
                        keyword = KeyWord(keyword=kw_text)
                        db.session.add(keyword)
                        db.session.flush()  # 获取keyword.id

                    db.session.execute(
                        db.insert(ArticleKeyword)
                        .values(
                            article_id=article.id,
                            keyword_id=keyword.id
                        )
                    )

            creation_list = CreationList(
                author_id=author_id,
                article_id=article.id,
                article_name=article.article_name,
                create_date=now.date(),
                latest_update_time=now.date(),
                latest_update_chapter_name=article.latest_update_chapter_name,
            )
            db.session.add(creation_list)

            db.session.commit()
            return article

        except ValueError as e:
            db.session.rollback()
            print(f"wrong logic: {str(e)}")
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"error database: {str(e)}")
            return None

    @staticmethod
    def update_article(article_id, update_data):
        article = Article.query.get(article_id)
        if not article:
            return None
        
        try:
            for key, value in update_data.items():
                if hasattr(article, key):
                    setattr(article, key, value)
            article.latest_update_time = datetime.utcnow()
            db.session.commit()
            return article
        except SQLAlchemyError:
            db.session.rollback()
            return None
        
    @staticmethod
    def add_article_view(article_id):
        """
        return: bool
        """
        article = Article.query.get(article_id)
        if not article:
            return False
        article.views += 1
        db.session.commit()
        
        return True

    @staticmethod
    def update_chapter(chapter_id, update_data):
        try:
            chapter = Chapter.query.get(chapter_id)
            if not chapter:
                print('yes')
                return None

            allowed_fields = {
                'chapter_name', 'word_count', 
                'text_path', 'is_draft', 'status'
            }
            updates = {k: v for k, v in update_data.items() if k in allowed_fields}

            for key, value in updates.items():
                setattr(chapter, key, value)
            
            article = Article.query.get(chapter.article_id)
            if article:
                article.latest_update_time = datetime.utcnow()
                if 'chapter_name' in updates:
                    article.latest_update_chapter_name = updates['chapter_name']
                
                total_words = db.session.query(
                    db.func.sum(Chapter.word_count)
                ).filter(
                    Chapter.article_id == article.id,
                    Chapter.is_draft == False
                ).scalar() or 0

                article.word_count = total_words
            
            db.session.commit()
            return chapter
        except SQLAlchemyError:
            db.session.rollback()
            return None

    @staticmethod
    def update_reading_progress(user_id, article_id, chapter_id, duration_hours):
        
        try:
            record = ReadingRecord.query.filter_by(
                user_id=user_id,
                article_id=article_id
            ).first()

            if not record:
                article = Article.query.get(article_id)
                if not article:
                    return None
                
                record = ReadingRecord(
                    user_id=user_id,
                    article_id=article_id,
                    article_name=article.article_name,
                    latest_reading_chapter_id=chapter_id,
                    cumulative_reading_time=duration_hours
                )
                db.session.add(record)
            else:
                record.update_reading(chapter_id, duration_hours)
            
            db.session.commit()
            return record
        except SQLAlchemyError:
            db.session.rollback()
            return None

    @staticmethod
    def delete_record(record):
        try:
            db.session.delete(record)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    @staticmethod
    def delete_like(article_id):
        """
        :param article_id: int
        :return: (success: bool, likes: int)
        """
        try:
            article = Article.query.get(article_id)
            if not article:
                return False, 0
            
            if article.likes > 0:
                article.likes -= 1
            else:
                article.likes = 0
            db.session.commit()
            return True, article.likes
        except SQLAlchemyError:
            db.session.rollback()
            return False, 0
        
    @staticmethod
    def delete_book_from_shelf(user_id, article_id):
        """
       delete article data form user's bookshelf
        :return: bool
        """
        try:
            deleted = BookShelf.query.filter_by(
                user_id=user_id,
                article_id=article_id
            ).delete()
            db.session.commit()
            return deleted > 0
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    @staticmethod
    def get_latest_reading(user_id):
        """
        get latest reding record of user
        :return: ReadingRecord or None
        """
        try:
            return ReadingRecord.query.filter_by(
                user_id=user_id
            ).order_by(
                ReadingRecord.latest_reading_time.desc()
            ).first()
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def create_chapter(article_id, chapter_data):
        """
        create chapter with data
        return: bool, chapter
        """
        try:
            chapter = Chapter(
                article_id=article_id,
                chapter_id=chapter_data.get('chapter_id'),
                chapter_name=chapter_data.get('chapter_name'),
                word_count=chapter_data.get('word_count', 0),
                text_path=chapter_data.get('text_path'),
                status=chapter_data.get('status'),
                latest_update_time=datetime.utcnow(),
                is_draft=chapter_data.get('is_draft', False),
            )

            db.session.add(chapter)
            db.session.flush()

            article = db.session.get(Article, article_id)
            
            if not article:
                raise ValueError("No Article")

            article.chapter_number = Article.chapter_number + 1
            article.latest_update_time = datetime.utcnow()
            article.latest_update_chapter_name = chapter.chapter_name

            creation_list = db.session.execute(
                db.select(CreationList)
                .filter_by(article_id=article_id)
            ).scalar_one_or_none()

            if creation_list:
                creation_list.latest_update_time = datetime.utcnow().date()
                creation_list.latest_update_chapter_name = chapter.chapter_name
            else:
                creation_list = CreationList(
                    author_id=article.author_id,
                    article_id=article.id,
                    article_name=article.article_name,
                    create_date=datetime.utcnow().date(),
                    latest_update_time=datetime.utcnow().date(),
                    latest_update_chapter_name=chapter.chapter_name,
                )
                db.session.add(creation_list)
                
            total_words = db.session.query(
                db.func.sum(Chapter.word_count)
            ).filter(
                Chapter.article_id == article.id,
                Chapter.is_draft == False  # 只统计非草稿章节
            ).scalar() or 0

            article.word_count = total_words

            db.session.commit()
            return True, chapter

        except ValueError as e:
            db.session.rollback()
            print(f"Logical Error: {str(e)}")
            return False, None
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database Error: {str(e)}")
            return False, None
        
    @staticmethod
    def delete_article(article_id):
        """
        delete article
        :return: bool
        """
        try:
            deleted = Article.query.filter_by(id=article_id).delete()
            db.session.commit()
            return deleted > 0
        except SQLAlchemyError:
            db.session.rollback()
            return False
    
    @staticmethod
    def delete_chapter(chapter_id):
        """
        delet chapter and update data
        Return: bool
        """
        try:
            chapter = db.session.get(Chapter, chapter_id)
            if not chapter:
                return False

            article_id = chapter.article_id
            chapter_name = chapter.chapter_name

            db.session.delete(chapter)

            article = db.session.get(Article, article_id)
            if article:
                remaining_chapters = Chapter.query.filter_by(
                    article_id=article_id
                ).count()
                
                article.chapter_number = remaining_chapters
                article.latest_update_time = datetime.utcnow()

                if article.latest_update_chapter_name == chapter_name:
                    latest_chapter = Chapter.query.filter_by(
                        article_id=article_id
                    ).order_by(
                        Chapter.latest_update_time.desc()
                    ).first()
                    
                    article.latest_update_chapter_name = (
                        latest_chapter.chapter_name if latest_chapter 
                        else f"has deleted: {chapter_name}"
                    )
                    
                total_words = db.session.query(
                    db.func.sum(Chapter.word_count)
                ).filter(
                    Chapter.article_id == article.id,
                    Chapter.is_draft == False  # 只统计非草稿章节
                ).scalar() or 0

                article.word_count = total_words

            creation_list = db.session.execute(
                db.select(CreationList)
                .filter_by(article_id=article_id)
            ).scalar_one_or_none()

            if creation_list:
                creation_list.latest_update_time = datetime.utcnow().date()
                creation_list.latest_update_chapter_name = (
                    article.latest_update_chapter_name 
                    if article 
                    else f"has deleted: {chapter_name}"
                )

            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"delete error: {str(e)}")
            return False
    
    
    @staticmethod
    def keytag_list(search_keyword, limit=5):
        """
        get list of keyward
        :param search_keyword: str
        :param limit: int
        :return: List[dict]: 
            [{
                "keyword": "星际", 
                "is_hot": True,
                "usage_count": 15
            }]
        """
        try:
            keywords = db.session.query(
                KeyWord,
                db.func.count(ArticleKeyword.keyword_id).label('usage_count')
            ).outerjoin(
                ArticleKeyword,
                KeyWord.id == ArticleKeyword.keyword_id
            ).filter(
                db.or_(
                    KeyWord.is_hot == True,
                    KeyWord.keyword.contains(search_keyword)
                )
            ).group_by(
                KeyWord.id
            ).order_by(
                db.func.count(ArticleKeyword.keyword_id).desc() 
            ).limit(limit).all()

            return [{
                "keyword": kw.keyword,
                "is_hot": kw.is_hot,
                "usage_count": usage_count or 0
            } for kw, usage_count in keywords]
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def search_books(key_word, page=1, page_size=10, search_by_keyword=False):
        """
        :param key_word: str
        :param search_by_keyword: bool
        :return: (articles, total, current_page, total_pages)
        """
        try:
            if search_by_keyword:
                query = Article.query.join(
                    ArticleKeyword
                ).join(
                    KeyWord
                ).filter(
                    KeyWord.keyword.contains(key_word)
                ).order_by(
                    Article.latest_update_time.desc()
                )
            else:
                query = Article.query.filter(
                    db.or_(
                        Article.article_name.contains(key_word),
                        Article.intro.contains(key_word)
                    )
                )

            pagination = query.paginate(
                page=page,
                per_page=page_size,
                error_out=False
            )
            
            return (
                pagination.items,
                pagination.total,
                pagination.page,
                pagination.pages
            )
        except SQLAlchemyError:
            return [], 0, 1, 1
    
    @staticmethod
    def recommend_hot_articles(limit=5):
        """
        return: List[Article]
        """
        try:
            return Article.query.order_by(
                (Article.views * 0.7 + Article.likes * 0.3).desc()
            ).limit(limit).all()
        except SQLAlchemyError:
            return []
        
    @staticmethod
    def get_article_chapter_summary(article_id):
        """
        get all chapter summary of a book, e.g. ID and title
        :param article_id: int
        :return: List[dict] [{"id": 1, "title": "第一章"}, ...]
        """
        chapters = Chapter.query.filter_by(article_id=article_id).order_by(Chapter.id.asc()).all()
        return [{"id": chapter.id, "title": chapter.chapter_name} for chapter in chapters ]
      
    
    def get_author_articles(author_id):
        """
        Return informations of all books under author
        id、title、cover、intro、status、likes、commentCount
        
        input:
            author_id: int
        return:
            article_data: dict
        """
        articles = Article.query.filter_by(author_id=author_id).all()
        
        result = []
        for article in articles:
            comment_count = Comment.query.filter_by(article_id=article.id).count()
            
            article_data = {
                'id': article.id,
                'title': article.article_name,
                'cover': None,
                'intro': article.intro,
                'status': article.status,
                'likes': article.likes,
                'commentsCount': comment_count
            }
            result.append(article_data)
        
        return result
    
    def user_like_article(user_id, article_id):
        """
        Checkout whether user like the article
        input:
            user_id: int
            article_id: int
        return:
            result: bool
        """
        like = Like.query.filter_by(user_id=user_id, article_id=article_id).first()
        return like is not None
    
    
    def user_create_like(user_id, article_id):
        """
        User like operation
        input:
            user_id: int
            article_id: int
        return:
            result: bool
        """
        try:
            if DBOperations.user_like_article(user_id, article_id):
                article = Article.query.get(article_id)
                return False
            
            article = Article.query.get(article_id)
            if not article:
                return False
            
            new_like = Like(user_id=user_id, article_id=article_id)
            db.session.add(new_like)
            
            article.likes += 1
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            return False
        
    def user_cancel_like_article(user_id, article_id):
        """
        User unlike operation
        input:
            user_id: int
            article_id: int
        return:
            result: bool
        """
        try:
            like = Like.query.filter_by(user_id=user_id, article_id=article_id).first()
            if not like:
                article = Article.query.get(article_id)
                return False
            
            article = Article.query.get(article_id)
            if not article:
                return False
            
            db.session.delete(like)
            
            article.likes = max(0, article.likes - 1)
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            return False
        
    def get_user_balance(user_id):
        result = db.session.query(User.balance).filter(User.id == user_id).scalar()
        return result if result is not None else 0