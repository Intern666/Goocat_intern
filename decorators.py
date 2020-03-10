#encoding: utf-8

from functools import wraps
from flask import session, redirect, url_for, flash


# 登录限制的装饰器
def login_required(func):
    """
    登录限制的装饰器
    :param func:
    :return:
    """
    @wraps(func)
    def decorate(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            flash("请登录后再试！")
            return redirect(url_for('login.login'))

    return decorate
