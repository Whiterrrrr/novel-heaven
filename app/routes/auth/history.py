from flask import jsonify, request
from app.models import ReadingRecord, Article, Chapter
from flask_login import current_user, login_required
from app.routes.auth import auth_bp
from app.models import db

@auth_bp.route('/reading_history', methods=['GET'])
@login_required
def get_reading_history():
    """
    Retrieve paginated reading history
    Methods:
        GET: Returns user's reading progress records
    Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10)
    Security:
        - Requires valid login session
    Returns:
        - 200: JSON with nested reading history data
    Data Structure:
        data: Array of book reading records containing:
            - book_id: Unique content identifier
            - book_title: Content title
            - last_chapter: Latest read chapter metadata
            - last_read_time: ISO formatted timestamp
        pagination: Reserved for future pagination support
    Process:
        1. Get pagination parameters
        2. Query reading records chronologically
        3. Enrich with book/chapter metadata
        4. Format timestamps to ISO standard
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = ReadingRecord.query.filter_by(user_id=current_user.id).order_by(ReadingRecord.latest_reading_time.desc()).all()
    print(query)

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
    """
    Delete specific reading history record
    Parameters:
        record_id (int): Target history entry ID
    Methods:
        DELETE: Removes reading progress record
    Security:
        - Requires valid login session
    Returns:
        - 200: Success confirmation
        - 404: Error for non-existent record
    Process:
        1. Validate record ownership
        2. Perform database deletion
        3. Maintain data consistency
    """
    record = ReadingRecord.query.filter_by(
        author_id=current_user.id,
        id=record_id
    ).first()

    if not record:
        return jsonify({"code": 404, "msg": "记录不存在"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"code": 200, "msg": "删除成功"})