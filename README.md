# RateMyTeacher - 教师评价平台

   <div align="center">
     <img src="./logo.png" alt="RateMyTeacher Logo" width="250"/>
    <br>
     <p>
       <b>RateMyTeacher</b> - 一个让学生评价教师的平台
     </p>
   </div>

## 项目简介 | Project Introduction

RateMyTeacher 是一个基于 Flask 和 Vue.js 的教师评价平台，允许学生对自己喜欢的老师进行评价和打分。当评价数量达到一定阈值时，系统会自动将教师添加到数据库中，并生成 AI 总结。

RateMyTeacher is a teacher rating platform based on Flask and Vue.js, allowing students to rate and review their favorite teachers. When the number of reviews reaches a certain threshold, the system automatically adds the teacher to the database and generates an AI summary.

## 功能特点 | Features

- 👤 **用户系统** | **User System**
  - 用户注册和登录 | User registration and login
  - 个人资料管理 | Personal profile management

- 👨‍🏫 **教师评价** | **Teacher Rating**
  - 评价教师 | Rate teachers
  - 查看教师详情 | View teacher details
  - 自动添加教师 | Automatic teacher addition

- 💬 **评论系统** | **Review System**
  - 发表评论 | Post reviews
  - 点赞和踩功能 | Like and dislike functionality
  - 查看评论历史 | View review history

- 🤖 **AI 总结** | **AI Summary**
  - 基于 Ollama 的 AI 总结 | Ollama-based AI summary
  - 智能分析评价 | Intelligent review analysis

- 🔍 **搜索功能** | **Search Functionality**
  - 搜索教师 | Search for teachers
  - 搜索评论 | Search for reviews

## 技术栈 | Tech Stack

### 后端 | Backend
- Python 3.8+
- Flask
- SQLite
- SQLAlchemy
- Flask-Login
- Ollama

### 前端 | Frontend
- Vue.js
- Vue Router
- Vuex
- Axios
- Element UI
- Vuetify

## 安装说明 | Installation

### 前提条件 | Prerequisites
- Python 3.8+
- Node.js 14+
- Ollama with [huihui_ai/gemma3-abliterated:1b](https://huggingface.co/huihui-ai/gemma-3-1b-it-abliterated)

### 后端安装 | Backend Installation

```bash
# 克隆仓库 | Clone repository
git clone https://github.com/TheCYPER/RateMyTeacher.git
cd RateMyTeacher

# 创建虚拟环境 | Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 | or
venv\Scripts\activate  # Windows

# 安装依赖 | Install dependencies
pip install -r requirements.txt

# 运行后端 | Run backend
python backend/run.py
```

### 前端安装 | Frontend Installation

```bash
# 进入前端目录 | Enter frontend directory
cd frontend

# 安装依赖 | Install dependencies
npm install

# 运行开发服务器 | Run development server
npm run serve
```

## 使用方法 | Usage

1. **注册/登录** | **Register/Login**
   - 访问首页 | Visit homepage
   - 点击"注册"或"登录" | Click "Register" or "Login"

2. **评价教师** | **Rate Teachers**
   - 搜索教师 | Search for a teacher
   - 点击"评价"按钮 | Click "Rate" button
   - 填写评分和评论 | Fill in rating and review

3. **查看教师详情** | **View Teacher Details**
   - 点击教师名称 | Click on teacher name
   - 查看评价和 AI 总结 | View reviews and AI summary

4. **点赞/踩评论** | **Like/Dislike Reviews**
   - 在评论下方点击"点赞"或"踩" | Click "Like" or "Dislike" below reviews

## 项目结构 | Project Structure

```
RateMyTeacher/
├── backend/                # 后端代码 | Backend code
│   ├── app/                # 应用代码 | Application code
│   │   ├── models.py       # 数据模型 | Data models
│   │   ├── routes/         # 路由 | Routes
│   │   │   ├── user_routes.py    # 用户路由 | User routes
│   │   │   ├── teacher_routes.py # 教师路由 | Teacher routes
│   │   │   └── review_routes.py  # 评价路由 | Review routes
│   │   ├── ai_part.py      # AI 功能 | AI features
│   │   └── __init__.py     # 初始化 | Initialization
│   ├── config.py           # 配置文件 | Configuration
│   └── run.py              # 运行脚本 | Run script
├── frontend/               # 前端代码 | Frontend code
│   ├── src/                # 源代码 | Source code
│   ├── public/             # 公共资源 | Public resources
│   └── package.json        # 依赖配置 | Dependency configuration
└── README.md               # 项目说明 | Project description
```

## 贡献指南 | Contributing

欢迎贡献代码！请遵循以下步骤 | Welcome to contribute! Please follow these steps:

1. Fork 仓库 | Fork the repository
2. 创建功能分支 | Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 提交更改 | Commit your changes (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 | Push to the branch (`git push origin feature/amazing-feature`)
5. 创建 Pull Request | Create a Pull Request

## 许可证 | License

本项目采用 MIT 许可证 | This project is licensed under the MIT License - 查看 [LICENSE](LICENSE) 文件了解详情 | see the [LICENSE](LICENSE) file for details.

## 联系方式 | Contact

- 项目链接 | Project Link: [https://github.com/TheCYPER/RateMyTeacher](https://github.com/TheCYPER/RateMyTeacher)
- 问题反馈 | Issue Tracker: [https://github.com/TheCYPER/RateMyTeacher/issues](https://github.com/TheCYPER/RateMyTeacher/issues)

---

<div align="center">
  <p>Made with ❤️ by TheCYPER & Sugerbaby</p>
</div>
