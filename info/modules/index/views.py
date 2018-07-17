from info import constants
from info.models import User, News, Category
from . import index_blu
from flask import render_template, current_app, session


# 根路由
@index_blu.route('/')
def index():
    # 获取到当前登录用户的id
    user_id = session.get("user_id")
    # 通过id获取用户信息
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 获取点击排行数据
    news_list = None
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for news in news_list if news_list else []:
        click_news_list.append(news.to_basic_dict())

    # 获取新闻分类数据
    categories = Category.query.all()
    # print(type(categories))   # <class 'list'>

    # 定义列表保存分类数据
    categories_dicts = []

    for category in enumerate(categories):
        # print(type(category))   # <class 'tuple'>
        # 拼接内容
        a, b = category  # category是一个元组
        # print(b.to_dict())  # b是class 'info.models.Category'
        categories_dicts.append(b.to_dict())

    data = {
        "user_info": user.to_dict() if user else None,
        "click_news_list": click_news_list,
        "categories": categories_dicts
    }

    return render_template('news/index.html', data=data)


@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
