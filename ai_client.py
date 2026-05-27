# ============================================================
# AI客户端模块
# 这个文件封装了与Claude AI通信的所有逻辑:
#   - 初始化AI客户端
#   - 系统提示词(角色设定)
#   - 发送消息给AI并获取回复
#
# 为什么要单独放一个文件?
#   1. 把AI相关的配置和逻辑集中管理
#   2. 如果以后要换AI模型(比如换成OpenAI)，只需要改这个文件
#   3. 系统提示词可以方便地调整和优化
# ============================================================

import os
import anthropic


# ============================================================
# 初始化Claude AI客户端
# ============================================================

# 从环境变量读取API配置
api_key = os.getenv("ANTHROPIC_API_KEY")
base_url = os.getenv("ANTHROPIC_BASE_URL")

# 创建Anthropic客户端实例
# 这个客户端会在整个应用中被复用(不需要每次都创建新的)
client = anthropic.Anthropic(
    api_key=api_key,
    base_url=base_url
)


# ============================================================
# 系统提示词(System Prompt)
# 系统提示词是AI的"人格设定"，决定了它的回答风格和行为
# ============================================================

# 初次解读时的系统提示词
SYSTEM_PROMPT = """你是一位经验丰富的塔罗牌占卜师。你精通塔罗牌的象征意义，能够结合牌面和提问者的问题给出深刻的解读。

解读规则：
1. 先简要描述每张牌的核心含义（结合正位/逆位）
2. 分析牌与牌之间的关系和故事线
3. 结合提问者的具体问题给出综合解读
4. 给出温和而有建设性的建议
5. 保持神秘感和仪式感，但不要过度迷信
6. 使用中文回答，语言优美流畅
7. 控制在300-500字之间
8. 使用空行分隔不同的段落，让回答结构清晰

请以"亲爱的求问者"开头，以祝福语结尾。"""

# 追问时的系统提示词
FOLLOW_UP_PROMPT = """你是一位经验丰富的塔罗牌占卜师。用户已经进行了一次塔罗占卜，现在想追问更多细节。

规则：
1. 基于之前的牌面和解读，回答用户的追问
2. 保持与之前解读的一致性
3. 回答要简洁明了，控制在200-300字
4. 使用中文回答
5. 使用空行分隔段落

请直接回答用户的问题，不需要重复之前的解读内容。"""


# ============================================================
# AI调用函数
# ============================================================

def call_ai(system_prompt, user_message, max_tokens=1024):
    """
    调用Claude AI获取回复

    这是一个通用的AI调用函数，可以用于初次解读和追问

    参数:
        system_prompt - 系统提示词(AI的角色设定)
        user_message  - 用户的消息(包含问题和牌面信息)
        max_tokens    - 最大回复长度(字符数)

    返回值:
        AI的回复文字(字符串)
    """
    # client.messages.create() 发送请求给Claude AI
    response = client.messages.create(
        model="mimo-v2.5-pro",    # 使用的AI模型
        max_tokens=max_tokens,     # 最大回复长度
        system=system_prompt,      # 系统提示词(角色设定)
        messages=[                 # 对话消息列表
            {"role": "user", "content": user_message}
        ]
    )

    # response.content 是一个列表，第一个元素的text就是AI的回复文字
    return response.content[0].text


def get_reading(card_text, question, question_type, rag_context=""):
    """
    获取塔罗牌初次解读

    这个函数会:
    1. 构建包含牌面信息、问题类型和RAG参考的消息
    2. 调用AI获取解读

    参数:
        card_text     - 牌面信息的文字描述
        question      - 用户的问题
        question_type - 问题类型(如 '姻缘')
        rag_context   - RAG检索到的相关历史信息

    返回值:
        AI的解读文字
    """
    # 如果有RAG检索结果，添加到消息中
    rag_section = ""
    if rag_context:
        rag_section = f"\n\n【参考信息】\n{rag_context}\n(以上是历史参考，请结合当前牌面回答)"

    # 组合用户消息
    user_message = f"""我的问题是: {question}
问题类型: {question_type}

我抽到的牌:
{card_text}
{rag_section}

请为我进行塔罗牌解读。"""

    return call_ai(SYSTEM_PROMPT, user_message)


def get_follow_up_reply(history_messages, cards_text, question, rag_context=""):
    """
    获取追问的回复

    这个函数会:
    1. 获取当前会话的历史消息(短期记忆)
    2. 构建完整的对话上下文
    3. 调用AI获取回复

    参数:
        history_messages - 当前会话的历史消息列表
        cards_text       - 牌面信息的文字描述
        question         - 追问的问题
        rag_context      - RAG检索到的相关历史信息

    返回值:
        AI的回复文字
    """
    # 构建对话上下文
    messages = []

    # 添加历史消息(让AI知道之前的对话内容)
    for msg in history_messages:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # 构建追问消息
    rag_section = ""
    if rag_context:
        rag_section = f"\n\n【参考信息】\n{rag_context}"

    follow_up_message = f"""基于之前的牌面({cards_text})，用户想追问:
{question}
{rag_section}

请回答用户的追问。"""

    messages.append({"role": "user", "content": follow_up_message})

    # 构建系统上下文(包含牌面信息)
    system_context = FOLLOW_UP_PROMPT
    if history_messages:
        first_msg = history_messages[0]['content'] if history_messages else ''
        system_context += f"\n\n原始问题和牌面:\n{first_msg}"

    return call_ai(system_context, follow_up_message, max_tokens=512)
