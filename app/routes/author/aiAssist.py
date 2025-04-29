from flask import Blueprint, request, jsonify
from . import author_bp
from app.models import DBOperations
import os

DEEPSEEK_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

from openai import OpenAI

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

@author_bp.route("/llm", methods=['GET' ])
#@login_required
def AI_helper():
    data = request.get_json()
    
    try:
        operation = data['operation'] # 辅助扩写、分析文章 两类
        text = data['chapterContent']
        workTitle = data['workTitle']
        chapterTitle = data['chapterTitle']
        
    except:
        return jsonify(msg = 'Non valid input'), 400
    
    if not text or len(text) > 2000:
        return jsonify(msg = "The content length must between 1 and 2000"), 400
    
    
    prompt_template = {
        "analyze": "Please analyse the given passage in terms of the type of article, the language of the article and the flow of the article, around 100 words.No need to show the total number of words.\nThe article title is {workTitle} and the current chapter title is {chapterTitle}.\n{text}",
        "expand": "Please follow the logic of the given article to expand it by 500 words, which should be well-written and logical:\nThe article title is {workTitle} and the current chapter title is {chapterTitle}.\n{text}",
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
        
        return jsonify({"continueText": result})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500