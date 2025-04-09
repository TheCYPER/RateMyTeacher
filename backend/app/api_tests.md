# RateMyTeacher API 测试文档

## 基础信息
- 基础URL: `http://localhost:5000`
- 所有POST请求需要设置 `Content-Type: application/json`

## 用户相关接口

### 1. 用户注册
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass",
    "school": "测试大学"
  }'
```

### 2. 用户登录
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass"
  }'
```

### 3. 获取用户信息
```bash
curl -X GET http://localhost:5000/api/user/1
```

### 4. 更新用户信息
```bash
curl -X PUT http://localhost:5000/api/user/1 \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newusername"
  }'
```

## 教师相关接口

### 1. 获取教师列表
```bash
curl -X GET http://localhost:5000/api/teachers
```

### 2. 获取教师统计信息
```bash
curl -X GET http://localhost:5000/api/teachers/1/stats
```

### 3. 添加教师
```bash
curl -X POST http://localhost:5000/api/teachers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张老师",
    "department": "计算机学院"
  }'
```

### 4. 获取教师详情
```bash
curl -X GET http://localhost:5000/api/teachers/1
```

### 5. 搜索教师
```bash
curl -X GET "http://localhost:5000/api/search?q=张"
```

## 评价相关接口

### 1. 添加评价
```bash
curl -X POST http://localhost:5000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "score": 5,
    "comment": "老师讲课很好",
    "teacher_name": "张老师",
    "department": "计算机学院",
    "user_id": 1
  }'
```

### 2. 获取教师评价
```bash
curl -X GET http://localhost:5000/api/reviews/1
```

### 3. 获取用户评价
```bash
curl -X GET http://localhost:5000/api/user/reviews/1
```

### 4. 点赞评价
```bash
curl -X POST http://localhost:5000/api/reviews/1/like
```

### 5. 踩评价
```bash
curl -X POST http://localhost:5000/api/reviews/1/dislike
```

### 6. 获取评价反应
```bash
curl -X GET http://localhost:5000/api/reviews/1/reactions
```

## AI相关接口

### 1. 获取教师AI总结
```bash
curl -X GET http://localhost:5000/api/teachers/1/ai-summary
```

## 注意事项
1. 所有需要登录的接口（带有 `@login_required` 装饰器的接口）需要先登录获取 session
2. 测试时请确保数据库中有相应的测试数据
3. 部分接口可能需要特定的权限才能访问
4. 建议按顺序测试接口，因为某些接口依赖于其他接口的数据 