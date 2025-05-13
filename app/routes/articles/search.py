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
        page_size = self.data['page_size'] if 'page_size' in self.data.keys() else 4
        
        return DBOperations.search_books(key_word,page,page_size)
    
    def recommend_books(self,limit):
        # limit = self.data['limit'] if 'limit' in self.data.keys() else 27
        return DBOperations.recommend_hot_articles(limit)
    
        
@articles_bp.route("/search")
def search_books(): # Search for all articles with the search term in the title or abstract (paging available)
    """
    Params:
        q (str): The keyword to search for.
        page (int): The current page number.

    Returns:
        JSON response:
            - List of matching novels with details (cover URL, word count, etc.)
            - Pagination information: total items, current page, total pages.
            - 404 if no keyword provided.
            - Error message for invalid input.
    """
    
    keywords = request.args.get("q", "")
    page = request.args.get("page", "")
    data ={
        'key_word':keywords,
        'page':int(page)}
    manager = SearchManager(data)
    
    book_list, total_num, current_page, total_pages = manager.search_books()
    
    if book_list == -1:
        return jsonify(msg = 'Non valid input')
    elif book_list == []:
        return jsonify(msg = "The keyword to be searched was not provided"), 404
    else:
        items = []
        for article in book_list:
            stat = article.to_dict2()
            img_path = stat['author']+'/'+stat['article_name']+'/img.jpg'
            stat['cover_url'] = img_path
            wordcount = (str(stat['word_count']/10000)+' million words') if stat['word_count']>10000 else (str(stat['word_count'])+' words')
            stat['word_count'] = wordcount
            # print(wordcount)
            items.append(stat)
        data = {
            'counts':total_num,
            'page':current_page,
            'total_pages':total_pages,
            'items':items 
        }
        return jsonify(data)
    
    
@articles_bp.route("/hot",methods=['GET'])
#@articles_bp.route("/api/novel/categories/hot",methods=['GET'])
def recommend(): 
    """
    Recommend a list of hot novels.

    Returns:
        JSON response:
            - List of recommended novels with details (cover URL, title, author, etc.)
            - 404 if no recommendations are found.
    """
    
    data = {}
    manager = SearchManager(data)
    
    recommend_articles = manager.recommend_books(10)
    # print(recommend_articles)
    items = []
    for article in recommend_articles:
        stat = article.to_dict()
        img_path = stat['author']+'/'+stat['article_name']+'/img.jpg'
        stat['cover_url'] = img_path
        items.append(stat)
    if recommend_articles == []:
        return jsonify(msg = "错误描述"), 404
    else:
        return jsonify(items)
    
    
        
    