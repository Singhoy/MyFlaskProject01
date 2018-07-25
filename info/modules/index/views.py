from info import constants
from info.models import News, Category
from info.utils.common import func_out
from info.utils.response_code import RET
from . import index_blu
from flask import render_template, current_app, session, request, jsonify, g


# 新闻列表
@index_blu.route('/news_list')
def get_news_list():
    """
    获取指定分类的新闻列表
    1. 获取参数
    2. 校验参数
    3. 查询数据
    4. 返回数据
    """

    # 1. 获取参数
    args_dict = request.args
    page = args_dict.get("page", '1')
    per_page = args_dict.get("per_page", constants.HOME_PAGE_MAX_NEWS)
    category_id = args_dict.get("cid", '1')

    # 2.校验参数
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 3.查询数据并分页
    filters = [News.status == 0]
    # 如果分类id不为1，那么添加分类id的过滤
    if category_id != "1":
        filters.append(News.category_id == category_id)
    try:
        res = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")
    finally:
        # 获取查询出来的数据
        items = res.items
        # 获取到总页数
        totalPage = res.pages
        currentPage = res.page

    news_li = []
    for news in items:
        news_li.append(news.to_basic_dict())

    # 4.返回数据
    return jsonify(errno=RET.OK,
                   errmsg="查询成功",
                   totalPage=totalPage,
                   currentPage=currentPage,
                   newsList=news_li,
                   cid=category_id)


# 根路由
@index_blu.route('/')
@func_out
def index():
    # # 获取到当前登录用户的id
    # user_id = session.get("user_id")
    # # 通过id获取用户信息
    # user = None
    # if user_id:
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)

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
        "user_info": g.user.to_dict() if g.user else None,
        "click_news_list": click_news_list,
        "categories": categories_dicts
    }

    return render_template('news/index.html', data=data)


@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
