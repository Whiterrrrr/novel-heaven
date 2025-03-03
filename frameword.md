/novel_heaven
  ├── app/
  │   ├── __init__.py
  │   ├── models.py
  │   ├── routes/
  │   │   ├── auth/
  │   │   │   ├── __init__.py
  │   │   │   ├── routes.py
  │   │   │   └── forms.py
  │   │   ├── articles/
  │   │   │   ├── __init__.py
  │   │   │   ├── routes.py
  │   │   │   └── forms.py
  │   │   └── main/
  │   │       ├── __init__.py
  │   │       └── routes.py
  │   ├── templates/
  │   │   ├── base.html
  │   │   ├── auth/
  │   │   │   ├── login.html
  │   │   │   └── register.html
  │   │   ├── articles/
  │   │   |   ├── publish.html
  │   │   |   └── article.html
  |   |   └── main/
  │   │       ├── dashboard.html
  │   │       └── index.html
  │   └── static/
  │       ├── css/
  │       │   └── main.css
  │       └── js/
  │           └── main.js
  ├── config.py
  └── run.py

前端需要负责的页面：
1. 主页面index.html，有登录选项
2. 用户登录页面：登录成功，登录失败重新登录
3. 书架页面
4. 书籍搜索
5. 