import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'dev-key-123'  # 生产环境必须改为随机字符串
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'database', 'ratings.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
