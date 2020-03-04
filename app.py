# encoding: utf-8
import os
import pdb
import time
import dbhelper
from decorators import login_required
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route('/', methods=["GET", "POST"])
def index():
    context = {
        'questions': dbhelper.fetch_all_questions()
    }
    return render_template('index.html', **context)


@app.route('/detail/<question_id>/')
def detail(question_id):
    question = dbhelper.fetch_questions_by_questionid(question_id)
    answers = dbhelper.fetch_answers_by_questionid(question_id)
    answer_count = dbhelper.answer_count(question_id)
    return render_template('detail.html', question=question, answers=answers, answer_count=answer_count)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    author_id = session['user_id']
    # 获取当前时间对应时间戳
    # create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 插入一条回答
    dbhelper.insert_answer(content, question_id, author_id)
    return redirect(url_for('detail', question_id=question_id))


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = dbhelper.fetch_user_by_email(email)
        # 手机号码验证，如果被注册了就不能用了
        if user:
            return u'该手机号码被注册，请更换手机'
        else:
            # password1 要和password2相等才可以
            if password1 != password2:
                return u'两次密码不相等，请核实后再填写'
            else:
                dbhelper.insert_user(email, username, password1)
                return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        # 根据邮箱和密码查找表中是否有对应的user
        user = dbhelper.fetch_user_by_email_and_password(email, password)
        if user:
            session['user_id'] = user[0].get("id")
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index', userid=user[0].get("id")))
        else:
            return u'手机号码或者密码错误，请确认好在登录'


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        author_id = session.get('user_id')
        dbhelper.insert_question(title, content, author_id)
        return redirect(url_for('index'))


@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        return render_template('index.html')
    else:
        search_key = request.form.get('search_key')
        # title, content
        # 或 查找方式（通过标题和内容来查找）
        questions = dbhelper.search_by_key(search_key)
        return render_template('index.html', questions=questions)


# 钩子函数(注销)
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = dbhelper.fetch_user_by_id(user_id)
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
