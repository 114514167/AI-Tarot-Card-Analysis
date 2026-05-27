# ============================================================
# 塔罗牌大阿卡纳数据文件
# 这个文件存储了22张大阿卡纳塔罗牌的所有信息
# 以及一个随机抽牌的函数
# ============================================================

# 导入随机数模块，用来实现随机抽牌
import random

# ============================================================
# MAJOR_ARCANA 是一个列表，里面存放了22张大阿卡纳牌的数据
# 每张牌都是一个字典(dict)，包含以下字段:
#   id:         牌的编号 (0-21)
#   name_cn:    牌的中文名
#   name_en:    牌的英文名
#   upright:    正位信息 (keywords=关键词列表, meaning=含义说明)
#   reversed:   逆位信息 (同上结构)
#   image:      牌面图片的文件名
#   description: 对这张牌的简短描述
#
# 什么是"正位"和"逆位"?
#   - 正位(upright): 牌面朝上正常放置，代表正面含义
#   - 逆位(reversed): 牌面倒过来放置，代表相反或需要注意的含义
# ============================================================
MAJOR_ARCANA = [
    {
        "id": 0,
        "name_cn": "愚者",
        "name_en": "The Fool",
        "upright": {
            "keywords": ["新开始", "冒险", "天真", "自由"],
            "meaning": "代表新的开始，充满无限可能。保持开放的心态，勇敢踏出第一步。"
        },
        "reversed": {
            "keywords": ["鲁莽", "冒失", "犹豫不决"],
            "meaning": "提醒你三思而后行，避免冲动决定。注意可能存在的风险。"
        },
        "image": "00.svg",
        "description": "愚者是塔罗牌的起点，代表着纯真、冒险精神和无限潜力。"
    },
    {
        "id": 1,
        "name_cn": "魔术师",
        "name_en": "The Magician",
        "upright": {
            "keywords": ["创造力", "自信", "行动力", "技能"],
            "meaning": "你拥有实现目标所需的一切能力和资源。现在是采取行动的最佳时机。"
        },
        "reversed": {
            "keywords": ["欺骗", "操控", "才能浪费", "缺乏方向"],
            "meaning": "警惕周围的欺骗，也要反省自己是否在逃避真正的才能。"
        },
        "image": "01.svg",
        "description": "魔术师象征着将想法变为现实的力量，掌握四大元素的奥秘。"
    },
    {
        "id": 2,
        "name_cn": "女祭司",
        "name_en": "The High Priestess",
        "upright": {
            "keywords": ["直觉", "智慧", "神秘", "内在力量"],
            "meaning": "倾听内心的声音，你的直觉正在指引你走向正确的方向。"
        },
        "reversed": {
            "keywords": ["忽视直觉", "表面化", "秘密", "混乱"],
            "meaning": "你可能忽视了内心的声音，被表面现象所迷惑。静下心来重新感受。"
        },
        "image": "02.svg",
        "description": "女祭司是潜意识和直觉的守护者，掌握着隐藏的智慧。"
    },
    {
        "id": 3,
        "name_cn": "皇后",
        "name_en": "The Empress",
        "upright": {
            "keywords": ["丰盛", "母性", "自然", "创造力"],
            "meaning": "代表生命的丰盛与美好。在爱与关怀中，你将迎来收获和成长。"
        },
        "reversed": {
            "keywords": ["依赖", "缺乏安全感", "创造力受阻"],
            "meaning": "可能过度依赖他人，或忽视了自我照顾。需要重新找到内心的平衡。"
        },
        "image": "03.svg",
        "description": "皇后是大地之母的化身，象征着生育、丰饶和无条件的爱。"
    },
    {
        "id": 4,
        "name_cn": "皇帝",
        "name_en": "The Emperor",
        "upright": {
            "keywords": ["权威", "结构", "稳定", "领导力"],
            "meaning": "用理性和纪律来构建你的世界。坚定的领导力将带来秩序和成功。"
        },
        "reversed": {
            "keywords": ["专制", "固执", "控制欲", "缺乏弹性"],
            "meaning": "过度的控制欲可能适得其反。试着放松一些，接受不同的可能性。"
        },
        "image": "04.svg",
        "description": "皇帝代表着世俗的权力和秩序，是稳定与权威的象征。"
    },
    {
        "id": 5,
        "name_cn": "教皇",
        "name_en": "The Hierophant",
        "upright": {
            "keywords": ["传统", "信仰", "指导", "学习"],
            "meaning": "寻求传统智慧的指引，或找到一位导师来帮助你理解更深层的真理。"
        },
        "reversed": {
            "keywords": ["叛逆", "非传统", "打破常规", "个人信念"],
            "meaning": "是时候质疑传统观念，找到属于自己的信仰和道路。"
        },
        "image": "05.svg",
        "description": "教皇是精神世界的引导者，传递着神圣的知识和道德准则。"
    },
    {
        "id": 6,
        "name_cn": "恋人",
        "name_en": "The Lovers",
        "upright": {
            "keywords": ["爱情", "和谐", "选择", "价值观"],
            "meaning": "面临重要的选择，跟随你的心。爱与和谐将成为你的指引之光。"
        },
        "reversed": {
            "keywords": ["不和谐", "价值观冲突", "错误的选择", "犹豫"],
            "meaning": "内在的冲突导致了不和谐。需要重新审视自己的价值观和真正的需求。"
        },
        "image": "06.svg",
        "description": "恋人牌象征着爱、选择和二元性的统一，是心灵连接的象征。"
    },
    {
        "id": 7,
        "name_cn": "战车",
        "name_en": "The Chariot",
        "upright": {
            "keywords": ["胜利", "意志力", "决心", "前进"],
            "meaning": "凭借坚定的意志和决心，你将克服一切障碍，取得胜利。"
        },
        "reversed": {
            "keywords": ["失控", "方向迷失", "挫败", "缺乏自制"],
            "meaning": "内在的矛盾让你失去了方向。重新调整目标，找回前进的动力。"
        },
        "image": "07.svg",
        "description": "战车象征着通过意志力和决心取得胜利，驾驭对立的力量。"
    },
    {
        "id": 8,
        "name_cn": "力量",
        "name_en": "Strength",
        "upright": {
            "keywords": ["勇气", "内在力量", "耐心", "温柔的力量"],
            "meaning": "真正的力量来自内心。用温柔和耐心去面对挑战，你会发现自己比想象中更强大。"
        },
        "reversed": {
            "keywords": ["软弱", "自我怀疑", "缺乏勇气", "失控"],
            "meaning": "自我怀疑正在削弱你的力量。重新找回内心的勇气和自信。"
        },
        "image": "08.svg",
        "description": "力量牌展现的不是蛮力，而是以柔克刚的内在力量。"
    },
    {
        "id": 9,
        "name_cn": "隐士",
        "name_en": "The Hermit",
        "upright": {
            "keywords": ["内省", "独处", "智慧", "寻找真理"],
            "meaning": "暂时远离喧嚣，向内寻找答案。独处的时光将带来深刻的洞察。"
        },
        "reversed": {
            "keywords": ["孤立", "逃避", "固步自封", "拒绝帮助"],
            "meaning": "过度的孤立可能变成逃避。适当的独处是好的，但也要保持与外界的连接。"
        },
        "image": "09.svg",
        "description": "隐士是内在智慧的寻求者，在孤独中找到照亮前路的灯火。"
    },
    {
        "id": 10,
        "name_cn": "命运之轮",
        "name_en": "Wheel of Fortune",
        "upright": {
            "keywords": ["转变", "好运", "命运", "机遇"],
            "meaning": "命运的齿轮正在转动，好运即将到来。把握机遇，顺应变化的潮流。"
        },
        "reversed": {
            "keywords": ["坏运气", "抗拒改变", "失控", "逆境"],
            "meaning": "暂时的逆境是命运周期的一部分。保持耐心，低谷之后必有回升。"
        },
        "image": "10.svg",
        "description": "命运之轮象征着生命的循环和命运的不可预测性。"
    },
    {
        "id": 11,
        "name_cn": "正义",
        "name_en": "Justice",
        "upright": {
            "keywords": ["公正", "平衡", "真理", "因果"],
            "meaning": "宇宙的法则正在发挥作用。你的付出终将得到公正的回报。"
        },
        "reversed": {
            "keywords": ["不公正", "偏见", "逃避责任", "失衡"],
            "meaning": "面对不公正的局面，需要勇敢地站出来维护真理和平衡。"
        },
        "image": "11.svg",
        "description": "正义牌象征着宇宙的因果法则和万物的平衡。"
    },
    {
        "id": 12,
        "name_cn": "倒吊人",
        "name_en": "The Hanged Man",
        "upright": {
            "keywords": ["牺牲", "放手", "新视角", "等待"],
            "meaning": "暂时的停滞是为了更好的开始。换个角度看问题，你会有全新的领悟。"
        },
        "reversed": {
            "keywords": ["拖延", "抗拒", "无谓的牺牲", "停滞不前"],
            "meaning": "你可能在无意义地拖延。是时候做出决定，从停滞中解脱出来。"
        },
        "image": "12.svg",
        "description": "倒吊人通过自愿的牺牲获得更高层次的智慧和洞察。"
    },
    {
        "id": 13,
        "name_cn": "死神",
        "name_en": "Death",
        "upright": {
            "keywords": ["结束", "转变", "新生", "放下过去"],
            "meaning": "旧的篇章正在结束，新的开始即将到来。拥抱变化，这是重生的时刻。"
        },
        "reversed": {
            "keywords": ["抗拒改变", "恐惧", "停滞", "无法放手"],
            "meaning": "对改变的恐惧正在阻碍你的成长。学会放手，才能迎来新的可能。"
        },
        "image": "13.svg",
        "description": "死神并非字面意义上的死亡，而是象征着深刻的转变和更新。"
    },
    {
        "id": 14,
        "name_cn": "节制",
        "name_en": "Temperance",
        "upright": {
            "keywords": ["平衡", "耐心", "适度", "和谐"],
            "meaning": "在生活中寻找平衡与和谐。耐心和适度将引导你走向正确的道路。"
        },
        "reversed": {
            "keywords": ["失衡", "过度", "缺乏耐心", "冲突"],
            "meaning": "生活中的某些方面失去了平衡。重新调整，找到中庸之道。"
        },
        "image": "14.svg",
        "description": "节制牌象征着对立元素的融合与和谐统一。"
    },
    {
        "id": 15,
        "name_cn": "恶魔",
        "name_en": "The Devil",
        "upright": {
            "keywords": ["束缚", "诱惑", "物质主义", "阴暗面"],
            "meaning": "审视那些束缚你的事物。认清诱惑的本质，你就有力量挣脱枷锁。"
        },
        "reversed": {
            "keywords": ["解脱", "打破束缚", "觉醒", "重获自由"],
            "meaning": "你正在摆脱那些限制你的事物。继续保持觉醒，自由就在前方。"
        },
        "image": "15.svg",
        "description": "恶魔牌揭示了物质世界的诱惑和束缚，以及挣脱它们的可能性。"
    },
    {
        "id": 16,
        "name_cn": "塔",
        "name_en": "The Tower",
        "upright": {
            "keywords": ["突变", "破坏", "觉醒", "解放"],
            "meaning": "旧有的结构正在崩塌，虽然令人不安，但这是通往真理的必经之路。"
        },
        "reversed": {
            "keywords": ["逃避灾难", "恐惧改变", "延迟的变革"],
            "meaning": "你正在试图避免不可避免的改变。与其抗拒，不如主动拥抱转型。"
        },
        "image": "16.svg",
        "description": "塔象征着突然的变革和旧有信念的崩塌，是觉醒的催化剂。"
    },
    {
        "id": 17,
        "name_cn": "星星",
        "name_en": "The Star",
        "upright": {
            "keywords": ["希望", "灵感", "宁静", "信念"],
            "meaning": "在黑暗之后，星光为你指引方向。保持信念，美好的事物正在到来。"
        },
        "reversed": {
            "keywords": ["失去信心", "绝望", "与自我断连", "创意枯竭"],
            "meaning": "你可能暂时失去了希望。记住，星星永远在那里，即使被乌云遮蔽。"
        },
        "image": "17.svg",
        "description": "星星是希望和灵感的象征，在黑暗中闪耀着指引之光。"
    },
    {
        "id": 18,
        "name_cn": "月亮",
        "name_en": "The Moon",
        "upright": {
            "keywords": ["幻觉", "潜意识", "直觉", "不确定"],
            "meaning": "事情可能不像表面看起来那样。相信你的直觉，在迷雾中找到真相。"
        },
        "reversed": {
            "keywords": ["释放恐惧", "真相浮现", "走出迷雾"],
            "meaning": "迷雾正在散去，真相即将显现。你正在从困惑中走出来。"
        },
        "image": "18.svg",
        "description": "月亮照亮了潜意识的世界，揭示隐藏的真相和幻象。"
    },
    {
        "id": 19,
        "name_cn": "太阳",
        "name_en": "The Sun",
        "upright": {
            "keywords": ["快乐", "成功", "活力", "光明"],
            "meaning": "阳光普照，一切都在向好的方向发展。享受这段充满快乐和成功的时光。"
        },
        "reversed": {
            "keywords": ["暂时的挫折", "乐观过度", "延迟的成功"],
            "meaning": "虽然暂时有些阴霾，但阳光终将穿透云层。保持乐观但也要脚踏实地。"
        },
        "image": "19.svg",
        "description": "太阳是最积极的牌之一，象征着纯粹的快乐、成功和生命力。"
    },
    {
        "id": 20,
        "name_cn": "审判",
        "name_en": "Judgement",
        "upright": {
            "keywords": ["觉醒", "重生", "召唤", "反思"],
            "meaning": "听从内心的召唤，审视过去的经历。这是觉醒和重生的时刻。"
        },
        "reversed": {
            "keywords": ["自我怀疑", "逃避审视", "错过机会"],
            "meaning": "你可能在逃避对自己的审视。勇敢面对过去，才能迎接新的开始。"
        },
        "image": "20.svg",
        "description": "审判象征着灵魂的觉醒和对生命意义的深刻反思。"
    },
    {
        "id": 21,
        "name_cn": "世界",
        "name_en": "The World",
        "upright": {
            "keywords": ["完成", "成就", "圆满", "新旅程"],
            "meaning": "一个重要的周期即将圆满完成。庆祝你的成就，准备迎接新的旅程。"
        },
        "reversed": {
            "keywords": ["未完成", "缺少闭合", "延迟", "不完整"],
            "meaning": "还有未完成的事情需要处理。找到缺失的那块拼图，才能真正圆满。"
        },
        "image": "21.svg",
        "description": "世界牌象征着一个完整周期的结束和新旅程的开始。"
    }
]


