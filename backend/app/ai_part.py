import requests
import json
from flask import jsonify

def get_ai_summary(teacher_name, department, reviews):
    """
    使用Ollama模型生成教师评价的AI总结
    
    Args:
        teacher_name: 教师姓名
        department: 院系
        reviews: 评价列表
        
    Returns:
        AI生成的总结文本
    """
    # 构建提示词
    prompt = f"请对{department}的{teacher_name}老师的评价进行总结。以下是学生的评价：\n\n"
    
    for review in reviews:
        prompt += f"评分：{review.score}/5，评价：{review.comment}\n"
    
    prompt += "\n请总结这些评价，包括：1. 总体评分 2. 主要优点 3. 主要缺点 4. 学生普遍反馈 5. 建议"
    
    # 调用Ollama API
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "huihui_ai/gemma3-abliterated:1b",  # 使用您部署的模型名称
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "无法生成AI总结")
        else:
            return f"AI服务错误: {response.status_code}"
    except Exception as e:
        return f"AI服务异常: {str(e)}"

def init_ai_routes(app):
    """初始化AI相关路由"""
    
    @app.route('/api/teachers/<int:teacher_id>/ai-summary', methods=['GET'])
    def get_teacher_ai_summary(teacher_id):
        """获取教师的AI总结"""
        from .models import Teacher, Review
        
        teacher = Teacher.query.get_or_404(teacher_id)
        reviews = Review.query.filter_by(teacher_id=teacher_id).all()
        
        if not reviews:
            return jsonify({"error": "该教师暂无评价"}), 404
            
        summary = get_ai_summary(teacher.name, teacher.department, reviews)
        return jsonify({"summary": "省流：" + summary}) 
    