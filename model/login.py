# encoding: utf-8
from flask import Blueprint, request, render_template, session, redirect, url_for, flash

import dbhelper

login_blu = Blueprint('login', __name__)


@login_blu.route('/regist/', methods=['GET', 'POST'])
def regist():
    """
    注册函数，检测，返回用户名，email，密码
    :return:
    """
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if email=='' or username =='' or password1 =='' or password2 =='':
            return render_template('regist.html',  error='输入有误，请重新输入！')
        user = dbhelper.fetch_user_by_email(email)
        # 手机号码验证，如果被注册了就不能用了
        if user:
            return render_template('regist.html', error_email='该邮箱被注册，请更换邮箱！')
        else:
        # password1 要和password2相等才可以
            if password1 != password2:
                return render_template('regist.html', eassword='两次密码不相等，请核实后再填写')
            else:
                dbhelper.insert_user(email, username, password1)
                flash("注册成功！")
                return redirect(url_for('login.login'))


@login_blu.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登陆函数，检测，返回用户名，密码
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        if email == '' or password == '':
            return render_template('login.html',  error='输入有误，请重新输入！')

        # 根据邮箱和密码查找表中是否有对应的user
        user = dbhelper.fetch_user_by_email_and_password(email, password)
        if user:
            if user.get("UserStatus")=='2':
                return render_template('login.html',  error='该用户已被禁用！')
            session['user_id'] = user.get("id")
            # 如果想在31天内都不需要登录
            session.permanent = True
            flash("您已经成功登陆！")
            return redirect(url_for('index'))
        else:
            return render_template('login.html',  error='邮箱地址或者密码错误，请确认好再登录')


@login_blu.route('/logout/')
def logout():
    """
    退出函数，清除session
    :return:
    """
    session.clear()
    return redirect(url_for('login.login'))
