from app.models import *
from . import author_bp
# from forms import ArticleForm, ChapterForm
from flask_login import login_required, current_user
from flask import render_template, request, jsonify
import datetime
from abc import ABC, abstractmethod
import os
import app
from datetime import datetime


def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'jpg' 
    
class PublishManager(ABC):
    def __init__(self, data):
        self.data = data
        
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass
    
    
    
class PublishArticle(PublishManager):
    def __init__(self,data):
        super().__init__(data)
        
    def create(self):
        try:
            author_id = self.data['author_id']
            article_data = self.data['article_data']
        except:
            return -1
        print(f'author id is {author_id}')
        return DBOperations.create_article(author_id, article_data)
    
    def update(self):
        """
        try:
            form = ArticleForm(data={
            'title': self.data.get('article_title'),
            'category': self.data.get('category')
        })
        """
        try:
            article_id = self.data.get('article_id')
            update_data = self.data.get('update_data')
        except:
            return -1
        
        return DBOperations.update_article(article_id, update_data)
    
    def delete(self):
        try:
            article_id = self.data.get('article_id')
        except:
            return -1
        
        return DBOperations.delete_article(article_id)
    
    def show(self):
        try:
            user_id = self.data.get('user_id')
        except:
            return -1
        
        return DBOperations.get_author_articles(user_id)
    
class PublishChapter(PublishManager):
    def __init__(self,data):
        super().__init__(data)
        
    def create(self):
        try:
            article_id = self.data['article_id']
            chapter_data = self.data['chapter_data']
        except:
            return -1
        
        return DBOperations.create_chapter(article_id, chapter_data)
    
    def update(self):
        try:
            chapter_id = self.data.get('article_id')
            update_data = self.data.get('update_data')
        except:
            return -1
        
        return DBOperations.update_chapter(chapter_id, update_data)
    
    def delete(self):
        try:
            chapter_id = self.data.get('chapter_id')
        except:
            return -1
        
        return DBOperations.delete_chapter(chapter_id)      
    
    
          
@author_bp.route("/works/<int:article_id>/status", methods= ['PUT'])
def update_article(article_id):
    recv = request.get_json()
    data = {}
    data['article_id'] = article_id
    data['update_data'] = recv['update_content']
    manager = PublishArticle(data)
    
    article = manager.update()
    
    if not article:
        return jsonify(msg = 'Article is not exist'), 404
    elif article == -1:
        return jsonify(msg = 'No valid input')
    
    return jsonify({
        "msg": "Successfully updated",
        "published_at": article.latest_update_time.isoformat()
       # "article_url": f"/articles/{article.id}"  # 文章打开详情页的路径
    })
    
@author_bp.route("/works", methods=['POST','GET'])
@login_required
def create_new_article():
    if request.method == 'POST':
        article_data = {}
        
        article_data['article_name'] = request.form.get('title')
        article_data['intro'] = request.form.get('synopsis')
        article_data['cat_id'] = 2# request.form.get('category')
        file = request.files['cover']

        # 如果文件符合要求，进行保存
        if file and allowed_file(file.filename):
            authorname = User.query.get(current_user.id).username

            cover_dir = os.path.join('book_sample', authorname, article_data['article_name'])
            os.makedirs(cover_dir, exist_ok=True)  

            cover_path = os.path.join(cover_dir, 'img.jpg')
            file.save(cover_path)
        
            
        data = {
            'author_id':current_user.id,
            'article_data':article_data
        }
            
        
        manager = PublishArticle(data)
        
        new_article = manager.create()
        
        if not new_article:
            return jsonify(msg = 'Error')
        elif new_article == -1:
            return jsonify(msg = 'Non valid input')
        else:
            return jsonify({
                "novel_id": new_article.id,
                "message":"Novel published successfully!"
            })
    else:
        
        #print(current_user.id)
        data = {'user_id':current_user.id}
        #data = {'user_id':6}
        manager = PublishArticle(data)
        books = manager.show()
        authorname = User.query.get(current_user.id).username
        for book in books:
            book['cover'] = f"{authorname}/{book['title']}/img.jpg"
        
        return jsonify(books)
        

@author_bp.route("/delete/article", methods=['POST'])
#@login_required
def delete_article():
    data = request.get_json()
    manager = PublishArticle(data)
    
    status = manager.delete()
    
    if status == -1:
        return jsonify(msg = 'Non valid article_id')
    elif not status:
        return jsonify(msg = 'Article chosen to delete is not exist'), 400
    else:
        return jsonify(msg = 'Successfully delete')
    
    
