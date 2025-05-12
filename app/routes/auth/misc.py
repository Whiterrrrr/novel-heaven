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

@auth_bp.route('/user/favorites/<int:article_id>', methods=['GET'])
@login_required
def check_user_favorites(article_id):
    user = User.query.filter_by(id=current_user.id).first()
    print("call get_user_favorites()")
    bookshelf = DBOperations.get_bookshelf_data(user.id)
    bookshelf = [DBOperations.get_article_statistics(book.article_id) for book in bookshelf]
    for book in bookshelf:
        if book['id'] == article_id: return jsonify({"msg": "book found"}), 200
    return jsonify({"msg": "not found"}), 400


@auth_bp.route('/user/coins', methods=['GET'])
@login_required
def get_user_coins():
    user = User.query.filter_by(id=current_user.id).first()
    print("call get_user_coins()")
    return jsonify({ "balance": user.balance }), 200


@auth_bp.route('/user/center', methods=['GET'])
@login_required
def get_my_center():
    user = User.query.filter_by(id=current_user.id).first()
    bookshelf = DBOperations.get_bookshelf_data(user.id)
    bookshelf = [DBOperations.get_article_statistics(book.article_id) for book in bookshelf]
    get_cover_pth = lambda book: f"/api/novel/cover/{book['author']}/{book['title']}/img.jpg"
    books = [{"id":book['id'], "cover":get_cover_pth(book), "title":book['title'], "author":book['author']} for book in bookshelf]
    tippings = DBOperations.get_user_tippings(user.id, limit=10)
    tippings = [{"date": tipping['time'],
                 "amount": tipping['amount'],
                 "book":Article.query.filter_by(id=tipping['article_id']).first().article_name}
                for tipping in tippings]
    '''r.date }}, I gave {{ r.amount }} coins to "{{ r.book'''
    print(tippings)
    print("call get_my_center")
    return jsonify({
        "favoriteBooks": books,
        "rewards": tippings,
        "messages": DBOperations.get_user_comments(user.id),
        "remainingCoins": user.balance,
    }), 200
'''
{
        const
    {
        favoriteBooks = [],
    rewards = [],
    messages = [],
    remainingCoins = 0,
    } = res.data | | {};
    this.favoriteBooks = favoriteBooks;
    this.rewards = rewards;
    this.messages = messages;
    this.remainingCoins = remainingCoins;
    }
'''