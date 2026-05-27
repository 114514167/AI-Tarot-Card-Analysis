# ============================================================
# RAG检索增强模块
# RAG = Retrieval Augmented Generation (检索增强生成)
#
# 核心思想:
#   在AI回答之前，先从历史数据中检索相关信息，
#   把这些信息作为"参考"提供给AI，让回答更准确、更有针对性。
#
# 举个例子:
#   用户问 "我考研能成功吗？"
#   RAG会从历史中发现:
#   1. 用户之前问过类似的学业问题
#   2. 用户之前抽到过"星星"牌(代表希望)
#   3. 用户的记忆中记录了"常问学业问题"
#   然后把这些信息告诉AI，AI的回答就会更有针对性。
#
# 当前使用的是简单的文本匹配策略，
# 未来可以升级为向量数据库(如ChromaDB)实现语义检索。
# ============================================================

from db import get_recent_user_questions, get_all_memories, get_messages_by_session


def rag_retrieve(session_id, question):
    """
    RAG检索主函数: 从历史数据中检索与当前问题相关的信息

    检索策略(3种来源):
        1. 历史问题 - 用户之前问过什么问题
        2. 用户记忆 - 长期记忆中存储的偏好信息
        3. 会话牌面 - 当前会话的牌面信息(追问时使用)

    参数:
        session_id - 当前会话ID(追问时传入，初次提问传None)
        question   - 用户的问题

    返回值:
        一个字符串，包含检索到的所有相关信息
        如果没有检索到任何信息，返回空字符串
    """
    context_parts = []  # 存储检索到的上下文信息

    # --- 检索1: 查找用户历史中类似的问题 ---
    # 从数据库中获取用户最近的5个问题
    history_questions = get_recent_user_questions(
        limit=5,
        exclude_question=question
    )

    if history_questions:
        context_parts.append("【历史问题参考】")
        for q in history_questions:
            context_parts.append(f"- {q['content']}")

    # --- 检索2: 查找用户的长期记忆 ---
    # 从user_memory表中查找用户偏好
    memories = get_all_memories()

    if memories:
        context_parts.append("\n【用户记忆】")
        for mem in memories:
            context_parts.append(f"- {mem['memory_key']}: {mem['memory_value']}")

    # --- 检索3: 如果是追问，获取当前会话的消息历史 ---
    # 追问时，需要知道之前已经讨论了什么
    if session_id:
        session_messages = get_messages_by_session(session_id)
        if session_messages:
            context_parts.append("\n【当前会话历史】")
            for msg in session_messages[:4]:  # 只取前4条，避免上下文太长
                role_cn = "用户" if msg["role"] == "user" else "塔罗师"
                # 截取前50个字符，避免太长
                content_preview = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
                context_parts.append(f"- [{role_cn}]: {content_preview}")

    # 把所有检索到的信息拼接成一个字符串
    return "\n".join(context_parts) if context_parts else ""


def update_user_memory(question, cards):
    """
    更新用户的长期记忆

    当用户提问后，我们分析问题和牌面信息，
    把有价值的信息存入user_memory表，供以后的RAG检索使用

    参数:
        question - 用户的问题
        cards    - 抽到的牌
    """
    from db import upsert_memory

    # 记录用户最近的问题
    upsert_memory("last_question", question)

    # 记录最近出现的牌(用于分析用户与哪些牌有"缘分")
    card_names = [card["name_cn"] for card in cards]
    upsert_memory("recent_cards", ", ".join(card_names))
