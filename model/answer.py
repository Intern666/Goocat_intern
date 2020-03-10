# encoding: utf-8

import time
from decorators import login_required
from flask import Blueprint, render_template, request, url_for, session, redirect
import dbhelper

answer_blu = Blueprint('answer', __name__)


@answer_blu.route('/detail/<question_id>/')
def detail(question_id):
    """
    问题细节函数，返回问题，该问题所有答案，答案数
    :param question_id:
    :return:
    """
    question = dbhelper.fetch_questions_by_questionid(question_id)
    answers = dbhelper.fetch_answers_by_questionid(question_id)
    answer_count = dbhelper.answer_count(question_id)
    return render_template('detail.html', question=question, answers=answers, answer_count=answer_count)


@answer_blu.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    """
    添加回答函数，返回回答内容，问题id，作者idr
    :return:
    """
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    author_id = session['user_id']
    # 获取当前时间对应时间戳
    # create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 插入一条回答
    if content != '':
        temp = dbhelper.fetch_user_by_id(author_id)
        if temp['UserMute'] == '1':
            # print('禁言用户非法访问！')
            return redirect(url_for('answer.detail', question_id=question_id))
        dbhelper.insert_answer(content, question_id, author_id)
    return redirect(url_for('answer.detail', question_id=question_id))