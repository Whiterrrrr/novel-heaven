from flask import Blueprint, request, jsonify
from . import articles_bp
from app.models import DBOperations
import os
import requests

DEEPSEEK_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

from openai import OpenAI

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

@articles_bp.route("/aihelper", methods=['GET' ])
#@login_required
def AI_helper():
    data = request.get_json()
    
    try:
        operation = data['operation'] # 辅助扩写、分析文章 两类
        text = data['content']
    except:
        return jsonify(msg = 'Non valid input'), 400
    
    if not text or len(text) > 2000:
        return jsonify(msg = "The content length must between 1 and 2000"), 400
    
    
    prompt_template = {
        "analyze": "Please analyse the given passage in terms of the type of article, the language of the article and the flow of the article, around 100 words.No need to show the total number of words.\n{text}",
        "expand": "Please follow the logic of the given article to expand it by 500 words, which should be well-written and logical:\n{text}",
        }


    try:
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for helping me to creating or understanding an article"},
            {"role": "user", "content": prompt_template[operation].format(text=text)},
            ],
        stream=False
    )
        
        result = response.choices[0].message.content
        
        return jsonify({"result": result})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500