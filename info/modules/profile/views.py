from flask import g, redirect, render_template, request, jsonify, current_app, session

from info import db
from info.constants import QINIU_DOMIN_PREFIX, USER_COLLECTION_MAX_NEWS
from info.utils.common import func_out
from info.utils.image_storage import storage
from info.utils.response_code import RET
from . import profile_blu


# 新闻收藏
@profile_blu.route('/collection')
@func_out
def user_collection():
    # 获取页数
    p = request.args.get("p", 1)
    try:
        p = int(p)
    except Exception as e:
        current_app.logger.error(e)
        p = 1

    user = g.user
    collections = []
    current_page = 1
    total_page = 1
    try:
        # 进行分页数据查询
        paginate = user.collection_news.paginate(p, USER_COLLECTION_MAX_NEWS, False)
        # 获取分页数据
        collections = paginate.items
        # 获取当前页
        current_page = paginate.page
        # 获取总页数
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    # 收藏列表
    collection_dict_li = []
    for news in collections:
        collection_dict_li.append(news.to_basic_dict())

    data = {"total_page": total_page,
            "current_page": current_page,
            "collections": collection_dict_li}

    return render_template('news/user_collection.html', data=data)


# 修改用户密码
@profile_blu.route('/pass_info', methods=["GET", "POST"])
@func_out
def pass_info():
    if request.method == "GET":
        return render_template('news/user_pass_info.html')

    # 1.获取到传入的参数
    data_dict = request.json
    ole_password = data_dict.get("old_password")
    new_password = data_dict.get("new_password")

    if not all([ole_password, new_password]):
        return jsonify(errno=RET.PARAMERR, errmsg="all参数有误")

    # 2.获取当前登录用户的信息
    user = g.user

    if not user.check_passowrd(ole_password):
        return jsonify(errno=RET.PWDERR, errmsg="原密码错误")

    # 更新数据
    user.password = new_password
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")

    return jsonify(errno=RET.OK, errmsg="保存成功")


# 头像上传路由
@profile_blu.route('/pic_info', methods=["GET", "POST"])
@func_out
def pic_info():
    user = g.user
    if request.method == "GET":
        return render_template('news/user_pic_info.html', data={"user_info": user.to_dict()})

    # 1.获取到上传的文件
    try:
        avatar_file = request.files.get("avatar").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="读取文件出错")

    # 2.再将文件上传到七牛云
    try:
        url = storage(avatar_file)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传图片错误")

    # 3.将头像信息更新到当前用户的模型中
    # 设置用户模型相关数据
    user.avatar_url = url
    # 将数据保存到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存用户数据错误")

    # 4.返回上传的结果（avatar_url）
    return jsonify(errno=RET.OK, errmsg="上传成功", data={"avatar_url": QINIU_DOMIN_PREFIX + url})


# 用户基本信息路由
@profile_blu.route('/base_info', methods=["GET", "POST"])
@func_out
def base_info():
    """
    用户基本信息
    1. 获取用户登录信息
    2. 获取到传入参数
    3. 更新并保存数据
    4. 返回结果
    """

    # 1. 获取当前登录用户的信息
    user = g.user
    if request.method == "GET":
        return render_template('news/user_base_info.html', data={"user_info": user.to_dict()})

    # 2.获取到传入参数
    data_dict = request.json
    nick_name = data_dict.get("nick_name")
    gender = data_dict.get("gender")
    signature = data_dict.get("signature")
    if not all([nick_name, gender, signature]):
        return jsonify(errno=RET.PARAMERR, errmsg="all参数有误")

    if gender not in (['MAN', 'WOMAN']):
        return jsonify(errno=RET.PARAMERR, errmsg="gender参数有误")

    # 3.更新并保存数据
    user.nick_name = nick_name
    user.gender = gender
    user.signature = signature
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")

    # 将session中保存的数据进行实时更新
    session["nick_name"] = nick_name

    # 4.返回响应
    return jsonify(errno=RET.OK, errmsg="更新成功")


# 个人中心主页
@profile_blu.route('/info')
@func_out
def user_info():
    """
       获取用户信息
       1. 获取到当前登录的用户模型
       2. 返回模型中指定内容
    """

    user = g.user
    if not user:
        # 用户未登录，重定向到主页
        return redirect('/')

    data = {
        "user_info": user.to_dict()
    }

    # 渲染模板
    return render_template("news/user.html", data=data)
