from app import create_app, db
from app.models import User, Teacher, Review
import os

app = create_app()

def init_db():
    with app.app_context():
        # 检查数据库是否为空
        if User.query.count() == 0:
            print("数据库为空，开始生成测试数据...")
            from generate_test_data import main
            main()
            print("测试数据生成完成！")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
