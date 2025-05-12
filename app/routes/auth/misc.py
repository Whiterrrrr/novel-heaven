from datetime import datetime
from flask import Blueprint, jsonify, request
from app.models import Article, User
from flask_login import current_user, login_required
from app.routes.auth import auth_bp
from app.routes.articles import articles_bp
from app.models import db
from app.models import DBOperations

@auth_bp.route('/user/comments', methods=['GET'])
@login_required
def get_user_comments():
    user = User.query.filter_by(id=current_user.id).first()
    print("call get_user_comments()")
    result = DBOperations.get_user_comments(user.id)
    print(result)
    return jsonify({"objects": result}), 200

@auth_bp.route('/user/coins', methods=['GET'])
@login_required
def get_user_coins():
    user = User.query.filter_by(id=current_user.id).first()
    print("call get_user_coins()")
    return jsonify({ "balance": user.balance }), 200


@auth_bp.route('/user/center', methods=['GET'])
@login_required
def get_my_center():
    print("call get_my_center")
    user = User.query.filter_by(id=current_user.id).first()
    bookshelf = DBOperations.get_bookshelf_data(user.id)
    bookshelf = [DBOperations.get_article_statistics(book.article_id) for book in bookshelf]
    get_cover_pth = lambda book: f"/api/novel/cover/{book['author']}/{book['title']}/img.jpg"
    get_book_name = lambda id: Article.query.filter_by(id=id).first().article_name
    books = [{"id":book['id'], "cover":get_cover_pth(book), "title":book['title'], "author":book['author']} for book in bookshelf]
    tippings = DBOperations.get_user_tippings(user.id, limit=10)
    tippings = [{"date": tipping['time'],
                 "amount": tipping['amount'],
                 "book":get_book_name(tipping['article_id'])}
                for tipping in tippings]
    comments = DBOperations.get_user_comments(user.id)
    comments = [{"book":get_book_name(comment["article_id"]),
                 "content": comment["content"],
                 "date": comment["time"]} for comment in comments]
    '''{
    book: "书籍名称",  // 字符串类型
    content: "评论内容",  // 字符串类型
    date: "2025-05-12"  // 字符串或Date类型（需格式化）
    }'''

    return jsonify({
        "favoriteBooks": books,
        "rewards": tippings,
        "messages": comments,
        "remainingCoins": user.balance,
    }), 200


@auth_bp.route('/user/favorites/<int:article_id>', methods=['POST'])
@login_required
def add_favorite(article_id):
    print("call add_favorite()")
    bookshelf, state = DBOperations.add_to_bookshelf(current_user.id, article_id)
    if bookshelf is not None and state:
        return jsonify({"msg": "favorited"}), 201 # 类似于这种
    else:
        return jsonify({"msg": "unsuccessful"}), 400  # 类似于这种


@auth_bp.route('/user/favorites/<int:article_id>', methods=['DELETE'])
@login_required
def remove_favorite(article_id):
    print("call remove_favorite()")
    state = DBOperations.delete_book_from_shelf(current_user.id, article_id)
    if state:
        return jsonify({"msg": "unfavorited"}), 200
    else:
        return jsonify({"msg": "unsuccessful"}), 400  # 类似于这种
