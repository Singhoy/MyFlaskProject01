from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from redis import StrictRedis

app = Flask(__name__)


class Config(object):
    """工程配置信息"""
    DEBUG = True

    # 数据库配置信息，mysql
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/news1"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # SECRET_KEY配置
    SECRET_KEY = "lafdkjflkdjflkadfjkadkjhfsakjdhfiandx"
    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_PERMANENT = False  # 如果设置为True，则关闭浏览器session就失效
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 86400  # session 的有效期，单位是秒


app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
CSRFProtect(app)
Session(app)

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    redis_store.set('hi', '1')
    print(redis_store.get('hi'))
    return 'index'


if __name__ == '__main__':
    manager.run()
