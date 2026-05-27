# ============================================================
# 数据库工具模块
# 这个文件封装了所有与MySQL数据库相关的操作:
#   - 数据库连接
#   - 会话(session)的增删改查
#   - 消息(message)的增删改查
#   - 用户记忆(memory)的读写
#
# 为什么要单独放一个文件?
#   1. 让数据库操作集中管理，方便维护
#   2. 其他模块只需要调用这里的函数，不需要关心SQL细节
#   3. 如果以后要换数据库(比如换成SQLite)，只需要改这个文件
# ============================================================

import os
import json
from datetime import datetime
import pymysql

# ============================================================
# 数据库连接
# ============================================================


def get_db_connection():
    """
    创建并返回一个MySQL数据库连接

    从环境变量中读取数据库配置(主机、端口、用户名、密码、数据库名)
    返回的连接对象可以用来执行SQL语句

    返回值: pymysql连接对象
    """
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),  # 数据库主机地址
        port=int(os.getenv("MYSQL_PORT")),  # 端口号
        user=os.getenv("MYSQL_USER"),  # 用户名
        password=os.getenv("MYSQL_PASSWORD"),  # 密码
        database=os.getenv("MYSQL_DATABASE"),  # 数据库名
        charset="utf8mb4",  # 字符集(支持中文和emoji)
        cursorclass=pymysql.cursors.DictCursor,  # 返回字典格式结果
    )


def format_datetime(dt):
    """
    将datetime对象格式化为易读的字符串

    参数:
        dt - datetime对象，或者已经是字符串的时间

    返回值:
        格式化后的字符串，如 "2026-05-27 14:30"
    """
    if dt is None:
        return ""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M")
    return str(dt)


def format_time(dt):
    """
    将datetime对象格式化为简短的时间字符串

    参数:
        dt - datetime对象

    返回值:
        时间字符串，如 "14:30"
    """
    if dt is None:
        return ""
    if isinstance(dt, datetime):
        return dt.strftime("%H:%M")
    return str(dt)


# ============================================================
# 会话(Session)相关操作
# "会话"就是用户从开始占卜到结束的整个过程
# ============================================================


def create_session(spread_type, cards_data, summary):
    """
    创建一个新的占卜会话

    参数:
        spread_type - 牌阵类型 ('triple' 或 'single')
        cards_data  - 抽到的牌的数据(列表)
        summary     - 会话摘要(一句话概括)

    返回值:
        新创建的会话ID(整数)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # INSERT INTO: 向表中插入一条新记录
        # json.dumps(): 把Python对象转换成JSON字符串
        # ensure_ascii=False: 确保中文不会被转义成\uXXXX
        cursor.execute(
            """
            INSERT INTO sessions (spread_type, cards_data, summary)
            VALUES (%s, %s, %s)
        """,
            (spread_type, json.dumps(cards_data, ensure_ascii=False), summary),
        )

        conn.commit()  # 提交更改
        return cursor.lastrowid  # 返回新记录的ID

    finally:
        cursor.close()
        conn.close()


def get_all_sessions():
    """
    获取所有历史会话列表

    返回值:
        会话列表，每个会话是一个字典
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 不在SQL中格式化日期，直接获取原始的datetime
        # 这样可以避免PyMySQL的%转义问题
        cursor.execute("""
            SELECT id, summary, spread_type, created_at
            FROM sessions
            ORDER BY created_at DESC
        """)
        sessions = cursor.fetchall()

        # 在Python中格式化日期
        for s in sessions:
            s["created_at"] = format_datetime(s["created_at"])

        return sessions

    finally:
        cursor.close()
        conn.close()


def get_session_by_id(session_id):
    """
    根据ID获取单个会话的详细信息

    参数:
        session_id - 会话ID

    返回值:
        会话字典，如果不存在返回None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 直接获取原始数据，不在SQL中格式化日期
        cursor.execute(
            """
            SELECT id, spread_type, cards_data, summary, created_at
            FROM sessions
            WHERE id = %s
        """,
            (session_id,),
        )

        session = cursor.fetchone()

        if session:
            # 格式化日期
            session["created_at"] = format_datetime(session["created_at"])
            # 把cards_data从JSON字符串转回Python对象
            if session["cards_data"]:
                if isinstance(session["cards_data"], str):
                    session["cards_data"] = json.loads(session["cards_data"])

        return session

    finally:
        cursor.close()
        conn.close()


def delete_session(session_id):
    """
    删除指定会话

    因为messages表设置了ON DELETE CASCADE(级联删除)，
    删除session时，相关的messages会自动被删除

    参数:
        session_id - 要删除的会话ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
        conn.commit()

    finally:
        cursor.close()
        conn.close()


# ============================================================
# 消息(Message)相关操作
# 每次用户提问和AI回答都是一条消息
# ============================================================


def create_message(session_id, role, content, question_type=""):
    """
    创建一条新消息

    参数:
        session_id    - 所属会话的ID
        role          - 消息角色: 'user'(用户) 或 'assistant'(AI)
        content       - 消息内容
        question_type - 问题类型(如 '姻缘'、'学业')

    返回值:
        新创建的消息ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO messages (session_id, role, content, question_type)
            VALUES (%s, %s, %s, %s)
        """,
            (session_id, role, content, question_type),
        )

        conn.commit()
        return cursor.lastrowid

    finally:
        cursor.close()
        conn.close()


def get_messages_by_session(session_id):
    """
    获取指定会话的所有消息

    参数:
        session_id - 会话ID

    返回值:
        消息列表，按时间正序排列(先提问后回答)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 直接获取原始数据
        cursor.execute(
            """
            SELECT role, content, question_type, created_at
            FROM messages
            WHERE session_id = %s
            ORDER BY created_at ASC
        """,
            (session_id,),
        )

        messages = cursor.fetchall()

        # 在Python中格式化时间
        for msg in messages:
            msg["time"] = format_time(msg.pop("created_at"))

        return messages

    finally:
        cursor.close()
        conn.close()


def get_recent_user_questions(limit=5, exclude_question=""):
    """
    获取用户最近的提问历史(用于RAG检索)

    参数:
        limit            - 最多返回几条记录
        exclude_question - 排除某个问题(避免和当前问题重复)

    返回值:
        问题列表
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT content, question_type
            FROM messages
            WHERE role = 'user'
            AND content != %s
            ORDER BY created_at DESC
            LIMIT %s
        """,
            (exclude_question, limit),
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


# ============================================================
# 用户记忆(Memory)相关操作
# 用于存储长期记忆(用户偏好、历史信息等)
# ============================================================


def get_all_memories():
    """
    获取所有用户记忆

    返回值:
        记忆列表，每个记忆是一个字典
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT memory_key, memory_value
            FROM user_memory
            ORDER BY updated_at DESC
        """)
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def upsert_memory(memory_key, memory_value):
    """
    插入或更新一条用户记忆

    "Upsert" = Update or Insert
    如果这个key已经存在，就更新它的值；
    如果不存在，就插入一条新记录。

    参数:
        memory_key   - 记忆的类型(如 'last_question', 'recent_cards')
        memory_value - 记忆的内容
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # ON DUPLICATE KEY UPDATE: 如果主键/唯一键冲突，就执行更新操作
        cursor.execute(
            """
            INSERT INTO user_memory (memory_key, memory_value)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE memory_value = %s, updated_at = CURRENT_TIMESTAMP
        """,
            (memory_key, memory_value, memory_value),
        )

        conn.commit()

    finally:
        cursor.close()
        conn.close()
