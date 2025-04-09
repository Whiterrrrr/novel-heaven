from app.models import *
from . import articles_bp
from forms import ArticleForm, ChapterForm
from flask_login import login_required, current_user
from flask import render_template, request, jsonify
import datetime

@articles_bp.route("/publish/submmit", methods=['GET', 'POST'])
def publish_article():
    data = request.get_json()
    
    form = ArticleForm(data={
        'title': data.get('article_title'),
        'category': data.get('category')
    })
    article_id = data.get('article_id')
    
    article = Article.query.filter_by(
        id=article_id,
        user_id=current_user.id,
        is_draft=True
    ).first()
    
    if not article:
        return jsonify(msg = 'Article is not exist'), 404
    
    try:
        # 更新文章状态
        article.is_draft = False
        article.published_at = datetime.utcnow()
        
        # 更新关联章节状态（如果有章节草稿）
        Chapter.query.filter_by(article_id=article.id, is_draft=True).update(
            {"is_draft": False},
            synchronize_session=False
        )
        
        db.session.commit()
        
        return jsonify({
            "code": 200,
            "msg": "Successfully submmit",
            "published_at": article.published_at.isoformat(),
            "article_url": f"/articles/{article.id}"  # 文章打开详情页的路径
        })
    except Exception as e:
        db.session.rollback()
        return jsonify(msg = 'Error sending'), 500
    
    
@articles_bp.route("/publish/create", methods=['POST'])
def create_new_article():
    
    new_article = Article(
        title = request.json.get('title'),
        user_id = current_user.id,
        category = request.json.get('category'),
        is_draft = True
    )
    db.session.add(new_article)
    db.session.commit()
    
    return jsonify({
        "code": 201,
        "novel_id": new_article.id,
        "edit_url": f"/editor/{new_article.id}" # 跳转到编辑页面，需要editor.html
    })


@articles_bp.route("/publish/chapter_make", methods=['POST'])
@login_required
def create_new_chapter():
    request_data = request.get_json() 
    
    article_id = request_data.get('article_id')

    form = ChapterForm(data={
        'chapter_title': request_data.get('chapter_title'),
        'content': request_data.get('content')
    })
    
    if form.validate() and article_id:

        article = Article.query.filter_by(id = article_id, user_id = current_user.id).first()
        if not article:
            return jsonify(msg = "Error operation"), 403
 
        max_order = Chapter.query.filter_by(article_id=article.id).with_entities(db.func.max(Chapter.order)).scalar() or 0
        
        chapter = Chapter(
            title=request_data.get('title'),
            content=request_data.get('content'),
            order=max_order + 1,
            article_id=article.id,
            is_draft=True
        )
            
        db.session.add(chapter)
        db.session.commit()
    
    return jsonify({
        "code": 200,
        "chapter_id": chapter.id,
        "order": chapter.order
    })


@articles_bp.route("/editor/<int:article_id>")
@login_required
def article_editor(article_id):

    article = Article.query.filter_by(
        id=article_id,
        user_id=current_user.id
    ).first_or_404()
    
    chapters = Chapter.query.filter_by(article_id=article_id).order_by(Chapter.order).all()
    
    return render_template('editor.html', 
        article=article,
        chapters=chapters
    )
    

@articles_bp.route("/delete/chapter/<chapter_id>", methods=['POST'])
@login_required
def delete_chapter(chapter_id):
    chapter_select = Chapter.query.filter_by(user_id = current_user, chapter_id = chapter_id).first()
    
    if not chapter_select:
        return jsonify(msg = 'Chapter chosen to delete is not in your personal editing space'), 400
    else:
        db.session.delete(chapter_select)
        db.session.commit()
        return jsonify(msg = 'Successfully delete')


@articles_bp.route("/delete/article/<article_id>", methods=['POST'])
@login_required
def delete_article(article_id):
    article_select = Article.query.filter_by(user_id = current_user, article_id = article_id).first()
    
    if not article_select:
        return jsonify(msg = 'Article chosen to delete is not in your personal editor'), 400
    else:
        db.session.delete(article_select)
        db.session.commit()
        return jsonify(msg = 'Successfully delete')