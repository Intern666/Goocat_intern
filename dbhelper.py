# encoding: utf-8
import logging

import pymysql


# 数据库连接
def connect():
    """
    设置连接数据库的参数和连接数据库的因素
    :return:连接数据库的连接和游标
    """
    config = {
        'host': '101.37.23.58',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    cursor = conn.cursor()
    conn.select_db("goocat")
    return conn, cursor


def sql_required(func):
    """
    装饰器，在操作数据库之前对于连接和关闭数据库
    :param func: 函数形式
    :return:装饰器
    """
    def decorate(*args, **kwargs):
        try:
            conn, cursor = connect()
            result = func(*args, **kwargs, conn=conn, cursor=cursor)
        except Exception as e:
            result = None
            logging.error(str(e))
            print(str(e))
        finally:
            cursor.close()
            conn.close()
            return result

    return decorate


@sql_required
def insert_user(email, username, password, conn, cursor):
    """
    插入一个用户
    :param email:
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


@sql_required
def fetch_user_by_email(email, conn, cursor):
    """
    通过邮箱检查用户信息
    :param email: 需要查询的游湖邮箱
    :param conn: 数据库连接
    :param cursor: 数据课游标
    :return: 用户信息
    """
    sql = "select * from user_info where UserEmail = %s"
    args = email
    cursor.execute(sql, args)
    user = cursor.fetchall()
    return user


@sql_required
def fetch_all_questions(conn, cursor):
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


@sql_required
def fetch_questions_by_questionid(question_id, conn, cursor):
    """
    通过questionid取得对应问题，理论上id为主键，唯一
    :param question_id:
    :return:问题id对应的问题
    """
    # sql = "select * from question where id=%s limit 1" % question_id
    # sql = "select a.`id`, a.`title`, a.`content`, a.`create_time`, b.`username` from question a " \
    #       "left join user b on a.`author_id` = b.`id` where a.`id`=%s limit 1"
    sql = "select a.`id`, a.`QuestionTitle`, a.`QuestionContent`, a.`QuestionTime`, b.`UserName`,a.`UserID`" \
          " from user_question a left join user_info b on a.`UserID` = b.`id` where a.`id`=%s limit 1"
    args = question_id
    cursor.execute(sql, args)
    question = cursor.fetchone()
    return question


@sql_required
def fetch_answers_by_questionid(question_id, conn, cursor):
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


@sql_required
def insert_answer(content, question_id, author_id, conn, cursor):
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


@sql_required
def fetch_user_by_email_and_password(email, password, conn, cursor):
    """
    通过邮箱和密码查询user表返回对应user
    :param email:
    :param password:
    :return:
    """
    sql = "select * from user_info where UserEmail=%s and UserPassword=%s"
    args = (email, password)
    cursor.execute(sql, args)
    user = cursor.fetchone()
    return user


@sql_required
def insert_question(title, content, author_id, conn, cursor):
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
    question_id = conn.insert_id()
    conn.commit()
    return question_id


@sql_required
def search_by_key(search_key, conn, cursor):
    """
    根据key查找包含该key的问题
    :param search_key:
    :return:
    """
    # sql = "select * from user_question WHERE QuestionContent like %s or QuestionTitle like %s order by QuestionTime desc"
    sql = "select a.`id`, a.`QuestionTitle`, a.`QuestionContent`, a.`QuestionTime`, b.`UserName` " \
          " from user_question a left join user_info b on a.`UserID` = b.`id` WHERE QuestionContent " \
          "like %s or QuestionTitle like %s order by QuestionTime desc"
    # 匹配格式为 %key%  即包含key的
    arg = "%" + search_key + "%"
    args = (arg, arg)
    cursor.execute(sql, args)
    questions = cursor.fetchall()
    return questions


@sql_required
def fetch_user_by_id(user_id, conn, cursor):
    """
    根据id取得对应的user
    :param user_id:
    :return:
    """
    sql = "select * from user_info where id=%s"
    args = (user_id)
    cursor.execute(sql, args)
    user = cursor.fetchone()
    return user


@sql_required
def answer_count(question_id, conn, cursor):
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


@sql_required
def update_user_mute(user_id, user_mute, conn, cursor):
    """
    更新用户静音状态
    :param user_id: 用户id
    :param user_mute: 用户静音状态
    :param conn: 数据库连接
    :param cursor: 数据库游标
    :return: 无需返回数据值
    """
    user_new_mute = (int(user_mute) + 1) % 2
    sql = "update user_info set UserMute=%s where id=%s"
    args = (str(user_new_mute), user_id)
    cursor.execute(sql, args)
    conn.commit()


@sql_required
def delete_question_by_questionId(question_id, conn, cursor):
    """
    通过问题ID删除问题
    :param question_id: 需要删除问题的ID
    :param conn: 数据库连接
    :param cursor: 数据库游标
    :return: 无返回值
    """
    sql = "delete from user_question where id=%s"
    args = (question_id)
    cursor.execute(sql, args)
    conn.commit()


@sql_required
def delete_answers_by_questionID(question_id, conn, cursor):
    """
    通过问题ID 删除回答ID 删除问题使用
    :param question_id: 问题ID
    :param conn: 数据库连接
    :param cursor: 数据库游标
    :return: 无返回值
    """
    sql = "delete from user_answer where QuestionID=%s"
    args = (question_id)
    cursor.execute(sql, args)
    conn.commit()


@sql_required
def fetch_questions_by_userid(user_id, conn, cursor):
    """
    获取用户ID的题目
    :param user_id: 需要查询的用户ID
    :param conn: 数据库连接
    :param cursor: 数据库游标
    :return: 问题列表
    """
    sql = "select a.`id`, a.`QuestionTitle`, a.`QuestionTime`, a.`QuestionContent`, b.`UserName` " \
          " from user_question a left join user_info b on a.`UserID`=b.`id` where a.`UserID` = %s order by a.`QuestionTime` desc"
    args = user_id
    cursor.execute(sql, args)
    rows = cursor.fetchall()
    return rows


@sql_required
def fetch_answers_by_userid(user_id, conn, cursor):
    """
    听过回答者ID 获取用户答案
    :param user_id: 用户ID
    :param conn: 数据库连接
    :param cursor: 数据库游标
    :return: 答案列表
    """
    sql = "select a.`AnswerContent`, a.`QuestionID`, a.`UserID`, a.`AnswerTime`, b.`UserName` from user_answer a " \
          "left join user_info b on a.`UserID`=b.`id` where a.`UserID`=%s order by a.`AnswerTime` desc"
    args = user_id
    cursor.execute(sql, args)
    rows = cursor.fetchall()
    return rows


@sql_required
def update_user_by_userid(user_id, email, username, gender, school, conn, cursor):
    """
    更新用户信息
    :param user_id:修改后的用户ID
    :param email:修改后的邮箱
    :param username:修改后的用户名
    :param gender:修改后的性别
    :param school:修改后的学校
    :param conn:数据库连接
    :param cursor:数据库游标
    :return:无返回值
    """
    sql = "update user_info set `UserEmail` = %s, `UserName` = %s, `UserGender` = %s, `UserSchool` = %s" \
          "where `id` = %s"
    args = (email, username, gender, school, user_id)
    try:
        cursor.execute(sql, args)
        conn.commit()
    except Exception as e:
        logging.error(str(e))


def connectSocket(data1):
    """
    此方法是连接远程socket使用自动问答的结果
    :param data1:自动问答的问题
    :return:自动问答的结果
    """
    try:
        from socket import socket, AF_INET, SOCK_STREAM
        HOST = '127.0.0.1'  # or 'localhost'
        PORT = 50008
        BUFSIZ = 4098
        ADDR = (HOST, PORT)
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        # data = str(data)
        tcpCliSock.send(data1.encode())
        data1 = tcpCliSock.recv(BUFSIZ)
        data1 = data1.decode('utf-8')
        tcpCliSock.close()
    except Exception as e:
        return ""
    return data1
