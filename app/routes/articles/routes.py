from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import articles_bp
from .forms import ArticleForm
from app.models import Article, db

@articles_bp.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    """文章发布路由"""
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author=current_user,
            is_draft=form.save_as_draft.data
        )
        db.session.add(article)
        db.session.commit()
        flash('草稿已保存' if article.is_draft else '文章发布成功！', 'success')
        return redirect(url_for('articles.manage'))
    return render_template('articles/publish.html', form=form)

@articles_bp.route('/<int:article_id>')
def view_article(article_id):
    """文章详情页路由"""
    article = Article.query.get_or_404(article_id)
    article.views += 1  # 增加阅读计数
    db.session.commit()
    return render_template('articles/article.html', article=article)

@articles_bp.route('/manage')
@login_required
def manage():
    """文章管理路由"""
    articles = Article.query.filter_by(author=current_user).order_by(Article.created_at.desc()).all()
    return render_template('articles/manage.html', articles=articles)