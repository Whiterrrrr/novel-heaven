from app.models import *
from . import author_bp
# from forms import ArticleForm, ChapterForm
from flask_login import login_required, current_user
from flask import render_template, request, jsonify
import datetime
from abc import ABC, abstractmethod
import os
import app
from datetime import datetime
from PIL import Image

def allowed_file(filename):
    allowed_type = ['jpg', 'jpeg', 'png']
    file_type = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and allowed_type.__contains__(file_type), file_type
    
class PublishManager(ABC):
    def __init__(self, data):
        self.data = data
        
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass
    
    
    
class PublishArticle(PublishManager):
    def __init__(self,data):
        super().__init__(data)
        
    def create(self):
        try:
            author_id = self.data['author_id']
            article_data = self.data['article_data']
        except:
            return -1
        print(f'author id is {author_id}')
        return DBOperations.create_article(author_id, article_data)
    
    def update(self):
        """
        try:
            form = ArticleForm(data={
            'title': self.data.get('article_title'),
            'category': self.data.get('category')
        })
        """
        try:
            article_id = self.data.get('article_id')
            update_data = self.data.get('update_data')
        except:
            return -1
        
        return DBOperations.update_article(article_id, update_data)
    
    def delete(self):
        try:
            article_id = self.data.get('article_id')
        except:
            return -1
        
        return DBOperations.delete_article(article_id)
    
    def show(self):
        try:
            user_id = self.data.get('user_id')
        except:
            return -1
        
        return DBOperations.get_author_articles(user_id)
    
class PublishChapter(PublishManager):
    def __init__(self,data):
        super().__init__(data)
        
    def create(self):
        try:
            article_id = self.data['article_id']
            chapter_data = self.data['chapter_data']
        except:
            return -1
        
        return DBOperations.create_chapter(article_id, chapter_data)
    
    def update(self):
        try:
            chapter_id = self.data.get('chapter_id')
            update_data = self.data.get('update_data')
        except:
            return -1
        
        return DBOperations.update_chapter(chapter_id, update_data)
    
    def delete(self):
        try:
            chapter_id = self.data.get('chapter_id')
        except:
            return -1
        
        return DBOperations.delete_chapter(chapter_id)      
    
    
          
@author_bp.route("/works/<int:article_id>/status", methods= ['PUT'])
def update_article(article_id):
    """
    Update the content of a specific article.


    Arg:
        - article_id (int): The ID of the article to update.

    Param:
        - update_content (dict): The new attribute to update.

    Returns:
        JSON response:
            - If success: Confirmation message and latest update timestamp.
            - 404 if the article does not exist.
            - 400 if the input is invalid.
    """
    
    recv = request.get_json()
    data = {}
    data['article_id'] = article_id
    data['update_data'] = recv['update_content']
    manager = PublishArticle(data)
    
    article = manager.update()
    
    if not article:
        return jsonify(msg = 'Article is not exist'), 404
    elif article == -1:
        return jsonify(msg = 'No valid input')
    
    return jsonify({
        "msg": "Successfully updated",
        "published_at": article.latest_update_time.isoformat()
       # "article_url": f"/articles/{article.id}"  # 文章打开详情页的路径
    })


def convert_to_jpg(file_stream, output_dir, target_size=(297, 420)):
    try:
        with Image.open(file_stream) as img:
            
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background  # [7,8](@ref)
            else:
                img = img.convert('RGB')  # [6](@ref)
            resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
            
            filename = f"img.jpg"  # [5](@ref)
            save_path = os.path.join(output_dir, filename)

            resized_img.save(save_path, 'JPEG', quality=85, optimize=True)  # [6,7](@ref)
            return save_path
    except Exception as e:
        raise RuntimeError(f"格式转换失败: {str(e)}")  # [6](@ref)

