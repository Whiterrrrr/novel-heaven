from flask import render_template
from app.routes.main import main_bp
from app.models import Article
from flask_login import login_required

@main_bp.route('/')
def index():
    """首页路由"""
    latest_articles = Article.query.filter_by(is_draft=False)\
        .order_by(Article.created_at.desc())\
        .limit(6)\
        .all()
    return render_template('main/index.html', articles=latest_articles)

@main_bp.route('/dashboard')
@login_required 
def dashboard():
    """用户仪表盘路由"""
    return render_template('main/dashboard.html')