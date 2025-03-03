from flask import Blueprint

# 创建文章蓝本实例
articles_bp = Blueprint(
    'articles',  # 蓝本名称
    __name__,
    template_folder='templates/articles',  # 指定模板目录
    url_prefix='/articles'  # URL前缀
)

# 导入路由定义（必须放在最后避免循环引用）
from . import routes