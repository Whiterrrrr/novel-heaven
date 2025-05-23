import logging
from flask import Flask, current_app, request,g
from flask_cors import CORS
from app.models.user import User
from app.models import login_manager
from datetime import datetime

def create_app():
    app = Flask(__name__)
    CORS(app,supports_credentials=True)
    print("create_app()")
    app.config.from_object('config.Config')
    app.secret_key = '1155191482'
    
    app.config['UPLOAD_FOLDER'] = 'booksample/'
    app.config['ALLOWED_EXTENSIONS'] = {'jpg'} 
    
    
    from app.models import db
    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.articles import articles_bp
    from app.routes.author import author_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(articles_bp, url_prefix='/api/novel')
    app.register_blueprint(author_bp, url_prefix='/api/author')
    '''for rule in current_app.url_map.iter_rules():
        print(f"端点名: {rule.endpoint}")
        print(f"URL路径: {rule.rule}")
        print(f"允许的HTTP方法: {rule.methods}")
        print("------")'''
    #print(app.url_map)



    
    return app

def write_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}\t{message}\n"

    with open('runtime.log', 'a', encoding='utf-8') as f:
        f.write(log_entry)
