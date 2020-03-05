# encoding: utf-8

import time
from flask import Blueprint, request, render_template, session, url_for, redirect
import dbhelper
from decorators import login_required

question_blu = Blueprint('question', __name__)


@question_blu.route('/question/', methods=['GET', 'POST'])
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


@question_blu.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        return render_template('index.html')
    else:
        search_key = request.form.get('search_key')
        # title, content
        # 或 查找方式（通过标题和内容来查找）
        questions = dbhelper.search_by_key(search_key)
        return render_template('index.html', questions=questions, search_key=search_key)
