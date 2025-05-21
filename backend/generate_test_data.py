import random
from datetime import datetime, timedelta
from faker import Faker
from app import create_app, db
from app.models import User, Teacher, Review
import config

# 初始化 Faker
fake = Faker('zh_CN')

def generate_users(num_users=50):
    """生成测试用户数据"""
    users = []
    used_usernames = set()  # 用于跟踪已使用的用户名
    
    for _ in range(num_users):
        while True:
            username = fake.user_name()
            if username not in used_usernames:  # 确保用户名唯一
                used_usernames.add(username)
                user = User(
                    username=username,
                    school=fake.company(),
                    password_hash=fake.password()
                )
                users.append(user)
                break
    
    return users

def generate_teachers(num_teachers=30):
    """生成测试教师数据"""
    departments = [
        '计算机科学与技术', '软件工程', '人工智能', '数据科学',
        '数学', '物理', '化学', '生物',
        '英语', '中文', '历史', '哲学',
        '经济', '管理', '金融', '会计'
    ]
    
    teachers = []
    for _ in range(num_teachers):
        teacher = Teacher(
            name=fake.name(),
            department=random.choice(departments)
        )
        teachers.append(teacher)
    return teachers

def generate_reviews(users, teachers, num_reviews=200):
    """生成测试评价数据"""
    reviews = []
    for _ in range(num_reviews):
        # 随机选择一个用户和教师
        user = random.choice(users)
        teacher = random.choice(teachers)
        
        # 生成评价内容
        review = Review(
            score=random.randint(1, 5),
            comment=fake.text(max_nb_chars=200),
            teacher_name=teacher.name,
            department=teacher.department,
            user_id=user.id,
            teacher_id=teacher.id,
            created_at=fake.date_time_between(start_date='-1y', end_date='now'),
            likes=random.randint(0, 50),
            dislikes=random.randint(0, 20)
        )
        reviews.append(review)
    return reviews

def main():
    """主函数：生成并添加测试数据"""
    app = create_app()
    
    with app.app_context():
        try:
            # 清空现有数据
            print("清空现有数据...")
            Review.query.delete()
            Teacher.query.delete()
            User.query.delete()
            db.session.commit()
            
            # 生成并添加用户数据
            print("生成用户数据...")
            users = generate_users()
            db.session.add_all(users)
            db.session.commit()
            
            # 生成并添加教师数据
            print("生成教师数据...")
            teachers = generate_teachers()
            db.session.add_all(teachers)
            db.session.commit()
            
            # 生成并添加评价数据
            print("生成评价数据...")
            reviews = generate_reviews(users, teachers)
            db.session.add_all(reviews)
            db.session.commit()
            
            print(f"成功添加 {len(users)} 个用户")
            print(f"成功添加 {len(teachers)} 个教师")
            print(f"成功添加 {len(reviews)} 条评价")
        except Exception as e:
            print(f"生成测试数据时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            db.session.rollback()  # 发生错误时回滚

if __name__ == '__main__':
    main() 