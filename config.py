import logging
from redis import StrictRedis


class Config(object):
    """工程配置信息"""
    # SECRET_KEY配置
    SECRET_KEY = "lafdkjflkdjflkadfjkadkjhfsakjdhfiandx"

    # 数据库配置信息，mysql
    SQLALCHEMY_DATABASE_URI = "mysql://rot:myihunsql@127.0.0.1:3306/news1"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_PERMANENT = False  # 如果设置为True，则关闭浏览器session就失效
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 86400  # session 的有效期，单位是秒

    # 默认日志等级
    LOG_LEVEL = logging.DEBUG


class DevelopementConfig(Config):
    """开发模式下的配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产模式下的配置"""
    LOG_LEVEL = logging.ERROR


# 定义配置字典
config = {
    "dev": DevelopementConfig,
    "pro": ProductionConfig
}
