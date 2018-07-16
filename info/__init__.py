from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from redis import StrictRedis

from config import Config

app = Flask(__name__)

# 配置
app.config.from_object(Config)
# mysql配置
db = SQLAlchemy(app)
# redis配置
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 开启csrf保护
CSRFProtect(app)
# 设置session保存位置
Session(app)
