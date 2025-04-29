from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # 配置 CORS 支持凭证
    CORS(app, supports_credentials=True, origins=['http://localhost:3000'])
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # 添加 user_loader 函数
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    from .routes import init_all_routes
    init_all_routes(app)  # 初始化所有路由
    
    from .ai_part import init_ai_routes
    init_ai_routes(app)  # 初始化AI路由

    with app.app_context():
        db.create_all()  # 自动创建数据库表

    return app
