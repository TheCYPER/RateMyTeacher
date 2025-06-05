from app import create_app, db
from app.models import User, Teacher, Review
import os

app = create_app()

def init_db():
    with app.app_context():
        try:
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
        except Exception as e:
            print(f"初始化数据库时出错: {str(e)}")

# 在应用启动时初始化数据库
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
