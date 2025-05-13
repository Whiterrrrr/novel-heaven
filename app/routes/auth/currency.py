from datetime import datetime
from flask import Blueprint, jsonify, request
from app.models import Article, User, DBOperations
from flask_login import current_user, login_required
from app.routes.auth import auth_bp
from app.routes.articles import articles_bp
from app.models import db
from app.routes.auth.forms import TippingForm


@auth_bp.route('/user/rewards', methods=['GET', 'POST'])
@login_required
def get_reward():
    """
    Manage user tipping records and balance
    Methods:
        GET: Retrieve tipping history
        POST: [Reserved for future use]
    Security:
        - Requires valid login session
    Returns:
        - 200: JSON with tipping history and current balance
    Data Structure:
        result: Array of tipping transaction objects
        balance: Current remaining coins
    Process:
        1. Verify user authentication
        2. Query tipping records via DBOperations
        3. Return combined financial data
    """
    user = User.query.filter_by(id=current_user.id).first()
    result = DBOperations.get_user_tippings(user.id)
    return jsonify({"result": result,"balance": user.balance}), 200

@auth_bp.route('/novel/<int:article_id>/tip', methods=['POST'])
@login_required
def tip_author(article_id):
    """
    Process author tipping transaction
    Parameters:
        article_id (int): Target novel content ID
    Form Data:
        tips (int): Tipping amount (default: 1)
    Security:
        - Requires valid login session
    Returns:
        - 200: Success with updated balance
        - 400: Invalid amount/insufficient balance
        - 404: Article not found
        - 500: Transaction failure
    Process:
        1. Validate article existence
        2. Verify tipping amount validity
        3. Check payer's balance adequacy
        4. Execute balance transfer transaction
        5. Record tipping in database
    Data Flow:
        - Deduct coins from current user
        - Credit coins to article author
        - Create tipping record
    """
    article = Article.query.get_or_404(article_id)
    print(article.article_name)
    author = DBOperations.get_user_by_id(article.author_id)
    print(author.username)

    form = TippingForm()
    amount = form.tips.data
    if amount is None:
        amount = 1

    if not isinstance(amount, int) or amount <= 0:
        return jsonify({"code": 400, "msg": "金额无效"}), 400

    if current_user.balance < amount:
        return jsonify({"code": 400, "msg": "余额不足"}), 400

    try:
        current_user.balance -= amount
        author.balance += amount
        tipping = DBOperations.create_tipping(current_user.id, article_id, amount)

    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "msg": "打赏失败"}), 500

    return jsonify({
        "code": 200,
        "msg": "打赏成功",
        "myBalance": current_user.balance,
        "transaction_id": tipping.id
    })