from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()
_db_initialized = False  # 添加标志

def create_app():
    global _db_initialized  # 使用全局标志
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # 配置 CORS 支持凭证
    CORS(app, supports_credentials=True, origins=[
        'http://localhost:3000',
        'http://localhost:8080',
        'https://lighthearted-biscochitos-c101a0.netlify.app'  # 您的 Netlify 域名
    ])
    
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

    # 初始化数据库（只在第一次时执行）
    if not _db_initialized:
        with app.app_context():
            try:
                # 首先创建所有表
                db.create_all()
                print("数据库表创建成功")
                
                from app.models import User, Teacher, Review
                # 检查数据库是否为空
                if User.query.count() == 0:
                    print("数据库为空，开始生成测试数据...")
                    from generate_test_data import main
                    main()
                    print("测试数据生成完成！")
                else:
                    print(f"数据库中已有 {User.query.count()} 个用户")
                    print(f"数据库中已有 {Teacher.query.count()} 个教师")
                    print(f"数据库中已有 {Review.query.count()} 条评价")
                _db_initialized = True  # 标记为已初始化
            except Exception as e:
                print(f"初始化数据库时出错: {str(e)}")
                import traceback
                print(traceback.format_exc())

    return app
