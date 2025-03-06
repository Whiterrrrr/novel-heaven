from flask import Blueprint, request, g, jsonify
from . import articles_bp
from app.models import KeyWord, Article, db
from app import not_, or_

@articles_bp.route("/search_tags")
def keytag_list(): # 输入关键词周围较高频率搜索词呈现
    search_word = request.get('search_keyword')
    
    if not search_word:
        return jsonify(msg = "No key word")
    
    keytags = KeyWord.query.filter(or_(KeyWord.is_hot == True, KeyWord.keyword.contains(search_word))).limit(5)
    
    data = [{
        'keyword':word.keyword,
        'is_hot':word.is_hot
    } for word in keytags]
    
    return jsonify(data)

@articles_bp.route("/search_books")
def search_books(): # 按关键词搜索包含该词的所有文章（分页提供）
    key_word = request.args.get("key_word")
    page = request.args.get("page", 1, type = int)
    page_size = request.args.get("pagesize", 10, type=int)
    
    if not key_word:
        return jsonify(msg = "The keyword to be searched was not provided")
    
    candidate_book = Article.query.filter( Article.title.contains(key_word))
    
    paginate = candidate_book.paginate(page, page_size)
    
    book_list = paginate.items
    
    items = []
    for book in book_list:
        items.append({
            'id': book.book_id,
            'title': book.book_name,
            'introduction': book.introduction,
            'author': book.author,
            'state': book.state,
            'category_id': book.category_id,
            "category_name": book.category_name 
        })
    
    data = {
        'counts':paginate.total,
        'page':paginate.page,
        'total_pages':paginate.pages,
        'items':items 
    }
    
    return jsonify(data)
    
@articles_bp.route("/recommend")
def recommend(): # 按照 精准搜索、包含匹配、随机推荐，展示一共7本书
    tags = request.args("key_word")
    search_key_word = KeyWord.query.filter(KeyWord.keyword == tags).first()
    
    if not search_key_word:
        search_key_word = KeyWord(keyword = search_key_word, count = 0)
    search_key_word.count += 1
    
    if search_key_word >= 10:
        search_key_word.is_hot = True
    db.session.add(search_key_word)
    db.session.commit()
    
    
    book_check_list = []
    accurate_book = {}
    match_book_list = []
    recommendation_book_list = []
    # 精准匹配
    accurate_book= Article.query.filter_by(title = tags)
    if accurate_book:
        accurate_book = {
            'id': accurate_book.id,
            'title': accurate_book.title,
            'introduction': accurate_book.introduction,
            'category_id':accurate_book.category_id,
            'category_name':accurate_book.category_name
        }
        book_check_list.append(accurate_book.id)
        
    # 包含匹配
    match_book = Article.query.filter(Article.title.contains(tags), not_(Article.id.in_(book_check_list))).limit(2)
    for book in match_book:
        match_book_list.append({
            'id': book.id,
            'title': book.title,
            'introduction': book.introduction,
            'category_id': book.category_id,
            'category_name': book.category_name
        })
        book_check_list.append(book.id)
        
    
    # 其余推荐 (如有时间推荐算法待实现）目前只是挑几本没选的 
    recommendation_book = Article.query.filter(not_(Article.id.in_(book_check_list))).limit(4)
    for book in recommendation_book:
        recommendation_book_list.append({
             'id': book.id,
            'title': book.title,
            'introduction': book.introduction,
            'category_id': book.category_id,
            'category_name': book.category_name
        })
        
    data = {
        'accurate': accurate_book,
        'match': match_book_list,
        'recommend': recommendation_book_list
    }
    
    return jsonify(data)
        
    