@author_bp.route("/works", methods=['POST','GET'])
@login_required
def create_new_article():
    """
    Create a new novel (POST) or list the author's novels (GET).
    """
    if request.method == 'POST':
        article_data = {}
        
        article_data['article_name'] = request.form.get('title')
        article_data['intro'] = request.form.get('synopsis')
        # cat_id = Category.query.filter_by(id=request.form.get('category_id'))
        cat_id = request.form.get('category_id')
        print(cat_id)
        article_data['cat_id'] = cat_id
        file = request.files['cover']
        alowed, file_type = allowed_file(file.filename)
        # 如果文件符合要求，进行保存
        if file and alowed:
            authorname = User.query.get(current_user.id).username

            cover_dir = os.path.join('book_sample', authorname, article_data['article_name'])
            os.makedirs(cover_dir, exist_ok=True)  

            cover_path = convert_to_jpg(file.stream, cover_dir)
        
            
        data = {
            'author_id':current_user.id,
            'article_data':article_data
        }
            
        
        manager = PublishArticle(data)
        
        new_article = manager.create()
        
        if not new_article:
            return jsonify(msg = 'Error')
        elif new_article == -1:
            return jsonify(msg = 'Non valid input')
        else:
            return jsonify({
                "novel_id": new_article.id,
                "message":"Novel published successfully!"
            })
    else:
        
        #print(current_user.id)
        data = {'user_id':current_user.id}
        #data = {'user_id':6}
        manager = PublishArticle(data)
        books = manager.show()
        authorname = User.query.get(current_user.id).username
        for book in books:
            book['cover'] = f"{authorname}/{book['title']}/img.jpg"
        
        return jsonify(books)
        

@author_bp.route("/works/<int:article_id>", methods=['DELETE'])
#@login_required
def delete_article(article_id):
    """
    Delete a specified article by its ID.
    """
    data = {'article_id':article_id}
    manager = PublishArticle(data)
    
    status = manager.delete()
    
    if status == -1:
        return jsonify(msg = 'Non valid article_id')
    elif not status:
        return jsonify(msg = 'Article chosen to delete is not exist'), 400
    else:
        return jsonify(msg = 'Successfully delete')
    
    
@author_bp.route("/works/<int:article_id>/chapters", methods=['POST'])
@login_required
def create_chapter(article_id):
    """
    Create a new chapter for a specific article.

    Arg:
        - article_id (int): ID of the article to which the chapter belongs.

    Request JSON Body:
        - title (str): Chapter title.
        - content (str): Chapter content.

    Actual Operations:
        - Save chapter content as a text file under the author's directory.
        - Generate chapter metadata including word count and file path.
        - Use PublishChapter manager to insert chapter data into the database.
    """
    
    recv = request.get_json() 
    # print(recv)
    data = {}
    chapter_data = {}
    
    # content = recv['content']
    title = recv['title']
    content = 'Chapter Title: ' +title + '\n\n' + recv['content']
    
    word_count = len(content)
    user = User.query.filter_by(id=current_user.id).first().username
    
    article: Article = Article.query.get(article_id)
    if article:
        article_name = article.to_dict()['title']
    chapterID = len(Chapter.query.filter_by(article_id=article_id).all()) + 1
    text_path = os.path.join('book_sample', user, article_name, 'chapter', f"chapter{chapterID}.txt")

    os.makedirs(os.path.dirname(text_path), exist_ok=True)  

    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    # print(f"recv is {recv}")
    chapter_data['chapter_name'] = f"chapter{chapterID}"
    chapter_data['text_path'] = text_path
    chapter_data['chapter_id'] = chapterID
    chapter_data['status'] = recv['status']
    # chapter_data['is_draft'] = False
    #print(recv['is_draft'])
    chapter_data['word_count'] = word_count
    data['chapter_data'] = chapter_data
    data['article_id'] = article_id
    manager = PublishChapter(data)

    # print(data['chapter_data'])
    status, new_chapter = manager.create()
    # print(new_chapter)
    if not new_chapter:
        return jsonify(msg = 'Error')
    elif new_chapter == -1:
        return jsonify(msg = 'Non valid input')
    else:
        return jsonify({
            "novel_id": article_id,
        })
        
