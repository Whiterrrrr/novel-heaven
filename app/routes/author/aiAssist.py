from flask import Blueprint, request, jsonify
from . import author_bp
from app.models import DBOperations
import os

DEEPSEEK_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
DEEPSEEK_API_KEY = "your api key"

from openai import OpenAI

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

@author_bp.route("/llm", methods=['POST' ])
#@login_required
def AI_helper():
    """
    AI assistant for expanding chapter content via LLM.
    """
    data = request.get_json()
    
    try:
        text = data['chapterContent']
        workTitle = data['workTitle']
        chapterTitle = data['chapterTitle']
        
    except:
        return jsonify(msg = 'Non valid input'), 400
    
    if not text or len(text) > 2000:
        return jsonify(msg = "The content length must between 1 and 2000"), 400
    
    
    prompt_template = {
        "analyze": f"Please analyse the given passage in terms of the type of article, the language of the article and the flow of the article, around 100 words.No need to show the total number of words.\nThe article title is {workTitle} and the current chapter title is {chapterTitle}.\n{text}",
        "expand": f"Please follow the logic of the given article to expand it by 500 words, which should be well-written and logical:\nThe article title is {workTitle} and the current chapter title is {chapterTitle}.\n{text}.Please give the expansion directly, without chapter title and any introductory sentences, e.g. Certainly! Here's a logical expansion of your chapter, etc.",
        }


    try:
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for helping me to creating or understanding an article"},
            {"role": "user", "content": prompt_template["expand"].format(text=text)},
            ],
        stream=False
    )
        
        result = response.choices[0].message.content
        print(result)
        return jsonify({"continuation": result})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500