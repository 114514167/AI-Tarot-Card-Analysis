# ============================================================
# Flask 后端主程序 (入口文件)
#
# 这个文件是整个应用的"入口点"，它的职责很简单:
#   1. 创建Flask应用实例
#   2. 注册路由(从routes.py导入)
#   3. 启动服务器
#
# 具体的业务逻辑被拆分到了以下模块中:
#   - db.py        - 数据库操作(连接、增删改查)
#   - ai_client.py - AI客户端(调用Claude API)
#   - rag.py       - RAG检索增强(从历史中检索相关信息)
#   - utils.py     - 工具函数(问题类型识别、牌面格式化)
#   - routes.py    - 路由定义(URL地址和处理函数)
#   - tarot_data.py - 塔罗牌数据(22张大阿卡纳)
#
# 这样拆分的好处:
#   1. 每个文件职责单一，代码更清晰
#   2. 方便修改和维护(改数据库只动db.py，改AI只动ai_client.py)
#   3. 方便测试(可以单独测试每个模块)
# ============================================================

# --- 导入需要的模块 ---
from flask import Flask
from dotenv import load_dotenv

# 从routes模块导入路由注册函数
from routes import register_routes

# --- 加载环境变量 ---
# 读取.env文件中的配置(API密钥、数据库密码等)
load_dotenv()

# --- 创建Flask应用实例 ---
# __name__ 告诉Flask当前文件的位置，这样它就能找到模板和静态文件
app = Flask(__name__)

# --- 注册所有路由 ---
# 这行代码会把routes.py中定义的所有URL地址注册到Flask应用中
register_routes(app)


# ============================================================
# 启动Flask服务器
# ============================================================
if __name__ == "__main__":
    # 启动前检查数据库连接是否正常
    try:
        from db import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM sessions LIMIT 1")  # 简单查询测试连接
        cursor.close()
        conn.close()
        print("数据库连接成功!")
    except Exception as e:
        print(f"数据库连接失败: {e}")
        print("请先运行 python db_init.py 初始化数据库")
        print("或者检查.env中的数据库配置是否正确")

    # app.run() 启动Flask开发服务器
    # debug=True: 开启调试模式(代码修改后自动重启，出错时显示详细信息)
    # port=5000: 监听5000端口(访问地址: http://localhost:5000)
    app.run(debug=True, port=5000)
