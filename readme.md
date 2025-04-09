# Novel Heaven

## How to start
### 1. 克隆代码仓库
```
git clone https://github.com/your-repo/novel_heaven.git
cd novel_heaven
```

### 2. 安装依赖
```
pip install -r requirements.txt
```

### 3. 进入Python交互环境
```
flask shell
```

### 4. 执行本地数据库创建初始化命令（在打开的Python环境中）
```
from app.models import db
db.create_all()
exit()
```

### 5. 运行app
```
python run.py
```

## Useful information
### 1. Flask Tut
```
https://tutorial.helloflask.com/
```

### 2. framework update
see ./doc/framework.md