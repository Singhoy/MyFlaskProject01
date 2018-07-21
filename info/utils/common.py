import functools

from flask import session, g


def func_out(f):
    @functools.wraps(f)
    def func_in(*args, **kwargs):
        # 获取到当前登录用户的id
        user_id = session.get("user_id")
        # 通过id获取用户信息
        user = None
        if user_id:
            from info.models import User
            user = User.query.get(user_id)

        g.user = user
        return f(*args, **kwargs)

    return func_in
