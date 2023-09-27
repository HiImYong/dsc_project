from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


# Flask 애플리케이션을 생성, __name__은 현재 모듈의 이름
app = Flask(__name__)

# app.config.from_object(Config): 애플리케이션의 설정을 Config 클래스로부터 가져온다.
app.config.from_object(Config)


db = SQLAlchemy(app)


migrate = Migrate(app, db)

from app import models
from app import routes