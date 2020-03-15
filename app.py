# encoding: utf-8
import os
import dbhelper
from flask import Flask, render_template, session

from model.login import login_blu
from model.answer import answer_blu
from model.question import question_blu
from model.person import person_blu
from model.admin import admin_blu

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.register_blueprint(login_blu)
app.register_blueprint(question_blu)
app.register_blueprint(answer_blu)
app.register_blueprint(person_blu)
app.register_blueprint(admin_blu)


@app.route('/', methods=["GET", "POST"])
def index():
    """
    主页函数，显示全部问题
    :return: 主页信息和问题参数
    """
    context = {
        'questions': dbhelper.fetch_all_questions()
    }
    return render_template('index.html', **context)


@app.route('/firstpage', methods=["GET", "POST"])
def firstpage():
    """
    首页函数，显示网页主页
    :return: 返回首页网页
    """
    return render_template('firstpage.html')


# 钩子函数(注销)
@app.context_processor
def my_context_processor():
    """
    定义钩子函数，各页面间传递user信息
    :return: 登陆用户信息
    """
    user_id = session.get('user_id')
    if user_id:
        user = dbhelper.fetch_user_by_id(user_id)
        if user:
            if user.get("UserStatus") == '2':
                session.clear()
                return {}
            return {'user': user}
    return {}


if __name__ == '__main__':
    '''
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    '''
    app.run(debug=True)
