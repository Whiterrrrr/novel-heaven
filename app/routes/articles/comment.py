from app.models import DBOperations
from . import articles_bp
from flask_login import login_required, current_user
from flask import  request, g, jsonify

class CommentManager():
    def __init__(self, data):
        self.data = data
        
    def create_comment(self,article_id):
        try:
            user_id = self.data['user_id']
            content = self.data['content']
        except :
            return -1
        
        return DBOperations.create_comment(user_id, article_id, content)
        
    def delete_comment(self, comment_id):
        try:
            verify = self.data['verify_user_id']
        except:
            verify = False
            
        return DBOperations.delete_comment(comment_id, verify)
               
    def get_article_comment(self):
        article_id = self.data['article_id']
        page = self.data['page'] if 'page' in self.data.keys() else 1
        per_page = self.data['per_page'] if 'per_page' in self.data.keys() else 20
        include_user_info = self.data['include_user_info'] if 'include_user_info' in self.data.keys() else False
        
        return DBOperations.get_article_comments(article_id, page, per_page, include_user_info)
    
    def get_user_comments(self):
        try:
            user_id = self.data['user_id']
        except:
            return -1
        
        days = self.data['days'] if 'days' in self.data.keys() else None
        limit = self.data['limit'] if 'limit' in self.data.keys() else 100
        
        return DBOperations.get_user_comments(user_id, days, limit),days,limit
    
    def get_recent_comments(self):
        hours = self.data['hours'] if 'hours' in self.data.keys() else 24
        limit = self.data['limit'] if 'limit' in self.data.keys() else 50
        
        return DBOperations.get_recent_comments(hours, limit),hours,limit
    
    def handle_article(self):
        try:
            status = self.data['like']
            article_id = self.data['article_id']
            user_id = self.data['user_id']
        except:
            return None
        
        
        return DBOperations.user_create_like(user_id, article_id) if status else DBOperations.user_cancel_like_article(user_id, article_id)

        
@articles_bp.route("/<int:article_id>/comments", methods=['POST','GET' ])
def make_comment(article_id):
    """
    Methods:
        GET:
            - Fetch all comments for the given article.
            - Return comments list and total page number if available.

        POST:
            - Add a new comment to the article.
            - Requires user authentication.
            - Get comment content from request JSON.
            - Return created comment info if successful.
            - Return 401 if unauthorized.
            - Return error message for missing data or invalid article.

    Args:
        article_id (int): The ID of the article.
        
    """
    if request.method == 'GET':
        data = {'article_id': article_id}
        manager = CommentManager(data)
        results, page_total_num = manager.get_article_comment()

        if page_total_num > 0:
            return jsonify(results), 200
        else:
            return jsonify(msg = "Error loading comments")
    
    else:
        if not current_user.is_authenticated:
            return jsonify({"message": "Unauthorized"}), 401
        data = request.get_json()
        data['user_id'] = current_user.id
        
        manager = CommentManager(data)
        new_comment = manager.create_comment(article_id)
        print(new_comment)
        if new_comment.article:
            return jsonify({
                'id': new_comment.user_id,
                'content': new_comment.context,
                'timestamp': new_comment.time
            }), 201
        elif new_comment == -1:
            return jsonify(msg = "Missing essential information")
        else:
            return jsonify(msg = "No such article")
     
"""
@articles_bp.route("/comment/delete/<int:comment_id>", methods=['POST'])
@login_required
def delete_comment(comment_id):
    data = request.get_json()
    manager = CommentManager(data)
    check = manager.delete_comment(comment_id)
    
    if not check:
        return jsonify(msg = 'Delete not success'), 400
    else:
        return jsonify(msg = 'Successfully delete')


@articles_bp.route("/comment/userTotal", methods=['GET'])
@login_required
def get_user_comments():
    data = request.get_json()
    manager = CommentManager(data)
    
    comments,days,limit = manager.get_user_comments()
    
    if comments == -1:
        return jsonify(msg = "Non valid user id"), 400
    elif comments != []:
        return jsonify({
            'comments':comments,
            'user_id':data['user_id'],
            'days':days,
            'limit':limit
        })
    else:
        return jsonify(msg = "Fail to get comments")


@articles_bp.route("/comment/recent", methods=['GET'])
@login_required
def get_recent_comments():
    data = request.get_json()
    manager = CommentManager(data)
    comments,hours,limit = manager.get_recent_comments()
    
    if comments != []:
        return jsonify({
            'comment_article': comments,
            'hours' : hours,
            'limit':limit
        })
    else:
        return jsonify(msg = 'Fail to get recent comments')
"""

@articles_bp.route("/<int:novel_id>/like", methods=['POST'])
@login_required
def handle_like(novel_id):
    """
    Handle like or unlike actions for a novel.
    
    - Requires user authentication.
    - Get action data ('like' or 'unlike') from request JSON.
    - Update like count through CommentManager.
    - Return updated total likes if successful.
    - Return error message if operation fails.

    Args:
        novel_id (int): The ID of the novel.
    """
    
    data = request.get_json()
    data['article_id'] = novel_id
    data['user_id'] = current_user.id
    manager = CommentManager(data)
    
    total_likes = manager.handle_article() 

    if total_likes != None:
        return jsonify({'likes': total_likes}), 200
    else:
        return jsonify(msg = 'Fail operation')



    
    