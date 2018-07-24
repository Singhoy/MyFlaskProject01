from flask import render_template, request, current_app, session, g, redirect, url_for

from info.models import User
from info.utils.common import func_out
from . import admin_blu


# 管理员登录
@admin_blu.route('/login', methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        # 取session中取指定的值
        user_id = session.get("user_id", None)
        is_admin = session.get("is_admin", False)
        # 如果用户id存在，并且是管理员，那么直接跳转管理后台主页
        if user_id and is_admin:
            return redirect(url_for('admin.admin_index'))
        return render_template('admin/login.html')

    # 获取到登录的参数
    username = request.form.get("username")
    password = request.form.get("password")

    if not all([username, password]):
        return render_template('admin/login.html', errmsg="参数不足")

    try:
        user = User.query.filter(User.mobile == username).first()
    except Exception as e:
        current_app.logger.error(e)
        return render_template('admin/login.html', errmsg="数据查询失败")

    if not user:
        return render_template('admin/login.html', errmsg="用户不存在")

    if not user.check_passowrd(password):
        return render_template('admin/login.html', errmsg="密码错误")

    if not user.is_admin:
        return render_template('admin/login.html', errmsg="用户权限错误")

    session["user_id"] = user.id
    session["nick_name"] = user.nick_name
    session["mobile"] = user.mobile
    session["is_admin"] = True

    # 跳转到后台管理主页
    return redirect(url_for('admin.admin_index'))


# 管理后台主页
@admin_blu.route('/index')
@func_out
def admin_index():
    user = g.user
    return render_template('admin/index.html', user=user.to_dict())
