from flask import request, jsonify, session
from flask_login import login_user, login_required, current_user
from app import db
from app.models import User

def init_user_routes(app):
    # 注册接口
    @app.route('/register', methods=['POST'])
    def register():
        print("---- 收到注册请求 ----")
        data = request.get_json()
        print("请求数据:", data)  # 添加此行
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': '用户名已存在 请登陆'}), 400
        
        user = User(
            username=data['username'],
            school=data.get('school', '未知学校')  # 如果没有提供学校，使用默认值
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': '注册成功'})

    # 登录接口
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if user and user.check_password(data['password']):
            login_user(user, remember=True)  # 添加 remember=True
            session.permanent = True  # 设置会话持久化
            return jsonify({
                'message': '登录成功',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'school': user.school
                }
            })
        return jsonify({'error': '用户名或密码错误'}), 401

    # 测试保护接口
    @app.route('/protected')
    @login_required  # 确保用户已登录
    def protected():
        return jsonify({
            'message': '您已登录',
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'school': current_user.school
            }
        })

    # 获取用户信息
    @app.route('/api/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify({
            'id': user.id,
            'username': user.username,
            'school': user.school
            # 不返回密码等敏感信息
        })

    # 更新用户信息
    @app.route('/api/user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'username' in data:
            user.username = data['username']
        
        db.session.commit()
        return jsonify({'message': '更新成功'})

    # 通过用户名获取用户信息
    @app.route('/api/user/by-username/<username>', methods=['GET'])
    @login_required
    def get_user_by_username(username):
        user = User.query.filter_by(username=username).first_or_404()
        return jsonify({
            'id': user.id,
            'username': user.username,
            'school': user.school
        }) 