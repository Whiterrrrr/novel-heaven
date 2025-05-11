from flask import Blueprint, request, jsonify
from . import articles_bp
from app.models import DBOperations
from flask_login import login_required, current_user

class ViewManager():
    def __init__(self, data):
        self.data = data
    
    def show_article_stat(self):
        try:
            article_id = self.data['article_id']
            user_id = self.data['user_id']
        except :
            return -1,-1
        
        is_liked = DBOperations.user_like_article(user_id, article_id)
        result = DBOperations.get_article_statistics(article_id)
        return (is_liked, result)
    
    def show_article_chapter_stat(self):
        try:
            article_id = self.data['article_id']
        except :
            return -1
        
        return DBOperations.get_article_chapter_summary(article_id)
    
    def get_article_data(self):
        try:
            article_id = self.data['article_id']
        except :
            return -1
        
        return DBOperations.get_chapter_data(article_id=article_id)
       
        
@articles_bp.route("/bookview/<int:novel_id>")
@login_required
def get_article_stat(novel_id):
    data = {'article_id':novel_id,'user_id':current_user.id}
    manager = ViewManager(data)
    
    is_liked, stat = manager.show_article_stat()
    
    article_name= stat['title']
    author = stat['author']
    
    img_path = stat['author']+'/'+stat['title']+'/img.jpg'
    stat['cover_url'] = img_path
    stat['likedByMe'] = is_liked
    if not stat:
        return jsonify(msg = 'No such article'), 404
    elif stat == -1:
        return jsonify(msg = 'Non valid article id')
    else:
        return stat
    
@articles_bp.route("/bookview/article")
# @login_required
def get_article_data():
    data = request.get_json()
    manager = ViewManager(data)
    
    chapters = manager.get_article_data()
    chapters = [chapter.to_dict() for chapter in chapters]
    
    if not chapters:
        return jsonify(msg = 'Error')
    elif chapters == -1:
        return jsonify(msg = 'Non valid article_id')
    else:
        return jsonify(chapters)
    
@articles_bp.route("/<int:novel_id>/chapters/<int:chapter_id>/content",methods=['GET'])
#@articles_bp.route("/chapters")
# @login_required
def get_chapter_data(novel_id, chapter_id):
    print(chapter_id)
    data = {'article_id':novel_id}
    manager = ViewManager(data)
    
    chapter_list = manager.get_article_data()
    if chapter_id > len(chapter_list):
        return jsonify(msg = 'Non valid chapter_id')
    chapter = chapter_list[chapter_id-1]
    path = chapter.text_path
    
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    result = {
        'id':chapter.id,
        'title':chapter.chapter_name,
        'content':content
    }    
    
    if not chapter:
        return jsonify(msg = 'Error')
    elif chapter == -1:
        return jsonify(msg = 'Non valid chapter_id')
    else:
        return jsonify(result)


@articles_bp.route("/<int:novel_id>/chapters")
def get_chapter_stat(novel_id):
    data = {'article_id':novel_id}
    manager = ViewManager(data)
    
    stat = manager.show_article_chapter_stat()
    
    if not stat:
        return jsonify(msg = 'No such article'), 404
    elif stat == -1:
        return jsonify(msg = 'Non valid article id')
    else:
        return stat