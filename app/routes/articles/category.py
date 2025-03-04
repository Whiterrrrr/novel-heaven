from flask import Blueprint, request, g, jsonify
from . import articles_bp
from models import Category, Article, db

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
    
    
    
    
@articles_bp.route('/book_category/<int:category_id>')
def get_books_by_category(category_id): # 指明类型后书籍分页
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pagesize', 10, type=int)
    category_id = request.args.get('category_id', 0, type=int)
    
    if not category_id:
        return jsonify(msg = 'This category is not exist'), 400
    
    category = Category.query.get(category_id)
    cat_books = category.cat_books
    
    books = cat_books.order_by(Article.likes.desc())
        
    pagination = books.paginate(page=page, per_page = page_size)
    
    books_data = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "introduction": book.introduction,
            "category_id": book.category_id,
            "category_name":book.category_name
        } for book in pagination.items
    ]
    
    return jsonify({
        "category": {"id": category.id, "label": category.name},
        "total_book": pagination.total, #总符合类型的book数
        "books": books_data,
        "total_pages": pagination.pages,
        "current_page": page
    })