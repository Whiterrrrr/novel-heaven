from flask import jsonify, request
from app.models import ReadingRecord, Article, Chapter
from flask_login import current_user, login_required
from app.routes.auth import auth_bp
from app.models import db

@auth_bp.route('/reading_history', methods=['GET'])
@login_required
def get_reading_history():
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 查询当前用户的阅读记录（按最后阅读时间倒序）
    query = ReadingRecord.query.filter_by(author_id=current_user.id)\
                                 .order_by(ReadingRecord.last_read_time.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    history_records = pagination.items

    # 结构化返回数据
    history_data = []
    for record in history_records:
        book = Article.query.get(record.book_id)
        chapter = Chapter.query.get(record.chapter_id) if record.chapter_id else None

        history_data.append({
            "book_id": book.book_id,
            "book_title": book.book_name,
            "cover": book.cover,
            "last_chapter": {
                "chapter_id": chapter.id if chapter else None,
                "chapter_title": chapter.title if chapter else "未知章节"
            },
            "progress": round(record.percentage * 100, 1),  # 转换为百分比
            "last_read_time": record.last_read_time.isoformat()
        })

    return jsonify({
        "data": history_data,
        "pagination": {
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page,
            "per_page": per_page
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