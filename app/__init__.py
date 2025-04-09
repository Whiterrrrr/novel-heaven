from flask import Flask
from app.models import login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    from app.models import db
    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.articles import articles_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(articles_bp, url_prefix='/articles')
    
    return app