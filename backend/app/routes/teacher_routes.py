from flask import request, jsonify, session
from flask_login import login_required, current_user
from app import db
from app.models import Teacher, Review, User
from sqlalchemy import func

def check_and_add_teacher(teacher_name, department):
    # 获取未关联教师的评价数量
    review_count = Review.query.filter_by(
        teacher_name=teacher_name,
        department=department,
        teacher_id=None
    ).count()
    
    # 如果评价数达到5个，自动添加教师
    if review_count >= 5:
        # 检查教师是否已存在
        existing_teacher = Teacher.query.filter_by(name=teacher_name, department=department).first()
        if existing_teacher:
            # 关联未关联的评价
            Review.query.filter_by(teacher_name=teacher_name, department=department, teacher_id=None).update(
                {Review.teacher_id: existing_teacher.id}
            )
            db.session.commit()
            return existing_teacher
        else:
            # 创建新教师
            new_teacher = Teacher(name=teacher_name, department=department)
            db.session.add(new_teacher)
            db.session.commit()
            
            # 关联未关联的评价
            Review.query.filter_by(teacher_name=teacher_name, department=department, teacher_id=None).update(
                {Review.teacher_id: new_teacher.id}
            )
            db.session.commit()
            return new_teacher
    return None

def init_teacher_routes(app):
    # 获取教师列表
    @app.route('/api/teachers', methods=['GET'])
    def get_teachers():
        teachers = Teacher.query.all()
        return jsonify([{
            'id': teacher.id,
            'name': teacher.name,
            'department': teacher.department,
            'review_count': len(teacher.ratings)
        } for teacher in teachers])
    
    # 搜索教师
    @app.route('/api/teachers/search', methods=['GET'])
    def search_teachers():
        query = request.args.get('q', '')
        if not query:
            return jsonify([])
            
        teachers = Teacher.query.filter(
            Teacher.name.ilike(f'%{query}%') | 
            Teacher.department.ilike(f'%{query}%')
        ).all()
        
        return jsonify([{
            'id': t.id,
            'name': t.name,
            'department': t.department,
            'review_count': len(t.ratings)
        } for t in teachers])
    
    # 教师评价统计接口
    @app.route('/api/teachers/<int:teacher_id>/stats', methods=['GET'])
    def get_teacher_stats(teacher_id):
        teacher = Teacher.query.get_or_404(teacher_id)
        reviews = Review.query.filter_by(teacher_id=teacher_id).all()
        
        # 计算统计信息
        total_reviews = len(reviews)
        if total_reviews == 0:
            avg_score = 0
        else:
            avg_score = sum(r.score for r in reviews) / total_reviews
            
        return jsonify({
            'total_reviews': total_reviews,
            'average_score': round(avg_score, 1)
        })

    # 添加教师接口
    @app.route('/api/teachers', methods=['POST'])
    @login_required
    def add_teacher_api():
        data = request.get_json()
        name = data.get('name')
        department = data.get('department')
        
        if not name or not department:
            return jsonify({'error': '教师姓名和院系不能为空'}), 400
            
        # 检查教师是否已存在
        existing_teacher = Teacher.query.filter_by(name=name, department=department).first()
        if existing_teacher:
            return jsonify({'message': '教师已存在', 'id': existing_teacher.id}), 200
            
        # 创建新教师
        new_teacher = Teacher(name=name, department=department)
        db.session.add(new_teacher)
        db.session.commit()
        
        # 关联未关联的评价
        Review.query.filter_by(teacher_name=name, department=department, teacher_id=None).update(
            {Review.teacher_id: new_teacher.id}
        )
        db.session.commit()
        
        return jsonify({'message': '教师添加成功', 'id': new_teacher.id}), 201

    # 获取教师详情
    @app.route('/api/teachers/<int:teacher_id>', methods=['GET'])
    def get_teacher(teacher_id):
        teacher = Teacher.query.get_or_404(teacher_id)
        return jsonify({
            'id': teacher.id,
            'name': teacher.name,
            'department': teacher.department,
            'review_count': len(teacher.ratings)
        })

    # 获取教师评价列表
    @app.route('/api/teachers/<int:teacher_id>/reviews', methods=['GET'])
    def get_teacher_reviews(teacher_id):
        teacher = Teacher.query.get_or_404(teacher_id)
        reviews = []
        for rating in teacher.ratings:
            reviews.append({
                'id': rating.id,
                'content': rating.comment,
                'rating': rating.score,
                'created_at': rating.created_at.isoformat(),
                'reviewer_name': rating.user.username,
                'likes': rating.likes,
                'dislikes': rating.dislikes,
                'user_liked': False,
                'user_disliked': False
            })
        
        # 按创建时间倒序排序
        reviews.sort(key=lambda x: x['created_at'], reverse=True)
        return jsonify(reviews)

    # 搜索教师
    @app.route('/api/search', methods=['GET'])
    def search():
        query = request.args.get('q', '')
        teachers = Teacher.query.filter(
            Teacher.name.ilike(f'%{query}%') | 
            Teacher.department.ilike(f'%{query}%')
        ).all()
        
        return jsonify([{
            'id': t.id,
            'name': t.name,
            'department': t.department,
            'review_count': len(t.ratings)
        } for t in teachers]) 