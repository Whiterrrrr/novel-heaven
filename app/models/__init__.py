from .base import db
from .user import *
from .book import *
from .other import *
from datetime import *
from sqlalchemy.exc import SQLAlchemyError

class DBOperations:
    @staticmethod
    def update_user_role(user_id, new_role):
        """
        更新用户角色（管理员操作）
        :param user_id: 目标用户ID
        :param new_role: 新角色
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
        删除用户（管理员操作）
        :param user_id: 目标用户ID
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
    def register_new_user(username, email, password):
        """
        注册新用户
        :param username: 用户名
        :param email: 邮箱
        :param password: 明文密码
        :return: (success: bool, user: User | None, message: str)
        """
        try:
            if User.query.filter_by(username=username).first():
                return False, None, "用户名已被使用"
            if User.query.filter_by(email=email).first():
                return False, None, "邮箱已被注册"

            user = User(username=username, email=email)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            return True, user, "注册成功"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, None, f"注册失败: {str(e)}"

    @staticmethod
    def update_user_settings(user_id, update_data):
        """
        更新用户设置
        :param user_id: 用户ID
        :param update_data: 更新数据字典
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
                    return False, "用户名已被使用"

            if 'email' in update_data:
                if User.query.filter(
                    User.email == update_data['email'],
                    User.id != user_id
                ).first():
                    return False, "邮箱已被注册"

            allowed_fields = {'username', 'email', 'bio', 'password'}
            for field, value in update_data.items():
                if field in allowed_fields:
                    if field == 'password':
                        user.set_password(value)
                    else:
                        setattr(user, field, value)

            db.session.commit()
            return True, "设置更新成功"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"更新失败: {str(e)}"
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def authenticate_user(email, password, remember=False):
        """
        验证用户登录凭证
        :param email: 用户邮箱
        :param password: 明文密码
        :param remember: 是否记住登录状态
        :return: (success: bool, user: User | None, message: str)
        """
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                return False, None, "用户不存在"
            
            if not user.check_password(password):
                return False, None, "密码错误"
            
            user.last_seen = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=remember)
            return True, user, "登录成功"
        except SQLAlchemyError:
            db.session.rollback()
            return False, None, "数据库错误"

    @staticmethod
    def check_and_reward_daily_login(user):
        """
        检查并发放每日登录奖励
        :param user: 用户对象
        :return: (reward_given: bool, amount: int)
        """
        try:
            if user.last_seen.date() == date.today():
                return False, 0
            
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
    def create_user(username, email, password, gender=None):
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return None
        
        new_user = User(
            username=username,
            email=email,
            gender=gender,
            joined_at=datetime.utcnow(),
            last_seen=datetime.utcnow()
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError:
            db.session.rollback()
            return None

    @staticmethod
    def update_user_profile(user_id, **kwargs):
        allowed_fields = {'username', 'email', 'gender', 'balance', 'is_author'}
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        user = User.query.get(user_id)
        if not user:
            return None
        
        try:
            for key, value in updates.items():
                setattr(user, key, value)
            user.last_seen = datetime.utcnow()
            db.session.commit()
            return user
        except SQLAlchemyError:
            db.session.rollback()
            return None

    
    
    
    
    @staticmethod
    def get_latest_articles(limit=1):
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
            article = Article.query.get(article_id)
            if not article:
                return None
                
            return {
                'views': article.views,
                'likes': article.likes,
                'comments': Comment.query.filter_by(article_id=article_id).count(),
                'bookmarks': BookShelf.query.filter_by(article_id=article_id).count()
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
    def create_article(author_id, article_data):
        try:
            article = Article(
                author_id=author_id,
                **article_data,
                create_time=datetime.utcnow(),
                latest_update_time=datetime.utcnow()
            )
            db.session.add(article)
            db.session.flush()
            
            creation_list = CreationList(
                author_id=author_id,
                article_id=article.id,
                article_name=article.article_name,
                create_date=datetime.utcnow().date(),
                latest_update_time=datetime.utcnow().date()
            )
            db.session.add(creation_list)
            
            db.session.commit()
            return article
        except SQLAlchemyError:
            db.session.rollback()
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
    def update_chapter(chapter_id, update_data):
        try:
            chapter = Chapter.query.get(chapter_id)
            if not chapter:
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
    def create_comment(user_id, article_id, content):
        try:
            new_comment = Comment(
                user_id=user_id,
                article_id=article_id,
                context=content,
                time=datetime.utcnow()
            )
            db.session.add(new_comment)
            db.session.commit()
            return new_comment
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
    def make_like(article_id):
        pass
    @staticmethod
    def delete_book_from_shelf(user_id, article_id):
        pass
    
    @staticmethod
    def get_latest_reading(user_id):
        pass
    
    @staticmethod
    def create_chapter(chapter_id, chapter_data):
        pass
    
    @staticmethod
    def delete_article(article_id)-> bool:
        pass
    
    @staticmethod
    def delete_chapter(chapter_id)-> bool: 
        pass
    
    @staticmethod
    def keytag_list(search_keyword, limit) -> list[KeyWord]:
        """
        keytag包含两类，一类是本身就是hot，一类是tag中包含search_keyword
        我感觉大致是这样子写： keytags = KeyWord.query.filter(or_(KeyWord.is_hot == True, KeyWord.keyword.contains(search_word))).limit(5)
        """
        pass
    
    @staticmethod
    def search_books(key_word,page,page_size):
        """
        返回值：list(Article), article_counts, current_page, total_pages
        """
        pass
    
    @staticmethod
    def recommend_hot_articles(limit=5):
        """按热度推荐（阅读量+点赞量加权）
        我感觉大致是这样子写：return Article.query.order_by((Article.views * 0.7 + Article.likes * 0.3).desc()).limit(limit).all()
        
        """