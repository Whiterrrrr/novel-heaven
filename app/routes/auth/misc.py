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
    """
    Retrieve authenticated user's comments
    Methods:
        GET: Returns paginated comment history
    Security:
        - Requires valid login session
    Returns:
        - 200: JSON array of comment objects
    Process:
        1. Get current user from session
        2. Query comments via DBOperations
        3. Format and return results
    """
    user = User.query.filter_by(id=current_user.id).first()
    result = DBOperations.get_user_comments(user.id)
    return jsonify({"objects": result}), 200

@auth_bp.route('/user/coins', methods=['GET'])
@login_required
def get_user_coins():
    """
    Get current coin balance
    Methods:
        GET: Returns user's virtual currency status
    Security:
        - Requires valid login session
    Returns:
        - 200: JSON with numeric balance value
    Data:
        balance (int): Current spendable coins
    """
    user = User.query.filter_by(id=current_user.id).first()
    return jsonify({ "balance": user.balance }), 200


@auth_bp.route('/user/center', methods=['GET'])
@login_required
def get_my_center():
    """
    Aggregate user profile data
    Methods:
        GET: Returns comprehensive user dashboard
    Security:
        - Requires valid login session
    Returns:
        - 200: JSON with nested profile data
    Data Structure:
        favoriteBooks: Array of book objects with metadata
        rewards: Recent tipping transactions
        messages: Latest comments
        remainingCoins: Current balance
    Process:
        1. Fetch bookshelf data
        2. Retrieve financial transactions
        3. Aggregate comment history
        4. Format asset URLs
    """
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
    return jsonify({
        "favoriteBooks": books,
        "rewards": tippings,
        "messages": comments,
        "remainingCoins": user.balance,
    }), 200


@auth_bp.route('/user/favorites/<int:article_id>', methods=['POST'])
@login_required
def add_favorite(article_id):
    """
    Add article to favorites
    Parameters:
        article_id (int): Target content ID
    Methods:
        POST: Creates new favorite entry
    Security:
        - Requires valid login session
    Returns:
        - 201: Success confirmation
        - 400: Error for duplicate/error
    Process:
        Calls DBOperations.add_to_bookshelf()
    """
    bookshelf, state = DBOperations.add_to_bookshelf(current_user.id, article_id)
    if bookshelf is not None and not state:
        return jsonify({"msg": "favorited"}), 201
    else:
        return jsonify({"msg": "unsuccessful"}), 400


@auth_bp.route('/user/favorites/<int:article_id>', methods=['DELETE'])
@login_required
def remove_favorite(article_id):
    """
    Remove article from favorites
    Parameters:
        article_id (int): Target content ID
    Methods:
        DELETE: Removes favorite association
    Security:
        - Requires valid login session
    Returns:
        - 200: Success confirmation
        - 400: Removal failure
    Process:
        Calls DBOperations.delete_book_from_shelf()
    """
    state = DBOperations.delete_book_from_shelf(current_user.id, article_id)
    if state:
        return jsonify({"msg": "unfavorited"}), 200
    else:
        return jsonify({"msg": "unsuccessful"}), 400
