from flask import Blueprint, request, g, jsonify
from flask_login import current_user

from . import articles_bp
from app.models import DBOperations

class CategoryManager():
    def __init__(self,data):
        self.data = data
    
    def get_articles_by_category(self):
        category_id = self.data['category_id'] if 'category_id' in self.data.keys() else None
        category_name = self.data['category_name'] if 'category_name' in self.data.keys() else None
        limit = self.data['limit'] if 'limit' in self.data.keys() else 20
        offset = self.data['offset'] if 'offset' in self.data.keys() else 0
        
        
        return DBOperations.get_articles_by_category(category_id, category_name,limit, offset)
    
    def get_category_hot_list(self):
        limit = self.data['limit'] if 'limit' in self.data.keys() else 10
        
        return DBOperations.get_category_hot_list(limit) 
    
"""     
@articles_bp.route("/book_category")
def category_list(): # 所有类型的所有书籍
    categories = Category.query.options(db.joinedload(Category.books)).all()
    
    # 结构化数据
    result = []
    for cat in categories:
        category_data = {
            "id": cat.id,
            "name": cat.name,
            "books": [
                {
                    "id": book.book_id,
                    "title": book.book_name,
                    "author": book.author,
                    "introduction": book.introduction
                } for book in cat.books
            ]
        }
        result.append(category_data)
    
    return jsonify({"data": result})
"""
    
    
    
@articles_bp.route('/categories/list')
def get_books_by_category(): 
    """
    Get a list of novels based on a given category.

    Params:
        category (str, optional): The category name to filter novels.

    Returns:
        JSON response:
            - List of novels if found.
            - 400 JSON message for invalid input.
            - 404 JSON message if no such category.
            - Error message if a server error occurs.
    """
    category = request.args.get('category', default=None)
    data = {'category_name':category}
    manager = CategoryManager(data)
    # print(data)
    
    articles = manager.get_articles_by_category()
    # print(articles)
    if articles == -1:
        return jsonify(msg = 'Non valid input'), 400
    elif articles == []:
        return jsonify(msg = 'No such category'), 404
    elif articles == -2:
        return jsonify(msg = 'Error')
    
    result = []
    for article in articles:
        a = article.to_dict2()
        article_name = a['article_name']
        article_author = a['author']
        wordcount = (str(a['word_count']/10000)+' million words') if a['word_count']>10000 else (str(a['word_count'])+' words')
        a['word_count'] = wordcount
        a['cover_url'] = f'{article_author}/{article_name}/img.jpg'
        result.append(a)
    print(result)
    return jsonify(result)

@articles_bp.route('/categories')
def get_hot_category_list():
    """
    Get a list of the most popular novel categories.

    Params:
        limit (int, optional): The maximum number of categories to return. Default is 10.

    Returns:
        JSON response:
            - List of popular categories with their names and IDs.
            - Error message if retrieval fails.
    """
    print(current_user)
    limit = request.args.get('limit', default=10, type=int)
    data = {'limit':limit}

    manager = CategoryManager(data)
    
    hot_list = manager.get_category_hot_list()
    if hot_list == []:
        return jsonify(msg = 'Error')
    else:
        return jsonify([{'category':category.name,'id':category.id} for category in hot_list])