# encoding: utf-8

import time
from flask import Blueprint, request, render_template, session, url_for, redirect
import dbhelper
from decorators import login_required

question_blu = Blueprint('question', __name__)


@question_blu.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    """
    发布问题函数，返回问题标题，作者id，问题内容
    :return:
    """
    if request.method == 'GET':
        return render_template('question.html')
    else:
        author_id = session.get('user_id')
        temp = dbhelper.fetch_user_by_id(author_id)
        if temp['UserMute']=='1':
            # print('禁言用户非法访问！')
            return  render_template('question.html')

        title = request.form.get('title')
        content = request.form.get('content')
        dbhelper.insert_question(title, content, author_id)
        return redirect(url_for('index'))


@question_blu.route('/search/', methods=['GET', 'POST'])
def search():
    """
    关键词搜索函数，返回带关键词的所有提问s
    :return:
    """
    if request.method == "GET":
        return render_template('index.html')
    else:
        search_key = request.form.get('search_key')
        # title, content
        # 或 查找方式（通过标题和内容来查找）
        questions = dbhelper.search_by_key(search_key)
        return render_template('index.html', questions=questions, search_key=search_key)
