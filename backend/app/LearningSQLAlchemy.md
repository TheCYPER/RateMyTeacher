以下是 **SQL 语句与 Flask-SQLAlchemy ORM 的对照表**，结合你的 `User` 和 `Review` 模型，用实际场景示例说明：

---

### **基础操作对照表**
| SQL 语句 | SQLAlchemy ORM 写法 | 说明 |
|----------|----------------------|------|
| **创建表** | 自动通过模型类定义 | 无需手动写 `CREATE TABLE` |

---

### **插入数据**
#### SQL
```sql
INSERT INTO user (username) VALUES ('john');
```

#### SQLAlchemy
```python
new_user = User(username='john')
db.session.add(new_user)
db.session.commit()
```

---

### **查询数据**
#### 1. 查询所有记录
##### SQL
```sql
SELECT * FROM user;
```

##### SQLAlchemy
```python
users = User.query.all()  # 返回列表
```

#### 2. 条件查询
##### SQL
```sql
SELECT * FROM user WHERE username = 'john' LIMIT 1;
```

##### SQLAlchemy
```python
user = User.query.filter_by(username='john').first()
```

#### 3. 复合条件
##### SQL
```sql
SELECT * FROM review 
WHERE rating > 3 AND teacher_id = 1;
```

##### SQLAlchemy
```python
from sqlalchemy import and_

reviews = Review.query.filter(
    and_(Review.rating > 3, Review.teacher_id == 1)
).all()
```

---

### **更新数据**
#### SQL
```sql
UPDATE user SET username = 'john_new' WHERE id = 1;
```

#### SQLAlchemy
```python
user = User.query.get(1)  # 通过主键查询
user.username = 'john_new'
db.session.commit()
```

---

### **删除数据**
#### SQL
```sql
DELETE FROM user WHERE id = 1;
```

#### SQLAlchemy
```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

---

### **排序与分页**
#### SQL
```sql
SELECT * FROM review 
ORDER BY rating DESC 
LIMIT 5 OFFSET 10;
```

#### SQLAlchemy
```python
reviews = Review.query.order_by(Review.rating.desc())
                      .offset(10).limit(5).all()
```

---

### **聚合查询**
#### SQL
```sql
SELECT teacher_id, AVG(rating) 
FROM review 
GROUP BY teacher_id;
```

#### SQLAlchemy
```python
from sqlalchemy import func

result = db.session.query(
    Review.teacher_id,
    func.avg(Review.rating)
).group_by(Review.teacher_id).all()
```

---

### **联表查询**
#### SQL
```sql
SELECT user.username, review.rating 
FROM user 
JOIN review ON user.id = review.user_id;
```

#### SQLAlchemy
```python
result = db.session.query(User.username, Review.rating)
                  .join(Review, User.id == Review.user_id)
                  .all()
```

---

### **事务处理**
#### SQL
```sql
BEGIN TRANSACTION;
INSERT INTO user (username) VALUES ('john');
INSERT INTO review (user_id, rating) VALUES (1, 5);
COMMIT;
```

#### SQLAlchemy
```python
try:
    user = User(username='john')
    db.session.add(user)
    db.session.flush()  # 获取生成的user.id
    
    review = Review(user_id=user.id, rating=5)
    db.session.add(review)
    
    db.session.commit()
except:
    db.session.rollback()
```

---

### **原生 SQL 执行**
```python
# 执行复杂 SQL 的终极方案
sql = "SELECT * FROM user WHERE username LIKE '%john%'"
result = db.session.execute(sql).fetchall()
```

---

### **关键差异总结**
| 特性         | 原生 SQL                 | SQLAlchemy ORM           |
|--------------|-------------------------|--------------------------|
| 安全性       | 需手动防注入             | 自动参数化查询防注入      |
| 可读性       | 字符串拼接难维护         | Python 对象操作更直观     |
| 数据库兼容性 | 依赖特定数据库语法       | 支持多种数据库方言        |
| 调试难度     | 需单独打印 SQL           | 可通过 `echo=True` 输出   |

---

在你的项目中，优先使用 ORM 方法，只有遇到极端性能需求时再考虑原生 SQL。可以通过以下方式查看 ORM 实际生成的 SQL：
```python
query = User.query.filter_by(username='john')
print(str(query))  # 输出: SELECT user.id AS user_id ...
```