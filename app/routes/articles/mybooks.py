from flask import Blueprint, request, jsonify
from . import articles_bp
from models import BookShelf, Article, User, ReadingRecord, Chapter,  db
from flask_login import login_required, current_user
import random

@articles_bp.route("/mybookshelf")
@login_required
def mybooks_list():
    
    myBookShelf = BookShelf.query.filter_by(user_id = current_user).order_by(BookShelf.created.desc()).all()
    data = []
    """
    if not myBookShelf:
        total = Book.query.all()
        return_book_list = random.sample(total, 5)
        for bk in return_book_list:
            book_shelf = BookShelf(user_id = user_id, book_id = bk.book_id, book_name = bk.book_name, cover = bk.cover)
        
            #db.session.add(book_shelf)
            data.append({
                'id':bk.book_id,
                'titke':bk.book_name
            }   
            )
        db.session.commit()
    """
    if not myBookShelf:
        pass
    else:
        for bk in myBookShelf:
            data.append({
            'id':bk.book_id,
            'title':bk.book_name
            })
    return jsonify(data)


@articles_bp.route("/mybookshelf/<book_id>", methods=['POST'])
@login_required
def add_book_to_shelf(book_id): 
    book_select = Article.query.filter_by(id = book_id).first()
    
    if not book_select:
        return jsonify(msg='Target book is not found'), 404
    
    book_shelf_exist = BookShelf.query.filter_by(user_id = current_user, book_id = book_id).first()
    
    if not book_shelf_exist:
        bookshelf = BookShelf(
            user_id = current_user,
            book_id = book_select.book_id,
            book_name = book_select.book_name,
            # cover = book_select.cover
        )
        db.session.add(bookshelf)
        db.session.commit()
        
        return jsonify(msg = 'Successfully add')
    else:
        return jsonify(msg = 'Book has been in your personal shelf'), 400


@articles_bp.route("/mybookshelf/<book_id>", methods=['DELETE'])
@login_required
def delete_book_from_shelf(book_id):
    book_select = BookShelf.query.filter_by(user_id = current_user, book_id = book_id).first()
    
    if not book_select:
        return jsonify(msg = 'Book chosen to delete is not in your personal shelf'), 400
    else:
        db.session.delete(book_select)
        db.session.commit()
        return jsonify(msg = 'Successfully delete')


@articles_bp.route("/mybookshelf/last_read")
@login_required
def last_read_book():
    user = User.query.get(current_user)
    
    last_progress = ReadingRecord.query.filter_by(user_id=current_user).order_by(ReadingRecord.last_read_time.desc()).first()

    if not last_progress:
        return jsonify(msg = 'No record for last read'), 404

    # 获取书籍和章节详情
    book = Article.query.get(last_progress.book_id)
    chapter = Chapter.query.filter_by(id = last_progress.chapter_id, article_id = last_progress.book_id)

    return jsonify({
        "code": 200,
        "data": {
            "book_id": book.book_id,
            "book_title": book.book_name,
            "chapter_id": chapter.id,
            "chapter_title": chapter.title,
            "last_read_time": last_progress.last_read_time.isoformat(),
            "percentage": last_progress.percentage
        }
    })