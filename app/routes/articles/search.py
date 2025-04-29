from flask import Blueprint, request, g, jsonify
from . import articles_bp
from app.models import KeyWord, Article, db
from app.models import DBOperations
from sqlalchemy import not_, or_

class SearchManager():
    def __init__(self, data):
        self.data = data 

    def keytag_list(self):
        try:
            search_keyword = self.data['search_keyword']
        except :
            return -1
        
        limit = self.data['limit'] if 'limit' in self.data.keys() else 5
        
        return DBOperations.keytag_list(search_keyword, limit)
    
    def search_books(self):
        try:
            key_word = self.data['key_word']
        except:
            return -1
        
        page = self.data['page'] if 'page' in self.data.keys() else 1
        page_size = self.data['page_size'] if 'page_size' in self.data.keys() else 10
        
        return DBOperations.search_books(key_word,page,page_size)
    
    def recommend_books(self,limit):
        # limit = self.data['limit'] if 'limit' in self.data.keys() else 27
        return DBOperations.recommend_hot_articles(limit)
    
        
@articles_bp.route("/search_tags")
def keytag_list(): 
    data = request.get_json()
    manager = SearchManager(data)
    
    tag_list = manager.keytag_list()
    
    if tag_list == -1:
        return jsonify(msg = 'Non valid input')
    elif tag_list == []:
        return jsonify(msg = 'Error'), 404
    else:
        data = [{
        'keyword':word.keyword,
        'is_hot':word.is_hot
    } for word in tag_list]
        return jsonify(data)
    
@articles_bp.route("/search")
def search_books(): # 按关键词搜索title包含该词的所有文章（分页提供）
    keywords = request.args.get("q", "")
    data ={'key_word':keywords}
    manager = SearchManager(data)
    
    book_list, total_num, current_page, total_pages = manager.search_books()
    
    if book_list == -1:
        return jsonify(msg = 'Non valid input')
    elif book_list == []:
        return jsonify(msg = "The keyword to be searched was not provided"), 404
    else:
        items = [article.to_dict1() for article in book_list]
            
        data = {
            'counts':total_num,
            'page':current_page,
            'total_pages':total_pages,
            'items':items 
        }
        return jsonify(data)
    
    
@articles_bp.route("/hot",methods=['GET'])
def recommend(): # 简易推荐书目
    data = {}
    manager = SearchManager(data)
    
    recommend_articles = manager.recommend_books(27)
    
    if recommend_articles == []:
        return jsonify(msg = "错误描述"), 404
    else:
        items = [article.to_dict() for article in recommend_articles]
        return jsonify(items)
    
    
        
    