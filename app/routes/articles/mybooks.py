from flask import Blueprint, request, jsonify
from . import articles_bp
from app.models import DBOperations
from flask_login import login_required, current_user


class BookManager():
    def __init__(self, data):
        self.data = data
    
    def get_bookshelf_data(self):
        try:
            user_id = self.data['user_id']
        except :
            return -1
        
        with_article_info = self.data['with_article_info'] if 'with_article_info' in self.data.keys() else False
        
        query = DBOperations.get_bookshelf_data(user_id, with_article_info)
        if with_article_info:
            return [
                {
                    "bookshelf": book_shelf.to_dict(),
                    "article_name": article_name,
                    "author_id": author_id,
                    "latest_update_time": latest_update_time.isoformat()
                }
                for book_shelf, article_name, author_id, latest_update_time in query
            ]
        else:
            return [book_shelf.to_dict() for book_shelf in query]

    """
    def add_to_bookshelf(self):
        try:
            user_id = self.data['user_id']
            article_id = self.data['article_id']
        except :
            return -1
        
        new_entry, exist = DBOperations.add_to_bookshelf(user_id, article_id)
        
        if exist:
            return 1
        else:
            return new_entry
        
    def delete_book_from_shelf(self):
        try:
            user_id = self.data['user_id']
            article_id = self.data['article_id']
        except :
            return -1
        
        return DBOperations.delete_book_from_shelf(user_id, article_id)
    """
    
    def handle_favorite(self):
        try:
            user_id = self.data['user_id']
            status = self.data['favorite']
            article_id = self.data['article_id']
        except :
            return -1
        
        if status:
            _, exist = DBOperations.add_to_bookshelf(user_id, article_id)
            if exist:
                return 2
            else:
                return True
        else:
            return DBOperations.delete_book_from_shelf(user_id, article_id)
        
    def get_last_reading_history(self):
        try:
            user_id = self.data['user_id']
        except :
            return -1
        
        query = DBOperations.get_latest_reading(user_id)
        
        if query == -1:
            return -1
        else:
            return  query.to_dict()
        
    def get_reading_history(self):
        try:
            user_id = self.data['user_id']
        except :
            return -1
        
        query = DBOperations.get_reading_history(user_id)
        
        if query == -1:
            return -1
        else:
            return [record.to_dict() for record in query]
    
@articles_bp.route("/mybookshelf",methods=['GET'])
@login_required
def mybooks_list():
    data = request.get_json()
    manager = BookManager(data)

    result = manager.get_bookshelf_data()
    if result == -1:
        return jsonify(msg = 'Non valid user id')
    elif result == -2:
        return jsonify(msg = 'Fail operation')
    elif result == []:
        return jsonify(msg = 'Zero book')
    else:
        return jsonify(result)

@articles_bp.route("/<int:novel_id>/favorite", methods=['POST'])
@login_required
def handle_favorite(novel_id): 
    data = request.get_json()
    data['article_id'] = novel_id
    #data['user_id'] = current_user.id
    manager = BookManager(data)
    
    status = manager.handle_favorite()
    
    if status== 2:
        return jsonify(msg='Target book has been in your personal shelf')
    elif status == False:
        return jsonify(msg='Error')
    else:
        return jsonify(msg = 'Successful')
    
"""  
@articles_bp.route("/<int:novel_id/favorite", methods=['POST'])
#@login_required
def add_book_to_shelf(novel_id): 
    data = request.get_json()
    #data['user_id'] = current_user.id
    
    manager = BookManager(data)
    
    book_select = manager.add_to_bookshelf()
    
    if not book_select:
        return jsonify(msg='Target book is not found'), 404
    elif book_select == -1:
        return jsonify(msg = 'Non valid')
    elif book_select == 1:
        return jsonify(msg='Target book has been in your personal shelf'), 400
    else:
        return jsonify(msg = 'Successfully add')
    


@articles_bp.route("/mybookshelf/delete", methods=['DELETE'])
@login_required
def delete_book_from_shelf():
    data = request.get_json()
    manager = BookManager(data)
    
    status = manager.delete_book_from_shelf()
    
    if not status:
        return jsonify(msg = 'Book chosen to delete is not in your personal shelf'), 400
    else:
        return jsonify(msg = 'Successfully delete')
"""

@articles_bp.route("/mybookshelf/last_read")
@login_required
def last_read_book():
    
    data = request.get_json()
    manager = BookManager(data)
    
    result = manager.get_last_reading_history()
    if not result:
        return jsonify(msg = 'No record for last read'), 404
    elif result == -1:
        return jsonify(msg = 'Error for searching')
    
    return jsonify(result)

@articles_bp.route("/mybookshelf/reading_history")
@login_required
def reading_history():
    data = request.get_json()
    manager = BookManager(data)
    
    result = manager.get_reading_history()
    
    if result == []:
        return jsonify(msg = 'No history'), 404
    elif result == -1:
        return jsonify(msg = 'Error for searching')

    return jsonify(result)  
