# ============================================================
# 数据库初始化脚本
# 这个文件负责:
#   1. 创建数据库(如果不存在)
#   2. 创建所有需要的数据表
#   3. 定义数据库连接的工具函数
#
# 使用方法: 运行 python db_init.py 即可初始化数据库
# ============================================================

# --- 导入需要的模块 ---

# pymysql: Python连接MySQL的驱动
import pymysql

# os 和 load_dotenv: 用来读取.env文件中的数据库配置
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()


# ============================================================
# 数据库连接函数
# ============================================================

def get_db_connection():
    """
    创建并返回一个MySQL数据库连接

    这个函数会:
    1. 从.env文件读取数据库配置(主机、端口、用户名、密码、数据库名)
    2. 创建一个到MySQL的连接
    3. 设置字符集为utf8mb4(支持中文和emoji)

    返回值: pymysql的连接对象
    """
    # 从环境变量读取数据库配置
    # os.getenv("变量名", "默认值") - 如果环境变量不存在，使用默认值
    connection = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),       # 数据库主机地址
        port=int(os.getenv("MYSQL_PORT")),       # 端口号(需要转成整数)
        user=os.getenv("MYSQL_USER"),            # 用户名
        password=os.getenv("MYSQL_PASSWORD"),    # 密码
        database=os.getenv("MYSQL_DATABASE"), # 数据库名
        charset="utf8mb4",                                # 字符集(支持中文)
        cursorclass=pymysql.cursors.DictCursor            # 返回结果是字典格式(方便使用)
    )
    return connection


def get_db_connection_no_db():
    """
    创建一个不指定数据库的连接

    这个函数用于初始化阶段，当我们还没有创建数据库时使用
    连接到MySQL服务器本身，但不连接到特定的数据库
    """
    connection = pymysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


# ============================================================
# 初始化数据库
# ============================================================

def init_database():
    """
    初始化数据库: 创建数据库和所有数据表

    这个函数会依次执行:
    1. 创建数据库(如果不存在)
    2. 创建sessions表(存储会话信息)
    3. 创建messages表(存储对话消息)
    4. 创建user_memory表(存储用户记忆)
    """
    print("正在初始化数据库...")

    # --- 第1步: 创建数据库 ---
    # 先连接到MySQL服务器(不指定数据库)
    conn = get_db_connection_no_db()
    cursor = conn.cursor()

    # CREATE DATABASE IF NOT EXISTS: 如果数据库不存在就创建
    # CHARACTER SET utf8mb4: 使用支持中文的字符集
    db_name = os.getenv("MYSQL_DATABASE", "tarot_db")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.commit()
    print(f"数据库 '{db_name}' 已创建(或已存在)")

    # 关闭这个连接(因为我们接下来要连接到具体的数据库)
    cursor.close()
    conn.close()

    # --- 第2步: 连接到刚创建的数据库，创建数据表 ---
    conn = get_db_connection()
    cursor = conn.cursor()

    # ----------------------------------------------------------
    # sessions 表: 存储每次占卜会话的信息
    # ----------------------------------------------------------
    # 一个"会话"就是用户从开始占卜到结束的整个过程
    # 包括: 用户选择的牌阵、抽到的牌、提出的问题、AI的解读等
    #
    # 字段说明:
    #   id            - 会话的唯一标识(自动递增的整数)
    #   spread_type   - 牌阵类型: 'triple'(三牌阵) 或 'single'(单牌阵)
    #   cards_data    - 抽到的牌的数据(JSON格式存储)
    #   created_at    - 会话创建时间(自动记录)
    #   updated_at    - 会话最后更新时间(每次修改自动更新)
    #   summary       - 会话摘要(用一句话概括这次占卜)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '会话ID(自动递增)',
            spread_type VARCHAR(20) NOT NULL COMMENT '牌阵类型: triple或single',
            cards_data JSON COMMENT '抽到的牌的数据(JSON格式)',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            summary VARCHAR(500) DEFAULT '' COMMENT '会话摘要'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='占卜会话表'
    """)
    print("sessions 表已创建")

    # ----------------------------------------------------------
    # messages 表: 存储每条对话消息
    # ----------------------------------------------------------
    # 一个会话中可以有多条消息(用户提问、AI回答、用户追问等)
    #
    # 字段说明:
    #   id            - 消息的唯一标识
    #   session_id    - 这条消息属于哪个会话(外键，关联sessions表)
    #   role          - 消息角色: 'user'(用户) 或 'assistant'(AI)
    #   content       - 消息内容
    #   question_type - 问题类型: '姻缘'、'学业'、'事业'等
    #   created_at    - 消息创建时间
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID(自动递增)',
            session_id INT NOT NULL COMMENT '所属会话ID',
            role VARCHAR(20) NOT NULL COMMENT '消息角色: user或assistant',
            content TEXT NOT NULL COMMENT '消息内容',
            question_type VARCHAR(50) DEFAULT '' COMMENT '问题类型',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            INDEX idx_session_id (session_id),
            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='对话消息表'
    """)
    print("messages 表已创建")

    # ----------------------------------------------------------
    # user_memory 表: 存储用户记忆(长期记忆)
    # ----------------------------------------------------------
    # 用来记住用户的偏好和历史信息，提供个性化的解读
    #
    # 字段说明:
    #   id            - 记忆的唯一标识
    #   memory_key    - 记忆的类型(如 'favorite_question', 'card_frequency')
    #   memory_value  - 记忆的内容
    #   created_at    - 创建时间
    #   updated_at    - 更新时间
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记忆ID(自动递增)',
            memory_key VARCHAR(100) NOT NULL COMMENT '记忆类型(如: 常问问题, 偏好牌阵)',
            memory_value TEXT COMMENT '记忆内容',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            UNIQUE KEY uk_memory_key (memory_key)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户记忆表(长期记忆)'
    """)
    print("user_memory 表已创建")

    # 提交所有SQL语句的更改
    conn.commit()

    # 关闭游标和连接
    cursor.close()
    conn.close()

    print("数据库初始化完成!")


# ============================================================
# 当直接运行这个文件时，执行初始化
# ============================================================
if __name__ == "__main__":
    init_database()
