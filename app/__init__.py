from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Flask 애플리케이션을 생성, __name__은 현재 모듈의 이름
# Flask 클래스의 생성자에 현재 모듈의 이름을 전달하고 있습니다.
# 여기서 현재 모듈은 __init__.py 파일을 말합니다.
app = Flask(__name__)

app.config.from_object(Config)


db = SQLAlchemy(app)


migrate = Migrate(app, db)


"""
순환 참조 문제는 모듈이 아직 실행 중인데 이미 참조하려고 할 때 발생합니다. 
코드를 아래로 이동시켰습니다. 
app 모듈이 완전히 초기화된 후에 models 및 routes 모듈을 import하므로 순환 참조 문제를 피할 수 있습니다.
"""
from app import models
from app import routes