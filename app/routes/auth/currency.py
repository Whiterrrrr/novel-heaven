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
    user = User.query.filter_by(id=current_user.id).first()
    print("call get reward", user.balance)
    result = DBOperations.get_user_tippings(user.id)
    # return jsonify({"records": [{ id, amount, bookTitle, date }], "balance": user.balance}), 200
    return jsonify({"result": result,"balance": user.balance}), 200

@auth_bp.route('/novel/<int:article_id>/tip', methods=['POST'])
@login_required
def tip_author(article_id):
    print("call tip_author()")
    article = Article.query.get_or_404(article_id)
    print(article.article_name)
    author = DBOperations.get_user_by_id(article.author_id)
    print(author.username)
    
    # 获取打赏金额
    form = TippingForm()
    amount = form.tips.data
    if amount is None:
        amount = 1

    if not isinstance(amount, int) or amount <= 0:
        return jsonify({"code": 400, "msg": "金额无效"}), 400

    # 检查余额是否充足
    if current_user.balance < amount:
        return jsonify({"code": 400, "msg": "余额不足"}), 400

    # 使用事务确保数据一致性
    try:
        # 扣除打赏者余额
        current_user.balance -= amount
        # 增加作者余额
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