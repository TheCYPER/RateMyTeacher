from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()
_db_initialized = False  # 添加标志

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # 配置 CORS 支持凭证
    CORS(app, supports_credentials=True, origins=[
        'http://localhost:3000',
        'http://localhost:8080',
        'https://lighthearted-biscochitos-c101a0.netlify.app'
    ])
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # 添加 user_loader 函数
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    from .routes import init_all_routes
    init_all_routes(app)
    
    from .ai_part import init_ai_routes
    init_ai_routes(app)

    # 初始化数据库
    with app.app_context():
        try:
            # 首先创建所有表
            db.create_all()
            print("数据库表创建成功")
            
            from app.models import User
            # 检查数据库是否为空
            if User.query.count() == 0:
                print("数据库为空，开始生成测试数据...")
                from generate_test_data import main
                main()
                print("测试数据生成完成！")
        except Exception as e:
            print(f"初始化数据库时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())

    return app
