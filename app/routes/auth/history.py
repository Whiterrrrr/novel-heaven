from flask import jsonify, request
from app.models import ReadingRecord, Article, Chapter
from flask_login import current_user, login_required
from app.routes.auth import auth_bp
from app.models import db

@auth_bp.route('/reading_history', methods=['GET'])
@login_required
def get_reading_history():
    # 获取分页参数
    print(request.args)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 查询当前用户的阅读记录（按最后阅读时间倒序）
    query = ReadingRecord.query.filter_by(user_id=current_user.id).order_by(ReadingRecord.latest_reading_time.desc()).all()
    print(query)
    # pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    # history_records = pagination.items

    # 结构化返回数据
    history_data = []
    for record in query:
        book = Article.query.get(record.article_id)
        chapter = Chapter.query.get(record.latest_reading_chapter_id) if record.latest_reading_chapter_id else None
        print(f"chapter_id:{chapter.chapter_id}, chapter_name:{chapter.chapter_name}")
        history_data.append({
            "book_id": book.id,
            "book_title": book.article_name,
            "last_chapter": {
                "chapter_id": chapter.chapter_id if chapter else None,
                "chapter_title": chapter.chapter_name if chapter else "未知章节"
            },
            # "progress": round(record.percentage * 100, 1),  # 转换为百分比
            "last_read_time": record.latest_reading_time.isoformat()
        })

    return jsonify({
        "data": history_data,
        "pagination": {
        }
    }), 200

@auth_bp.route('/reading_history/<int:record_id>', methods=['DELETE'])
@login_required
def delete_reading_history(record_id):
    # 确保用户只能删除自己的记录
    record = ReadingRecord.query.filter_by(
        author_id=current_user.id,
        id=record_id
    ).first()

    if not record:
        return jsonify({"code": 404, "msg": "记录不存在"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"code": 200, "msg": "删除成功"})