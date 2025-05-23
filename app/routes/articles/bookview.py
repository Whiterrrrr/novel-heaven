from flask import Blueprint, request, jsonify
from . import articles_bp
from app.models import DBOperations, Chapter
from flask_login import login_required, current_user

from ... import User


class ViewManager():
    def __init__(self, data: dict):
        self.data = data
    
    def show_article_stat(self):
        try:
            article_id = self.data['article_id']
        except :
            return -1,-1
        result = DBOperations.get_article_statistics(article_id)
        if 'user_id' in self.data.keys():
            user_id = self.data['user_id']
            is_liked = DBOperations.user_like_article(user_id, article_id)
            return (is_liked, result)
        else:
            return (False, result)
    
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
# @login_required
def get_article_stat(novel_id):
    """
    Get detailed statistics of a novel.

    Args:
        novel_id (int): Novel's unique id.

    Returns:
        dict or JSON response:
            - Article stats if successful.
            - 404 JSON if article not found.
            - Error message if invalid ID.

    Features:
        - Fetch basic article info and cover image path.
        - Check if current user liked or favorited it.
        - If logged in, include user balance and bookshelf.
    
    """
    data = {'article_id':novel_id}
    if current_user.is_authenticated:
        data['user_id'] = current_user.id
    manager = ViewManager(data)
    
    is_liked, stat = manager.show_article_stat()

    img_path = stat['author']+'/'+stat['title']+'/img.jpg'
    stat['cover_url'] = img_path
    stat['likedByMe'] = is_liked
    if current_user.is_authenticated:
        myBalance =  DBOperations.get_user_balance(current_user.id)
        stat['myBalance'] = myBalance
        user = User.query.filter_by(id=current_user.id).first()
        bookshelf = DBOperations.get_bookshelf_data(user.id)
        bookshelf = [book.article_id for book in bookshelf]
        stat['favoritedByMe'] = novel_id in bookshelf
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
    """
    Get the content and information of a specific chapter by novel_id and chapter_id.

    Args:
        novel_id (int): The ID of the novel.
        chapter_id (int): The ID of the chapter.

    Returns:
        JSON response:
            - Chapter details and text content if found.
            - 400 JSON message if chapter_id is invalid.
            - Error message if chapter retrieval fails.

    Function:
        - Fetch chapter info from the database.
        - If user is logged in, update reading progress.
        - Read chapter content from text file.
        - Return chapter ID, title, and content.
    """
    
    print(chapter_id)
    data = {'article_id':novel_id}
    manager = ViewManager(data)
    selected_chapter = Chapter.query.filter_by(article_id=novel_id, chapter_id=chapter_id).first()
    print(selected_chapter)
    if selected_chapter is None:
        return jsonify(msg = 'Non valid chapter_id'), 400
    path = selected_chapter.text_path
    if current_user.is_authenticated:
        DBOperations.update_reading_progress(current_user.id, novel_id, selected_chapter.id, 0.0)
    
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    result = {
        'id':selected_chapter.id,
        'title':selected_chapter.chapter_name,
        'content':content
    }    
    
    if not selected_chapter:
        return jsonify(msg = 'Error')
    elif selected_chapter == -1:
        return jsonify(msg = 'Non valid chapter_id')
    else:
        return jsonify(result)


@articles_bp.route("/<int:novel_id>/chapters")
def get_chapter_stat(novel_id):
    """
    Get statistics of all chapters' summary for a novel.

    Args:
        novel_id (int): The ID of the novel.

    Returns:
        JSON response:
            - Chapter statistics if found.
            - 404 JSON message if novel not found.
            - Error message if novel ID is invalid.

    """
    data = {'article_id':novel_id}
    manager = ViewManager(data)
    
    stat = manager.show_article_chapter_stat()
    # print(stat)
    if not stat:
        return jsonify(msg = 'No such article'), 404
    elif stat == -1:
        return jsonify(msg = 'Non valid article id')
    else:
        return stat