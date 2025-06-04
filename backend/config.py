import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'dev-key-123'  # 生产环境必须改为随机字符串
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'database', 'ratings.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 会话配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'  # 允许跨站请求
    PERMANENT_SESSION_LIFETIME = 86400  # 会话有效期24小时
