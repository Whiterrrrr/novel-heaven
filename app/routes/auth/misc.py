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

@auth_bp.route('/user/favorites', methods=['GET'])
@login_required
def get_user_favorites():
    user = User.query.filter_by(id=current_user.id).first()
    print("call get_user_favorites()")
    result = DBOperations.get_bookshelf_data(user.id)
    print(result)
    return jsonify({"objects": result}), 200

@auth_bp.route('/user/coins', methods=['GET'])
@login_required
def get_user_coins():
    user = User.query.filter_by(id=current_user.id).first()
    print("call get_user_coins()")
    return jsonify({ "balance": user.balance }), 200