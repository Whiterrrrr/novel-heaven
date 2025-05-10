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
    
    @app.before_request
    def log_request_info():
        # 记录请求头、方法、路径等核心信息
        print(f"""
        [Request Headers] {request.headers}
        [Request Method]  {request.method}
        [Request Path]    {request.path}
        [Request Body]    {request.get_data().decode('utf-8')}
        """)
    """
    @app.before_request
    def load_logged_in_user():
        token = request.headers.get('Authorization')
        if token:
            token = token.replace('Bearer ', '')
            user = User.query.filter_by(token=token).first()
            if user:
                g.current_user = user
            else:
                g.current_user = None
        else:
            g.current_user = None
     """
        
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
    app.run(host="0.0.0.0", port=5001, debug=True)


    
    return app

def write_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}\t{message}\n"

    with open('runtime.log', 'a', encoding='utf-8') as f:
        f.write(log_entry)