@author_bp.route("/works/<int:article_id>/chapters/<int:chapter_id>", methods=['PUT'])
@login_required
def update_chapter(article_id, chapter_id):
    """
    Update an existing chapter's title and content.


    Args:
        - article_id (int): ID of the article the chapter belongs to.
        - chapter_id (int): ID of the chapter to update.

    Request JSON Body:
        - title (str): New chapter title.
        - content (str): Updated chapter content.

    Behavior:
        - Delete the original chapter text file.
        - Save the updated content as a new text file with the new chapter title.
        - Update chapter metadata in the database via PublishChapter manager.
    """
    
    data = {
        'article_id':article_id,
        'chapter_id':chapter_id
    }
    
    recv = request.get_json() 
    update = {}
    update['chapter_name'] = recv['title']
    
    # status = DBOperations.delete_chapter(chapter_id)  
        
    authorname = User.query.get(current_user.id).username
    novelname = Article.query.get(article_id).article_name
    chaptername = Chapter.query.get(chapter_id).chapter_name
    origin_path = f'book_sample/{authorname}/{novelname}/chapter/{chaptername}.txt'
    if os.path.exists(origin_path):
        os.remove(origin_path)
    text_path = f'book_sample/{authorname}/{novelname}/chapter/{recv["title"]}.txt'
    
    os.makedirs(os.path.dirname(text_path), exist_ok=True)  

    # content = 'Chapter Title: ' + recv['title'] + '\n\n' + recv['content']
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(recv['content'])
    
    update['text_path'] = text_path
    data['update_data'] = update
    manager = PublishChapter(data)
    
    # print(update)
    article = manager.update()
    
    if not article:
        return jsonify(msg = 'Article is not exist'), 404
    elif article == -1:
        return jsonify(msg = 'No valid input')
    
    return jsonify({
        "msg": "Successfully update",
        "published_at": article.latest_update_time.isoformat()
       # "article_url": f"/articles/{article.id}"  # 文章打开详情页的路径
    })
    
@author_bp.route("/chapters/<int:chapter_id>", methods=['PUT'])
@login_required
def delete_chapter(article_id, chapter_id):
    data = {
        'article_id':article_id,
        'chapter_id':chapter_id
    }
    manager = PublishChapter(data)
    
    status = manager.delete()
    
    
    if status == -1:
        return jsonify(msg = 'Non valid chapter_id')
    elif not status:
        return jsonify(msg = 'Chapter chosen to delete is not exist'), 400
    else:
        return jsonify(msg = 'Successfully delete')
    

@author_bp.route("/me")
@login_required
def author_info():
    user = User.query.get(current_user.id)
    result = {
        'authorName':user.username,
        'coins':user.balance
    }
    print(user.username)
    return jsonify(result)

@author_bp.route("/comments")
@login_required
def fetch_comment():
    """"
    Fetch the latest comments for all articles authored by the current logged-in author.
    """
    
    limit = request.args.get("limit", 5)
    user_id = current_user.id
    
    books = DBOperations.get_author_articles(user_id)
    book_id = [book['id'] for book in books]
    
    comment = []
    for id in book_id:
        comment.append(DBOperations.get_article_comments(id,include_user_info=True)[0])
        
    flattened_data = [item for sublist in comment for item in sublist]

    # Sort by time descending
    sorted_data = sorted(
        flattened_data,
        key=lambda x: datetime.fromisoformat(x['time']),
        reverse=True
    )

    data = sorted_data[:limit] if len(sorted_data)>=int(limit) else sorted_data
    result = []
    for comment in data:
        result.append({
            'content':comment["content"],
            'date': comment["time"][:10],
            'reader': comment["user"]["username"]
        })
    
    # print(result)
    return jsonify(result)

@author_bp.route("/works/overview/<int:article_id>")
@login_required 
def show_article(article_id):
    """
    Retrieve detailed information about a specific article, including its metadata, chapters, and comments.

    Arg:
        - article_id (int): ID of the article to retrieve.

    Behavior:
        - Fetch article metadata such as title and status.
        - Fetch a summary of all chapters for the article.
        - Read content of each chapter from local text files.
        - Retrieve all comments on the article, including commenter usernames.
        - Combine all information into a structured JSON response.

    """
    
    result = {}
    origin = DBOperations.get_article_statistics(article_id)
    chapters = DBOperations.get_article_chapter_summary(article_id)
    authorname = User.query.get(current_user.id).username
    novelname = Article.query.get(article_id).article_name
    for chapter in chapters:
        text_path = f'book_sample/{authorname}/{novelname}/chapter/{chapter["title"]}.txt'
        print(text_path)
        with open(text_path, 'r', errors='ignore')as f:
            chapter['content'] = f.read()
        
    comments, _ = DBOperations.get_article_comments(article_id, include_user_info=True)
    result['title'] = origin['title']
    result['status'] = origin['status']
    result['comments'] = []
    
    for comment in comments:
        result['comments'].append({'user':comment['user']['username'], 'content':comment['content']})
    
    result['chapters'] = chapters
    
    return jsonify(result)
    