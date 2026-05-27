# ============================================================
# 路由模块
# 这个文件定义了所有的Flask路由(URL地址和对应的处理函数)
#
# Flask的路由就像"门牌号":
#   用户访问 /           -> 返回主页HTML
#   用户访问 /api/draw   -> 返回随机抽取的牌面数据
#   用户访问 /api/reading -> 调用AI进行解读
#   ...等等
#
# 为什么要单独放一个文件?
#   1. 路由是"指挥中心"，负责协调各个模块的工作
#   2. 把路由集中管理，方便查看系统有哪些功能
#   3. app.py只需要注册这些路由，不需要关心具体实现
# ============================================================

from flask import render_template, request, jsonify

# 从各个模块导入需要的函数
from tarot_data import draw_cards
from db import (
    create_session, create_message, get_messages_by_session,
    get_all_sessions, get_session_by_id, delete_session
)
from ai_client import get_reading, get_follow_up_reply
from rag import rag_retrieve, update_user_memory
from utils import detect_question_type, format_cards_text, format_cards_for_followup


def register_routes(app):
    """
    注册所有路由到Flask应用

    这个函数是路由模块的"入口"，
    app.py只需要调用这个函数就能注册所有路由

    参数:
        app - Flask应用实例
    """

    # ==========================================================
    # 路由1: 首页
    # 当用户访问 http://localhost:5000/ 时，返回index.html
    # ==========================================================
    @app.route("/")
    def index():
        """返回主页面"""
        return render_template("index.html")

    # ==========================================================
    # 路由2: 抽牌API
    # 当用户选择牌阵后，前端会请求这个接口获取随机牌面
    # ==========================================================
    @app.route("/api/draw")
    def api_draw():
        """
        抽牌API

        请求方式: GET
        URL参数: spread - 牌阵类型 ('triple' 或 'single')

        返回: {"cards": [牌面数据列表]}
        """
        # 从URL参数中获取牌阵类型
        spread = request.args.get("spread", "triple")

        # 根据牌阵类型决定抽几张牌
        count = 3 if spread == "triple" else 1

        # 调用tarot_data中的draw_cards函数随机抽牌
        cards = draw_cards(count)

        # 返回JSON格式的数据
        return jsonify({"cards": cards})

    # ==========================================================
    # 路由3: 解读API(第一次提问)
    # 这是核心功能: 用户翻牌后提问，AI进行解读
    # ==========================================================
    @app.route("/api/reading", methods=["POST"])
    def api_reading():
        """
        解读API: 用户第一次提问时调用

        请求方式: POST
        请求体(JSON): {"cards": [...], "question": "...", "spread": "..."}

        返回(JSON): {
            "reading": "AI的解读文字",
            "session_id": 会话ID,
            "question_type": "问题类型"
        }

        处理流程:
            1. 接收牌面数据和问题
            2. 识别问题类型
            3. RAG检索相关历史
            4. 调用AI生成解读
            5. 保存到数据库(会话+消息)
            6. 更新用户记忆
            7. 返回结果
        """
        try:
            # 从前端发送的JSON中获取数据
            data = request.get_json()
            cards = data.get("cards", [])
            question = data.get("question", "综合运势")
            spread = data.get("spread", "triple")

            # 验证: 必须有牌面数据
            if not cards:
                return jsonify({"error": "请先抽取塔罗牌"}), 400

            # --- 步骤1: 识别问题类型 ---
            question_type = detect_question_type(question)

            # --- 步骤2: RAG检索 ---
            rag_context = rag_retrieve(None, question)

            # --- 步骤3: 格式化牌面信息 ---
            card_text = format_cards_text(cards)

            # --- 步骤4: 调用AI生成解读 ---
            reading = get_reading(card_text, question, question_type, rag_context)

            # --- 步骤5: 保存到数据库 ---
            # 创建会话
            session_id = create_session(
                spread_type=spread,
                cards_data=cards,
                summary=f"{question_type}: {question[:30]}..."
            )

            # 保存用户的问题
            create_message(session_id, "user", question, question_type)

            # 保存AI的解读
            create_message(session_id, "assistant", reading)

            # --- 步骤6: 更新用户长期记忆 ---
            update_user_memory(question, cards)

            # --- 步骤7: 返回结果 ---
            return jsonify({
                "reading": reading,
                "session_id": session_id,
                "question_type": question_type
            })

        except Exception as e:
            return jsonify({"error": f"解读失败: {str(e)}"}), 500

    # ==========================================================
    # 路由4: 追问API(连续提问)
    # 用户看到解读后，可以继续追问
    # ==========================================================
    @app.route("/api/follow-up", methods=["POST"])
    def api_follow_up():
        """
        追问API: 用户在看到解读后继续提问

        请求方式: POST
        请求体(JSON): {"session_id": 1, "question": "..."}

        返回(JSON): {"reply": "AI的回复"}

        处理流程:
            1. 获取当前会话的历史消息(短期记忆)
            2. RAG检索相关历史(长期记忆)
            3. 调用AI生成回复
            4. 保存消息到数据库
        """
        try:
            data = request.get_json()
            session_id = data.get("session_id")
            question = data.get("question", "").strip()

            # 验证参数
            if not session_id:
                return jsonify({"error": "缺少会话ID"}), 400
            if not question:
                return jsonify({"error": "请输入问题"}), 400

            # --- 步骤1: 获取会话信息 ---
            session_info = get_session_by_id(session_id)
            if not session_info:
                return jsonify({"error": "会话不存在"}), 404

            # --- 步骤2: 获取历史消息(短期记忆) ---
            history_messages = get_messages_by_session(session_id)

            # --- 步骤3: RAG检索(长期记忆) ---
            rag_context = rag_retrieve(session_id, question)

            # --- 步骤4: 格式化牌面信息 ---
            cards = session_info.get("cards_data", [])
            cards_text = format_cards_for_followup(cards)

            # --- 步骤5: 调用AI获取回复 ---
            reply = get_follow_up_reply(history_messages, cards_text, question, rag_context)

            # --- 步骤6: 保存消息到数据库 ---
            create_message(session_id, "user", question)
            create_message(session_id, "assistant", reply)

            return jsonify({"reply": reply})

        except Exception as e:
            return jsonify({"error": f"追问失败: {str(e)}"}), 500

    # ==========================================================
    # 路由5: 获取历史会话列表
    # ==========================================================
    @app.route("/api/sessions")
    def api_sessions():
        """
        获取所有历史会话列表

        返回(JSON): {"sessions": [会话列表]}
        """
        sessions = get_all_sessions()
        return jsonify({"sessions": sessions})

    # ==========================================================
    # 路由6: 获取单个会话详情
    # ==========================================================
    @app.route("/api/sessions/<int:session_id>")
    def api_session_detail(session_id):
        """
        获取指定会话的详情(包括所有消息)

        URL参数: session_id - 会话ID

        返回(JSON): {"session": {...}, "messages": [...]}
        """
        # 获取会话信息
        session = get_session_by_id(session_id)
        if not session:
            return jsonify({"error": "会话不存在"}), 404

        # 获取该会话的所有消息
        messages = get_messages_by_session(session_id)

        return jsonify({
            "session": session,
            "messages": messages
        })

    # ==========================================================
    # 路由7: 删除会话
    # ==========================================================
    @app.route("/api/sessions/<int:session_id>", methods=["DELETE"])
    def api_delete_session(session_id):
        """
        删除指定会话(及其所有消息)

        因为数据库设置了级联删除，删除会话时消息会自动删除
        """
        delete_session(session_id)
        return jsonify({"success": True})
