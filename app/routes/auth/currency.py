from datetime import datetime
from flask import Blueprint, jsonify, request
from app.models import Article, User
from flask_login import current_user, login_required
from app.routes.auth import auth_bp
from app.routes.articles import articles_bp
from app.models import db


@auth_bp.route('/user/rewards', methods=['GET', 'POST'])
@login_required
def get_reward():
    user = User.query.filter_by(id=current_user.id).first()
    print("call get reward", user.balance)

    # return jsonify({"records": [{ id, amount, bookTitle, date }], "balance": user.balance}), 200
    return jsonify({"balance": user.balance}), 200

@auth_bp.route('/<int:article_id>/tip', methods=['POST'])
@login_required
def tip_author(article_id):
    article = Article.query.get_or_404(article_id)
    author = article.author  # 假设 Article 模型有 author 关系指向 User

    # 获取打赏金额
    data = request.get_json()
    amount = data.get('amount', 0)
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

        # 记录交易
        '''transaction = Transaction(
            from_user_id=current_user.id,
            to_user_id=author.id,
            article_id=article.id,
            amount=amount
        )
        db.session.add(transaction)
        db.session.commit()'''
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "msg": "打赏失败"}), 500

    return jsonify({
        "code": 200,
        "msg": "打赏成功",
        "new_balance": current_user.balance,
        "transaction_id": transaction.id
    })