from flask import request, jsonify
from flask_login import login_required
from app import db
from app.models import Review
from app.routes.teacher_routes import check_and_add_teacher

def init_review_routes(app):
    # 添加评论
    @app.route('/api/reviews', methods=['POST'])
    @login_required
    def add_review():
        data = request.get_json()
        
        # 检查必要字段
        if not all(k in data for k in ['score', 'comment', 'teacher_name', 'department', 'user_id']):
            return jsonify({'error': '缺少必要字段'}), 400
            
        # 创建评论
        review = Review(
            score=data['score'],
            comment=data['comment'],
            teacher_name=data['teacher_name'],
            department=data['department'],
            user_id=data['user_id']
        )
        
        # 如果提供了teacher_id，则直接关联
        if 'teacher_id' in data and data['teacher_id']:
            review.teacher_id = data['teacher_id']
            
        db.session.add(review)
        db.session.commit()
        
        # 检查是否需要自动添加教师
        check_and_add_teacher(data['teacher_name'], data['department'])
        
        return jsonify({'message': '评论成功', 'id': review.id})
    
    # 获取教师评论
    @app.route('/api/reviews/<int:teacher_id>', methods=['GET'])
    def get_reviews(teacher_id):
        reviews = Review.query.filter_by(teacher_id=teacher_id).all()
        return jsonify([{
            'id': r.id,
            'score': r.score, 
            'comment': r.comment,
            'created_at': r.created_at,
            'likes': r.likes,
            'dislikes': r.dislikes
        } for r in reviews])
    
    # 获取用户评论
    @app.route('/api/user/reviews/<int:user_id>', methods=['GET'])
    def get_user_reviews(user_id):  
        reviews = Review.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': r.id,
            'score': r.score,
            'comment': r.comment,
            'created_at': r.created_at,
            'teacher_name': r.teacher_name,
            'department': r.department,
            'likes': r.likes,
            'dislikes': r.dislikes
        } for r in reviews])
    
    # 点赞评论
    @app.route('/api/reviews/<int:review_id>/like', methods=['POST'])
    @login_required
    def like_review(review_id):
        review = Review.query.get_or_404(review_id)
        review.likes += 1
        db.session.commit()
        return jsonify({'message': '点赞成功', 'likes': review.likes})
    
    # 踩评论
    @app.route('/api/reviews/<int:review_id>/dislike', methods=['POST'])
    @login_required
    def dislike_review(review_id):
        review = Review.query.get_or_404(review_id)
        review.dislikes += 1
        db.session.commit()
        return jsonify({'message': '踩成功', 'dislikes': review.dislikes})
    
    # 获取评论点赞/踩数量
    @app.route('/api/reviews/<int:review_id>/reactions', methods=['GET'])
    def get_review_reactions(review_id):
        review = Review.query.get_or_404(review_id)
        return jsonify({
            'likes': review.likes,
            'dislikes': review.dislikes
        })
    
    # 获取按照点赞数量排序的前十条结论
    @app.route('/api/reviews/top', methods=['GET'])
    def get_top_reviews():
        reviews = Review.query.order_by(Review.likes.desc()).limit(10).all()
        return jsonify([{
            'id': r.id,
            'score': r.score,
            'comment': r.comment, 
            'created_at': r.created_at,
            'teacher_name': r.teacher_name,
            'department': r.department,
            'likes': r.likes,
            'dislikes': r.dislikes
        } for r in reviews])
    
    # 获取最新的十条评价
    @app.route('/api/reviews/latest', methods=['GET'])
    def get_latest_reviews():
        reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
        return jsonify([{
            'id': r.id,
            'score': r.score,
            'comment': r.comment, 
            'created_at': r.created_at,
            'teacher_name': r.teacher_name,
            'department': r.department,
            'likes': r.likes,
            'dislikes': r.dislikes
        } for r in reviews])
    
    # 取消点赞评论
    @app.route('/api/reviews/<int:review_id>/unlike', methods=['POST'])
    @login_required
    def unlike_review(review_id):
        review = Review.query.get_or_404(review_id)
        review.likes -= 1
        db.session.commit()
        return jsonify({'message': '取消点赞成功', 'likes': review.likes})
    
    # 取消踩评论
    @app.route('/api/reviews/<int:review_id>/undislike', methods=['POST'])
    @login_required
    def undislike_review(review_id):
        review = Review.query.get_or_404(review_id)
        review.dislikes -= 1
        db.session.commit()
        return jsonify({'message': '取消踩成功', 'dislikes': review.dislikes})
    