from flask import render_template, session, current_app, g

from info.models import User
from info.modules.news import news_blu
from info.utils.common import func_out


@news_blu.route('/<int:news_id>')
@func_out
def news_detail(news_id):
    # # 获取到当前登录用户的id
    # user_id = session.get("user_id")
    #
    # # 通过id获取用户信息
    # user = None
    # if user_id:
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)

    data = {
        "user_info": g.user.to_dict() if g.user else None
    }

    return render_template('news/detail.html', data=data)
