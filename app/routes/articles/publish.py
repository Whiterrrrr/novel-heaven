from app.models import *
from . import articles_bp
# from forms import ArticleForm, ChapterForm
from flask_login import login_required, current_user
from flask import render_template, request, jsonify
import datetime
from abc import ABC, abstractmethod

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
    
    
class PublishChapter(PublishManager):
    def __init__(self,data):
        super().__init__(data)
        
    def create(self):
        try:
            chapter_id = self.data['chapter_id']
            chapter_data = self.data['chapter_data']
        except:
            return -1
        
        return DBOperations.create_chapter(chapter_id, chapter_data)
    
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
    
    
          
@articles_bp.route("/publish/article/update", methods= ['POST'])
def update_article():
    data = request.get_json()
    manager = PublishArticle(data)
    
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
    
@articles_bp.route("/publish/article/create", methods=['POST'])
def create_new_article():
    data = request.get_json()
    manager = PublishArticle(data)
    
    new_article = manager.create()
    
    if not new_article:
        return jsonify(msg = 'Error')
    elif new_article == -1:
        return jsonify(msg = 'Non valid input')
    else:
        return jsonify({
            "novel_id": new_article.id,
            "edit_url": f"/editor/article/{new_article.id}" # 跳转到编辑页面，需要editor.html
        })

@articles_bp.route("/delete/article", methods=['POST'])
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
    
    
@articles_bp.route("/publish/chapter/create", methods=['POST'])
@login_required
def create_chapter():
    data = request.get_json() 
    manager = PublishChapter(data)
    
    """
    form = ChapterForm(data={
        'chapter_title': data.get('chapter_title'),
        'content': data.get('content')
    })
    
    if form.validate() and article_id:
    """
    new_chapter = manager.create()
    
    if not new_chapter:
        return jsonify(msg = 'Error')
    elif new_chapter == -1:
        return jsonify(msg = 'Non valid input')
    else:
        return jsonify({
            "novel_id": new_chapter.id,
            "edit_url": f"/editor/chapter/{new_chapter.id}" # 跳转到编辑页面，需要editor.html
        })
        
@articles_bp.route("/publish/chapter/update", methods= ['POST'])
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
    
@articles_bp.route("/delete/chapter", methods=['POST'])
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
    

@articles_bp.route("/editor/article/<int:article_id>")
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

@articles_bp.route("/editor/chapter/<int:chapter_id>")
@login_required
def chapter_editor(chapter_id):
    
    chapter = Chapter.query.filter_by(chapter_id=chapter_id)
    
    return render_template('editor_chapter.html', 
        chapter=chapter
    )
    
