from flask import Blueprint, request, render_template, session, redirect, url_for
from decorators import login_required
import dbhelper
import pdb

person_blu = Blueprint('person', __name__)


@person_blu.route('/person_info/', methods=['GET', 'POST'])
@login_required
def person_info():
    """
    获取本人用户信息
    :return:person_info.html 并传入用户信息
    """
    author_id = session.get('user_id')
    user = dbhelper.fetch_user_by_id(author_id)
    questions = dbhelper.fetch_questions_by_userid(author_id)
    answers = dbhelper.fetch_answers_by_userid(author_id)
    context = {
        'id': author_id,
        'username': user.get('UserName'),
        'email': user.get('UserEmail'),
        'school': user.get('UserSchool'),
        'gender': user.get('UserGender'),
        'questions': questions,
        'answers': answers

    }
    return render_template('person_info.html', **context)


@person_blu.route('/person_questions/', methods=['GET', 'POST'])
@login_required
def person_questions():
    """
    获取本人提的问题
    :return: person_questions.html并传入问题和答案
    """
    author_id = session.get('user_id')
    user = dbhelper.fetch_user_by_id(author_id)
    questions = dbhelper.fetch_questions_by_userid(author_id)
    answers = dbhelper.fetch_answers_by_userid(author_id)
    context = {
        'id': author_id,
        'username': user.get('UserName'),
        'questions': questions,
        'answers': answers

    }
    return render_template('person_questions.html', **context)


@person_blu.route('/person_answers/', methods=['GET', 'POST'])
@login_required
def person_answers():
    """
    获取本人回答的答案
    :return: person_questions.html并传入问题和答案
    """
    author_id = session.get('user_id')
    user = dbhelper.fetch_user_by_id(author_id)
    questions = dbhelper.fetch_questions_by_userid(author_id)
    answers = dbhelper.fetch_answers_by_userid(author_id)
    context = {
        'id': author_id,
        'username': user.get('UserName'),
        'questions': questions,
        'answers': answers

    }
    return render_template('person_answers.html', **context)


@person_blu.route('/person_info_update/', methods=['GET', 'POST'])
@login_required
def person_info_update():
    """
    更新用户信息，根据前端传入的信息更新用户信息
    :return:如果有重复，显示提示语，并继续修改，如果修改成功返回用户信息页面
    """
    if request.method == 'GET':
        return render_template('person_info.html')
    else:
        author_id = session.get('user_id')
        email = request.form.get('email')
        username = request.form.get('username')
        gender = request.form.get('gender')
        school = request.form.get('school')
        if email == '' or username == '' or gender == '' or school == '':
            return render_template('person_info_update.html', error='输入有误，请重新输入！')
        user = dbhelper.fetch_user_by_email(email)
        if user and user[0].get('id') != author_id:
            return render_template('person_info_update.html', error_email='该邮箱被注册，请更换邮箱！')
        else:
            dbhelper.update_user_by_userid(author_id, email, username, gender, school)
            return redirect(url_for('person.person_info'))
            # return render_template('person_info.html')


@person_blu.route('/person_info_update_test/', methods=['GET', 'POST'])
@login_required
def person_info_update_test():
    """
    获取当前用户信息
    :return:更新页面
    """
    user_id = session.get('user_id')
    user = dbhelper.fetch_user_by_id(user_id)
    return render_template('person_info_update.html', user=user)
