from flask import g, redirect, render_template

from info.utils.common import func_out
from . import profile_blu


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
