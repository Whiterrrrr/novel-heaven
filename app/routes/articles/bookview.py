from flask import Blueprint, request, jsonify
from . import articles_bp
from app.models import DBOperations
from flask_login import login_required

class ViewManager():
    def __init__(self, data):
        self.data = data
    
    def show_article_stat(self):
        try:
            article_id = self.data['article_id']
        except :
            return -1
        
        return DBOperations.get_article_statistics(article_id)
    
    def get_article_data(self):
        try:
            article_id = self.data['article_id']
        except :
            return -1
        
        return DBOperations.get_chapter_data(article_id=article_id)
       
    def get_chapter_data(self):
        try:
            chapter_id = self.data['chapter_id']
        except :
            return -1
        
        return DBOperations.get_chapter_data(chapter_id = chapter_id) 
    
@articles_bp.route("/bookview/article_stat")
@login_required
def get_article_stat():
    data = request.get_json()
    manager = ViewManager(data)
    
    stat = manager.show_article_stat()
    
    if not stat:
        return jsonify(msg = 'No such article'), 404
    elif stat == -1:
        return jsonify(msg = 'Non valid article id')
    else:
        return stat
    
@articles_bp.route("/bookview/article")
@login_required
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
    
@articles_bp.route("/bookview/article/chapter")
@login_required
def get_chapter_data():
    data = request.get_json()
    manager = ViewManager(data)
    
    chapter = manager.get_chapter_data()
    
    if not chapter:
        return jsonify(msg = 'Error')
    elif chapter == -1:
        return jsonify(msg = 'Non valid chapter_id')
    else:
        return jsonify(chapter.to_dict())