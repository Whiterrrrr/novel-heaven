from datetime import datetime
from flask import Blueprint, jsonify, request
from app.models import SignIn, Transaction, Article
from flask_login import current_user, login_required
from app.routes.auth import auth_bp
from app.routes.articles import articles_bp
from app.models import db


'''
签到
POST /api/user/sign_in
Headers: Authorization: Bearer <token>
Response: 
{
  "code": 200,
  "msg": "签到成功",
  "balance": 110
}
'''
@auth_bp.route('/sign_in', methods=['POST'])
@login_required
def sign_in():
    today = datetime.utcnow().date()
    # 检查今日是否已签到
    existing_sign_in = SignIn.query.filter_by(user_id=current_user.id, date=today).first()
    if existing_sign_in:
        return jsonify({"code": 400, "msg": "今日已签到"}), 400

    # 新增签到记录并更新余额
    sign_in = SignIn(user_id=current_user.id)
    current_user.balance += 10  # 假设每次签到奖励 10 虚拟币

    db.session.add(sign_in)
    db.session.commit()

    return jsonify({"code": 200, "msg": "签到成功", "balance": current_user.balance})



'''
打赏
POST /api/articles/5/tip
Headers: Authorization: Bearer <token>
Body: {"amount": 50}
Response: 
{
  "code": 200,
  "msg": "打赏成功",
  "new_balance": 60,
  "transaction_id": 3
}
'''
@articles_bp.route('/<int:article_id>/tip', methods=['POST'])
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
        transaction = Transaction(
            from_user_id=current_user.id,
            to_user_id=author.id,
            article_id=article.id,
            amount=amount
        )
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "msg": "打赏失败"}), 500

    return jsonify({
        "code": 200,
        "msg": "打赏成功",
        "new_balance": current_user.balance,
        "transaction_id": transaction.id
    })