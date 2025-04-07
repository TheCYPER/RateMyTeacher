以下是一些适合初学者的 SQLite 基础操作示例，包含最常用的 SQL 语句。我们将以你的 `RateMyTeacher` 项目场景为基础设计示例：

---

### **1. 基础表操作**
#### 创建表
```sql
-- 创建教师表
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT
);

-- 创建评价表
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);
```

---

### **2. 插入数据**
```sql
-- 插入教师数据
INSERT INTO teachers (name, department)
VALUES 
    ('张三', '计算机科学'),
    ('李四', '数学');

-- 插入评价数据
INSERT INTO reviews (teacher_id, rating, comment)
VALUES
    (1, 5, '讲解清晰，作业合理'),
    (1, 4, '课堂节奏稍快'),
    (2, 3, '内容较难理解');
```

---

### **3. 查询数据**
#### 基础查询
```sql
-- 查询所有教师
SELECT * FROM teachers;

-- 查询计算机科学系的教师
SELECT name FROM teachers WHERE department = '计算机科学';

-- 查询评分4分及以上的评价
SELECT * FROM reviews WHERE rating >= 4;
```

#### 排序与限制
```sql
-- 按评分降序排列评价
SELECT * FROM reviews ORDER BY rating DESC;

-- 获取评分最高的前2条评价
SELECT * FROM reviews ORDER BY rating DESC LIMIT 2;
```

---

### **4. 更新与删除**
```sql
-- 将李四的部门改为"应用数学"
UPDATE teachers 
SET department = '应用数学' 
WHERE name = '李四';

-- 删除id为3的评价
DELETE FROM reviews WHERE id = 3;
```

---

### **5. 聚合查询**
```sql
-- 统计每位教师的平均评分
SELECT 
    t.name,
    AVG(r.rating) AS avg_rating,
    COUNT(r.id) AS review_count
FROM teachers t
LEFT JOIN reviews r ON t.id = r.teacher_id
GROUP BY t.id;

-- 结果示例：
-- 张三 | 4.5 | 2
-- 李四 | NULL | 0
```

---

### **6. 多表连接查询**
```sql
-- 查看评价详情（包含教师姓名）
SELECT 
    t.name AS teacher_name,
    r.rating,
    r.comment
FROM reviews r
JOIN teachers t ON r.teacher_id = t.id;
```

---

### **7. 实用技巧**
#### 事务处理
```sql
BEGIN TRANSACTION;
-- 执行多个操作...
INSERT INTO ...;
UPDATE ...;
COMMIT;
```

#### 导出数据
```bash
# 在终端执行
sqlite3 ratings.db ".dump" > backup.sql
```

---

### **测试建议**
1. 在 SQLite 命令行中逐步执行这些语句
2. 观察结果变化（可用 `.schema` 查看表结构，`.tables` 查看所有表）
3. 尝试修改条件（WHERE）、排序方式（ORDER BY）等参数
4. 故意制造错误（如插入不满足 CHECK 约束的数据）观察报错信息

---

### **SQL 学习要点**
| 操作类型 | 关键语法 | 常见用途 |
|----------|----------|----------|
| 数据查询 | `SELECT ... FROM ... WHERE` | 提取特定数据 |
| 数据插入 | `INSERT INTO ... VALUES` | 添加新记录 |
| 数据更新 | `UPDATE ... SET ... WHERE` | 修改现有数据 |
| 数据删除 | `DELETE FROM ... WHERE` | 移除记录 |
| 表管理 | `CREATE TABLE`, `ALTER TABLE` | 定义数据结构 |

建议配合 [SQLite 官方文档](https://www.sqlite.org/lang.html) 深入学习，后续可以尝试在你的 Flask 项目中通过 Python 执行这些 SQL 语句。