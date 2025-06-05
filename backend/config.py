import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app', 'database', 'ratings.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 会话配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'
    PERMANENT_SESSION_LIFETIME = 86400

    # API配置
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:8080')
    BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')

    # OpenAI配置
    OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    FRONTEND_URL = 'http://localhost:8080'
    BACKEND_URL = 'http://localhost:5000'

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 生产环境必须设置这些环境变量
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    FRONTEND_URL = os.environ.get('FRONTEND_URL')
    BACKEND_URL = os.environ.get('BACKEND_URL')

# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
