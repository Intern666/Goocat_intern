# encoding: utf-8

from functools import wraps
from flask import session, redirect, url_for, flash

# 登录限制的装饰器

import dbhelper


def login_required(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            flash("请登录后再试！")
            return redirect(url_for('login.login'))

    return decorate


def admin_required(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            user = dbhelper.fetch_user_by_id(user_id)
            if user.get("UserStatus") == '1':
                return func(*args, **kwargs)
        else:
            flash("请登录后再试！")
            return redirect(url_for('login.login'))

    return decorate
