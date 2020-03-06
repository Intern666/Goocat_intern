# encoding: utf-8
import pymysql
import logging

config = {
    'host': '127.0.0.1',
    'port': 3307,
    'user': 'root',
    'passwd': 'Zhwlf1998',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


# 数据库连接
def connect():
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    cursor = conn.cursor()
    conn.select_db("goocat_intern")
    return conn, cursor


conn, cursor = connect()


def insert_user(email, username, password):
    """
    插入一条用户记录
    :param telephone:
    :param username:
    :param password:
    :return:
    """
    sql = "insert into user_info (UserEmail, UserName, UserPassword) " \
          "VALUES (%s, %s, %s)"
    args = (email, username, password)
    try:
        cursor.execute(sql, args)
        conn.commit()
    except Exception as e:
        logging.error(str(e))


def fetch_user_by_email(email):
    sql = "select * from user_info where UserEmail = %s"
    args = email
    cursor.execute(sql, args)
    user = cursor.fetchall()
    return user


def fetch_all_questions():
    """
    取到所有问题
    :return:问题列表，列表每一项是一个字典，对应question表中的属性
    """
    # sql = "select * from question order by create_time"
    # sql = "select a.`id`, a.`title`, a.`create_time`, a.`content`, b.`username` from question a " \
    #       "left join user b on a.`author_id`=b.`id` order by a.`create_time` desc"
    sql = "select a.`id`, a.`QuestionTitle`, a.`QuestionTime`, a.`QuestionContent`, b.`UserName`, a.`UserID`" \
          "from user_question a left join user_info b on a.`UserID`=b.`id` order by a.`QuestionTime` desc"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def fetch_questions_by_questionid(question_id):
    """
    通过questionid取得对应问题，理论上id为主键，唯一
    :param question_id:
    :return:问题id对应的问题
    """
    # sql = "select * from question where id=%s limit 1" % question_id
    # sql = "select a.`id`, a.`title`, a.`content`, a.`create_time`, b.`username` from question a " \
    #       "left join user b on a.`author_id` = b.`id` where a.`id`=%s limit 1"
    sql = "select a.`id`, a.`QuestionTitle`, a.`QuestionContent`, a.`QuestionTime`, b.`UserName`" \
          " from user_question a left join user_info b on a.`UserID` = b.`id` where a.`id`=%s limit 1"
    args = question_id
    cursor.execute(sql, args)
    rows = cursor.fetchall()
    question = rows[0]
    return question


def fetch_answers_by_questionid(question_id):
    """
    通过问题id取得对应的回答
    :param question_id:
    :return: 回答列表，列表中每一项是一个字典，对应answer表中的属性
    """
    # sql = "select * from answer where question_id=%s"
    # sql = "select a.`content`, a.`question_id`, a.`author_id`, a.`create_time`, b.`username` from answer a " \
    #       "left join user b on a.`author_id`=b.`id` where a.`question_id`=%s order by a.`create_time` desc"
    sql = "select a.`AnswerContent`, a.`QuestionID`, a.`UserID`, a.`AnswerTime`, b.`UserName` from user_answer a " \
          "left join user_info b on a.`UserID`=b.`id` where a.`QuestionID`=%s order by a.`AnswerTime` desc"
    args = question_id
    cursor.execute(sql, args)
    answers = cursor.fetchall()
    return answers


def insert_answer(content, question_id, author_id):
    """
    插入一条回答记录到answer表中
    :param content: 回答内容
    :param question_id: 问题id
    :param author_id: 作者id
    :return:
    """
    sql = "insert into user_answer (AnswerContent, QuestionID, UserID)" \
          " VALUES(%s, %s, %s)"
    args = (content, question_id, author_id)
    cursor.execute(sql, args)
    conn.commit()


def fetch_user_by_email_and_password(email, password):
    """
    通过邮箱和密码查询user表返回对应user
    :param email:
    :param password:
    :return:
    """
    sql = "select * from user_info where UserEmail=%s and UserPassword=%s"
    args = (email, password)
    cursor.execute(sql, args)
    user = cursor.fetchall()
    return user


def insert_question(title, content, author_id):
    """
    插入一条question记录
    :param title:
    :param content:
    :param author_id:
    :return:
    """
    sql = "insert into user_question (QuestionTitle, QuestionContent, UserID) " \
          "VALUES (%s, %s, %s)"
    args = (title, content, author_id)
    cursor.execute(sql, args)
    conn.commit()


def search_by_key(search_key):
    """
    根据key查找包含该key的问题
    :param search_key:
    :return:
    """
    # sql = "select * from user_question WHERE QuestionContent like %s or QuestionTitle like %s order by QuestionTime desc"
    sql = "select a.`id`, a.`QuestionTitle`, a.`QuestionContent`, a.`QuestionTime`, b.`UserName`" \
          " from user_question a left join user_info b on a.`UserID` = b.`id` WHERE QuestionContent " \
          "like %s or QuestionTitle like %s order by QuestionTime desc"
    # 匹配格式为 %key%  即包含key的
    arg = "%" + search_key + "%"
    args = (arg, arg)
    cursor.execute(sql, args)
    questions = cursor.fetchall()
    return questions


def fetch_user_by_id(user_id):
    """
    根据id取得对应的user
    :param user_id:
    :return:
    """
    sql = "select * from user_info where id=%s"
    args = (user_id)
    cursor.execute(sql, args)
    user = cursor.fetchall()
    #user = rows[0]
    return user


def answer_count(question_id):
    """
    获取该question的回答总数
    :param question_id:
    :return:
    """
    sql = "select count(*) as count from user_answer where QuestionID=%s"
    args = question_id
    cursor.execute(sql, args)
    count = cursor.fetchall()[0].get("count")
    return count

def update_user_mute(user_id,user_mute):
    user_new_mute = (int(user_mute)+1)%2
    sql = "update user_info set UserMute=%s where id=%s"
    args = (str(user_new_mute),user_id)
    cursor.execute(sql,args)
    conn.commit()

def delete_question_by_questionId(question_id):
    sql = "delete from user_question where id=%s"
    args = (question_id)
    cursor.execute(sql,args)
    conn.commit()

def delete_answers_by_questionID(question_id):
    sql = "delete from user_answer where QuestionID=%s"
    args = (question_id)
    cursor.execute(sql,args)
    conn.commit()