# ============================================================
# draw_cards 函数: 随机抽取塔罗牌
# 参数:
#   count - 要抽取几张牌，默认是3张
# 返回值:
#   一个列表，每个元素是一张牌的信息字典
#   字典包含: id, name_cn, name_en, position(正/逆位), keywords, meaning, image, description
# ============================================================
def draw_cards(count=3):
    # random.sample() 从列表中随机选取不重复的元素
    # 比如从22张牌中随机选3张，不会选到重复的
    selected = random.sample(MAJOR_ARCANA, count)

    result = []
    for card in selected:
        # random.random() 生成0到1之间的随机小数
        # 如果小于0.5就是逆位，否则是正位 (各50%概率)
        is_reversed = random.random() < 0.5
        position = "reversed" if is_reversed else "upright"

        # 把这张牌的信息整理成一个字典，加到结果列表中
        result.append({
            "id": card["id"],                    # 牌的编号
            "name_cn": card["name_cn"],           # 中文名
            "name_en": card["name_en"],           # 英文名
            "position": position,                 # 正位或逆位
            "keywords": card[position]["keywords"],  # 根据正/逆位获取对应的关键词
            "meaning": card[position]["meaning"],    # 根据正/逆位获取对应的含义
            "image": f"/static/images/major_arcana/{card['image']}",  # 图片路径
            "description": card["description"]    # 牌的描述
        })

    return result
