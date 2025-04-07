from .user_routes import init_user_routes
from .teacher_routes import init_teacher_routes
from .review_routes import init_review_routes

def init_all_routes(app):
    """初始化所有路由"""
    init_user_routes(app)
    init_teacher_routes(app)
    init_review_routes(app) 