from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    school = db.Column(db.String(64), nullable=False)
    ratings = db.relationship('Review', backref='user', lazy=True)
    
    # 添加点赞和点踩关系
    liked_ratings = db.relationship(
        'Review',
        secondary='user_liked_ratings',
        backref=db.backref('liked_by', lazy='dynamic'),
        lazy='dynamic'
    )
    
    disliked_ratings = db.relationship(
        'Review',
        secondary='user_disliked_ratings',
        backref=db.backref('disliked_by', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    department = db.Column(db.String(64))
    ratings = db.relationship('Review', backref='teacher', lazy=True)
    
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    teacher_name = db.Column(db.String(64), nullable=False)
    department = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    
    def associate_with_teacher(self, teacher):
        """将评价关联到教师"""
        self.teacher_id = teacher.id
        db.session.commit()

# 点赞关联表
user_liked_ratings = db.Table('user_liked_ratings',
    db.Column('user_id', db.Integer, db.ForeignKey('user_data.id'), primary_key=True),
    db.Column('review_id', db.Integer, db.ForeignKey('reviews.id'), primary_key=True)
)

# 点踩关联表
user_disliked_ratings = db.Table('user_disliked_ratings',
    db.Column('user_id', db.Integer, db.ForeignKey('user_data.id'), primary_key=True),
    db.Column('review_id', db.Integer, db.ForeignKey('reviews.id'), primary_key=True)
)