@author_bp.route("/works/<int:article_id>/chapters", methods=['POST'])
@login_required
def create_chapter(article_id):
    recv = request.get_json() 
    print(recv)
    data = {}
    chapter_data = {}
    
    content = recv['content']
    word_count = len(content)
    user = User.query.filter_by(id=current_user.id).first().username
    
    article = Article.query.get(article_id)
    if article:
        article_name = article.to_dict()['title'] 
    text_path = os.path.join('book_sample', user, article_name, 'chapter', f"{recv['title']}.txt")

    os.makedirs(os.path.dirname(text_path), exist_ok=True)  

    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    chapter_data['chapter_name'] = recv['title']
    chapter_data['text_path'] = text_path
    chapter_data['status'] = recv['status']
    chapter_data['is_draft'] = False #recv['is_draft']
    print(recv['is_draft'])
    chapter_data['word_count'] = word_count
    data['chapter_data'] = chapter_data
    data['article_id'] = article_id
    manager = PublishChapter(data)


    status, new_chapter = manager.create()
    
    if not new_chapter:
        return jsonify(msg = 'Error')
    elif new_chapter == -1:
        return jsonify(msg = 'Non valid input')
    else:
        return jsonify({
            "novel_id": new_chapter.id,
            
        })
        
@author_bp.route("/publish/chapter/update", methods= ['POST'])
def update_chapter():
    data = request.get_json()
    manager = PublishChapter(data)
    
    article = manager.update()
    
    if not article:
        return jsonify(msg = 'Article is not exist'), 404
    elif article == -1:
        return jsonify(msg = 'No valid input')
    
    return jsonify({
        "msg": "Successfully update",
        "published_at": article.latest_update_time.isoformat()
       # "article_url": f"/articles/{article.id}"  # 文章打开详情页的路径
    })
    
@author_bp.route("/delete/chapter", methods=['POST'])
@login_required
def delete_chapter():
    data = request.get_json()
    manager = PublishChapter(data)
    
    status = manager.delete()
    
    if status == -1:
        return jsonify(msg = 'Non valid chapter_id')
    elif not status:
        return jsonify(msg = 'Chapter chosen to delete is not exist'), 400
    else:
        return jsonify(msg = 'Successfully delete')
    
"""
@author_bp.route("/editor/article/<int:article_id>")
@login_required
def article_editor(article_id):

    article = Article.query.filter_by(
        id=article_id,
        user_id=current_user.id
    ).first_or_404()
    
    chapters = Chapter.query.filter_by(article_id=article_id).order_by(Chapter.order).all()
    
    return render_template('editor.html', 
        article=article,
        chapters=chapters
    )

@author_bp.route("/editor/chapter/<int:chapter_id>")
@login_required
def chapter_editor(chapter_id):
    
    chapter = Chapter.query.filter_by(chapter_id=chapter_id)
    
    return render_template('editor_chapter.html', 
        chapter=chapter
    )
    """

@author_bp.route("/me")
@login_required
def author_info():
    user = User.query.get(current_user.id)
    result = {
        'authorName':user.username,
        'coins':user.balance
    }
    print(user.username)
    return jsonify(result)

@author_bp.route("/comments")
@login_required
def fetch_comment():
    limit = request.args.get("limit", 5)
    user_id = current_user.id
    
    books = DBOperations.get_author_articles(user_id)
    book_id = [book['id'] for book in books]
    
    comment = []
    for id in book_id:
        comment.append(DBOperations.get_article_comments(id,include_user_info=True)[0])
        
    flattened_data = [item for sublist in comment for item in sublist]

    # 按时间降序排序
    sorted_data = sorted(
        flattened_data,
        key=lambda x: datetime.fromisoformat(x['time']),
        reverse=True
    )

    data = sorted_data[:limit] if len(sorted_data)>=int(limit) else sorted_data
    result = []
    for comment in data:
        result.append({
            'content':comment["content"],
            'date': comment["time"][:10],
            'reader': comment["user"]["username"]
        })
    
    # print(result)
    return jsonify(result)

@author_bp.route("/works/overview/<int:article_id>")
@login_required 
def show_article(article_id):
    result = {}
    origin = DBOperations.get_article_statistics(article_id)
    chapters = DBOperations.get_article_chapter_summary(article_id)
    
    comments, _ = DBOperations.get_article_comments(article_id, include_user_info=True)
    result['title'] = origin['title']
    result['status'] = origin['status']
    result['comments'] = []
    
    for comment in comments:
        result['comments'].append({'user':comment['user']['username'], 'content':comment['content']})
    
    result['chapters'] = chapters
    
    return jsonify(result)
    