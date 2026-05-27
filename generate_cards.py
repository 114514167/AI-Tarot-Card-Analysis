"""生成22张大阿卡纳塔罗牌SVG图片"""

import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "static", "images", "major_arcana")
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 200, 320  # 卡片尺寸


def svg_wrap(inner, bg_colors):
    """SVG包装器，统一卡片外框"""
    c1, c2, c3 = bg_colors
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="50%" stop-color="{c2}"/>
      <stop offset="100%" stop-color="{c3}"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#d4af37"/>
      <stop offset="50%" stop-color="#f5d77a"/>
      <stop offset="100%" stop-color="#d4af37"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <!-- 背景 -->
  <rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>
  <!-- 外边框 -->
  <rect x="4" y="4" width="{W-8}" height="{H-8}" rx="10" fill="none" stroke="url(#gold)" stroke-width="2"/>
  <!-- 内边框 -->
  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="7" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity="0.5"/>
  <!-- 角落装饰 -->
  <path d="M18,18 L32,18 M18,18 L18,32" stroke="#d4af37" stroke-width="1.5" opacity="0.6"/>
  <path d="M{W-18},18 L{W-32},18 M{W-18},18 L{W-18},32" stroke="#d4af37" stroke-width="1.5" opacity="0.6"/>
  <path d="M18,{H-18} L32,{H-18} M18,{H-18} L18,{H-32}" stroke="#d4af37" stroke-width="1.5" opacity="0.6"/>
  <path d="M{W-18},{H-18} L{W-32},{H-18} M{W-18},{H-18} L{W-18},{H-32}" stroke="#d4af37" stroke-width="1.5" opacity="0.6"/>
  {inner}
</svg>"""


def card_label(num, name_cn, name_en):
    """卡片底部标签"""
    return f"""
  <!-- 底部标签 -->
  <rect x="0" y="{H-60}" width="{W}" height="60" rx="0" fill="rgba(0,0,0,0.5)"/>
  <rect x="10" y="{H-58}" width="{W-20}" height="56" rx="5" fill="rgba(0,0,0,0.3)"/>
  <text x="{W/2}" y="{H-38}" text-anchor="middle" fill="#d4af37" font-size="11" font-family="serif" font-weight="bold">No.{num:02d} · 大阿卡纳</text>
  <text x="{W/2}" y="{H-20}" text-anchor="middle" fill="#f5d77a" font-size="14" font-family="serif" font-weight="bold">{name_cn} · {name_en}</text>"""


def card_title_top(name_cn):
    """卡片顶部标题"""
    return f"""
  <text x="{W/2}" y="32" text-anchor="middle" fill="#d4af37" font-size="13" font-family="serif" font-weight="bold" filter="url(#glow)">{name_cn}</text>"""


# ============================================================
# 0 愚者 The Fool
# ============================================================
def card_0():
    inner = f"""
  {card_title_top("愚者")}
  <!-- 太阳 -->
  <circle cx="{W/2}" cy="80" r="18" fill="#FFD700" opacity="0.9" filter="url(#softglow)"/>
  <circle cx="{W/2}" cy="80" r="12" fill="#FFF8DC"/>
  <!-- 山脉 -->
  <polygon points="30,200 70,130 110,200" fill="#5a8a5a" opacity="0.7"/>
  <polygon points="80,200 130,110 180,200" fill="#4a7a4a" opacity="0.8"/>
  <!-- 小路 -->
  <path d="M{W/2},200 Q{W/2},170 130,140" stroke="#c4a45a" stroke-width="2" fill="none" opacity="0.6"/>
  <!-- 花朵 -->
  <circle cx="55" cy="195" r="4" fill="#FF69B4" opacity="0.8"/>
  <circle cx="145" cy="190" r="3" fill="#FFB6C1" opacity="0.7"/>
  <circle cx="80" cy="198" r="3.5" fill="#FF1493" opacity="0.6"/>
  <!-- 蝴蝶 -->
  <path d="M100,100 Q95,90 100,85 Q105,90 100,100" fill="#FF69B4" opacity="0.8"/>
  <path d="M100,100 Q105,90 110,85 Q105,90 100,100" fill="#FFB6C1" opacity="0.8"/>
  <!-- 星星 -->
  <text x="40" y="70" fill="#FFD700" font-size="10" opacity="0.7">✦</text>
  <text x="160" y="60" fill="#FFD700" font-size="8" opacity="0.5">✦</text>
  <text x="150" y="100" fill="#FFD700" font-size="6" opacity="0.4">✦</text>
  {card_label(0, "愚者", "The Fool")}"""
    return svg_wrap(inner, ("#87CEEB", "#B0E0E6", "#90EE90"))


# ============================================================
# 1 魔术师 The Magician
# ============================================================
def card_1():
    inner = f"""
  {card_title_top("魔术师")}
  <!-- 魔法阵 -->
  <circle cx="{W/2}" cy="110" r="40" fill="none" stroke="#FFD700" stroke-width="1.5" opacity="0.6"/>
  <circle cx="{W/2}" cy="110" r="30" fill="none" stroke="#FF6347" stroke-width="1" opacity="0.5"/>
  <!-- 无限符号 -->
  <path d="M75,80 Q85,65 100,80 Q115,95 125,80" stroke="#FFD700" stroke-width="2.5" fill="none" filter="url(#glow)"/>
  <path d="M75,80 Q85,95 100,80 Q115,65 125,80" stroke="#FFD700" stroke-width="2.5" fill="none"/>
  <!-- 权杖 -->
  <line x1="{W/2}" y1="70" x2="{W/2}" y2="155" stroke="#d4af37" stroke-width="3"/>
  <circle cx="{W/2}" cy="68" r="5" fill="#FFD700" filter="url(#glow)"/>
  <!-- 四元素 -->
  <text x="55" y="150" fill="#FF4500" font-size="14" opacity="0.8">🔥</text>
  <text x="135" y="150" fill="#4169E1" font-size="14" opacity="0.8">💧</text>
  <text x="55" y="175" fill="#32CD32" font-size="14" opacity="0.8">🌿</text>
  <text x="135" y="175" fill="#87CEEB" font-size="14" opacity="0.8">💨</text>
  <!-- 桌子 -->
  <rect x="60" y="155" width="80" height="8" rx="2" fill="#8B4513" opacity="0.8"/>
  {card_label(1, "魔术师", "The Magician")}"""
    return svg_wrap(inner, ("#8B0000", "#DC143C", "#FF6347"))


# ============================================================
# 2 女祭司 The High Priestess
# ============================================================
def card_2():
    inner = f"""
  {card_title_top("女祭司")}
  <!-- 月亮 -->
  <circle cx="{W/2}" cy="85" r="25" fill="none" stroke="#C0C0C0" stroke-width="1.5" opacity="0.7"/>
  <circle cx="{W/2+8}" cy="80" r="22" fill="#191970" opacity="0.8"/>
  <!-- 柱子 -->
  <rect x="40" y="100" width="12" height="100" fill="#4169E1" opacity="0.5" rx="2"/>
  <rect x="148" y="100" width="12" height="100" fill="#4169E1" opacity="0.5" rx="2"/>
  <text x="46" y="115" fill="#C0C0C0" font-size="9" font-family="serif">B</text>
  <text x="154" y="115" fill="#C0C0C0" font-size="9" font-family="serif">J</text>
  <!-- 帘幕 -->
  <path d="M52,100 Q{W/2},130 148,100" stroke="#6A5ACD" stroke-width="1" fill="none" opacity="0.6"/>
  <!-- 水 -->
  <path d="M60,180 Q80,170 100,180 Q120,190 140,180" stroke="#00CED1" stroke-width="1.5" fill="none" opacity="0.6"/>
  <path d="M55,190 Q80,180 100,190 Q120,200 145,190" stroke="#00CED1" stroke-width="1" fill="none" opacity="0.4"/>
  <!-- 卷轴 -->
  <rect x="82" y="130" width="36" height="25" rx="3" fill="#E6E6FA" opacity="0.7"/>
  <text x="{W/2}" y="147" text-anchor="middle" fill="#191970" font-size="8" font-family="serif">TORA</text>
  <!-- 星星 -->
  <text x="100" y="65" fill="#C0C0C0" font-size="8" opacity="0.6">✦</text>
  {card_label(2, "女祭司", "The High Priestess")}"""
    return svg_wrap(inner, ("#191970", "#4169E1", "#87CEEB"))


# ============================================================
# 3 皇后 The Empress
# ============================================================
def card_3():
    inner = f"""
  {card_title_top("皇后")}
  <!-- 麦穗 -->
  <path d="M50,170 Q55,130 60,100" stroke="#DAA520" stroke-width="2" fill="none"/>
  <circle cx="58" cy="98" r="4" fill="#DAA520"/>
  <path d="M140,170 Q145,130 150,100" stroke="#DAA520" stroke-width="2" fill="none"/>
  <circle cx="148" cy="98" r="4" fill="#DAA520"/>
  <!-- 心形 -->
  <path d="M{W/2},90 Q{W/2-15},70 {W/2},85 Q{W/2+15},70 {W/2},90" fill="#FF69B4" opacity="0.8" filter="url(#glow)"/>
  <!-- 花朵装饰 -->
  <circle cx="70" cy="140" r="6" fill="#FF69B4" opacity="0.7"/>
  <circle cx="85" cy="135" r="5" fill="#FFB6C1" opacity="0.6"/>
  <circle cx="115" cy="135" r="5" fill="#FFB6C1" opacity="0.6"/>
  <circle cx="130" cy="140" r="6" fill="#FF69B4" opacity="0.7"/>
  <!-- 王座 -->
  <rect x="70" y="105" width="60" height="70" rx="8" fill="#228B22" opacity="0.4"/>
  <rect x="75" y="110" width="50" height="60" rx="5" fill="#32CD32" opacity="0.3"/>
  <!-- 草地 -->
  <ellipse cx="{W/2}" cy="200" rx="60" ry="10" fill="#32CD32" opacity="0.4"/>
  <!-- 小花 -->
  <text x="60" y="195" fill="#FF1493" font-size="8" opacity="0.7">❀</text>
  <text x="130" y="192" fill="#FF69B4" font-size="7" opacity="0.6">❀</text>
  <text x="95" y="198" fill="#FFB6C1" font-size="6" opacity="0.5">❀</text>
  {card_label(3, "皇后", "The Empress")}"""
    return svg_wrap(inner, ("#228B22", "#32CD32", "#98FB98"))


# ============================================================
# 4 皇帝 The Emperor
# ============================================================
def card_4():
    inner = f"""
  {card_title_top("皇帝")}
  <!-- 王座 -->
  <rect x="65" y="90" width="70" height="90" rx="5" fill="#8B0000" opacity="0.6"/>
  <rect x="60" y="85" width="80" height="15" rx="3" fill="#B22222" opacity="0.7"/>
  <!-- 权杖 -->
  <line x1="75" y1="95" x2="75" y2="170" stroke="#d4af37" stroke-width="3"/>
  <circle cx="75" cy="93" r="4" fill="#FFD700"/>
  <!-- 球体 -->
  <circle cx="125" cy="130" r="10" fill="none" stroke="#d4af37" stroke-width="2"/>
  <line x1="115" y1="130" x2="135" y2="130" stroke="#d4af37" stroke-width="1"/>
  <line x1="125" y1="120" x2="125" y2="140" stroke="#d4af37" stroke-width="1"/>
  <!-- 盾牌 -->
  <path d="M{W/2},100 L{W/2-15},115 L{W/2},150 L{W/2+15},115 Z" fill="none" stroke="#d4af37" stroke-width="1.5"/>
  <!-- 公羊角 -->
  <path d="M70,80 Q65,70 75,65" stroke="#d4af37" stroke-width="2" fill="none"/>
  <path d="M130,80 Q135,70 125,65" stroke="#d4af37" stroke-width="2" fill="none"/>
  <!-- 山峰 -->
  <polygon points="40,200 70,150 100,200" fill="#B22222" opacity="0.3"/>
  <polygon points="100,200 130,140 160,200" fill="#8B0000" opacity="0.3"/>
  {card_label(4, "皇帝", "The Emperor")}"""
    return svg_wrap(inner, ("#2F0000", "#8B0000", "#B22222"))


# ============================================================
# 5 教皇 The Hierophant
# ============================================================
def card_5():
    inner = f"""
  {card_title_top("教皇")}
  <!-- 三重冠 -->
  <path d="M{W/2},60 L{W/2-20},90 L{W/2+20},90 Z" fill="#9370DB" stroke="#d4af37" stroke-width="1"/>
  <circle cx="{W/2}" cy="65" r="4" fill="#FFD700"/>
  <circle cx="{W/2-10}" cy="75" r="3" fill="#FFD700"/>
  <circle cx="{W/2+10}" cy="75" r="3" fill="#FFD700"/>
  <!-- 钥匙 -->
  <line x1="70" y1="120" x2="70" y2="180" stroke="#d4af37" stroke-width="2"/>
  <circle cx="70" cy="118" r="6" fill="none" stroke="#d4af37" stroke-width="2"/>
  <line x1="70" y1="170" x2="76" y2="170" stroke="#d4af37" stroke-width="2"/>
  <line x1="70" y1="175" x2="76" y2="175" stroke="#d4af37" stroke-width="2"/>
  <!-- 十字架 -->
  <line x1="130" y1="110" x2="130" y2="180" stroke="#C0C0C0" stroke-width="2"/>
  <line x1="120" y1="130" x2="140" y2="130" stroke="#C0C0C0" stroke-width="2"/>
  <!-- 柱子 -->
  <rect x="55" y="95" width="8" height="100" fill="#6A0DAD" opacity="0.4" rx="2"/>
  <rect x="137" y="95" width="8" height="100" fill="#6A0DAD" opacity="0.4" rx="2"/>
  <!-- 信徒 -->
  <circle cx="80" cy="175" r="5" fill="#DDA0DD" opacity="0.5"/>
  <circle cx="120" cy="175" r="5" fill="#DDA0DD" opacity="0.5"/>
  {card_label(5, "教皇", "The Hierophant")}"""
    return svg_wrap(inner, ("#2E0854", "#6A0DAD", "#9370DB"))


# ============================================================
# 6 恋人 The Lovers
# ============================================================
def card_6():
    inner = f"""
  {card_title_top("恋人")}
  <!-- 天使 -->
  <circle cx="{W/2}" cy="75" r="8" fill="#FFB6C1" opacity="0.8"/>
  <path d="M{W/2-20},80 Q{W/2-30},60 {W/2-15},55" stroke="#FFB6C1" stroke-width="1.5" fill="none" opacity="0.6"/>
  <path d="M{W/2+20},80 Q{W/2+30},60 {W/2+15},55" stroke="#FFB6C1" stroke-width="1.5" fill="none" opacity="0.6"/>
  <!-- 两棵树 -->
  <rect x="45" y="110" width="8" height="80" fill="#228B22" opacity="0.6"/>
  <circle cx="49" cy="100" r="18" fill="#32CD32" opacity="0.5"/>
  <rect x="147" y="110" width="8" height="80" fill="#8B0000" opacity="0.6"/>
  <circle cx="151" cy="100" r="18" fill="#FF4500" opacity="0.4"/>
  <!-- 火焰(知识树) -->
  <text x="145" y="95" fill="#FF4500" font-size="10" opacity="0.7">🔥</text>
  <!-- 心形 -->
  <path d="M{W/2},120 Q{W/2-20},100 {W/2},115 Q{W/2+20},100 {W/2},120" fill="#FF1493" opacity="0.8" filter="url(#glow)"/>
  <!-- 太阳光线 -->
  <line x1="{W/2}" y1="50" x2="{W/2}" y2="35" stroke="#FFD700" stroke-width="1.5" opacity="0.6"/>
  <line x1="{W/2-15}" y1="55" x2="{W/2-25}" y2="42" stroke="#FFD700" stroke-width="1" opacity="0.4"/>
  <line x1="{W/2+15}" y1="55" x2="{W/2+25}" y2="42" stroke="#FFD700" stroke-width="1" opacity="0.4"/>
  <!-- 山 -->
  <polygon points="30,200 100,155 170,200" fill="#FF69B4" opacity="0.2"/>
  {card_label(6, "恋人", "The Lovers")}"""
    return svg_wrap(inner, ("#FFB6C1", "#FF69B4", "#FF1493"))


# ============================================================
# 7 战车 The Chariot
# ============================================================
def card_7():
    inner = f"""
  {card_title_top("战车")}
  <!-- 星星冠 -->
  <path d="M70,70 L100,55 L130,70" stroke="#FFD700" stroke-width="2" fill="none"/>
  <circle cx="85" cy="62" r="3" fill="#FFD700"/>
  <circle cx="100" cy="57" r="3.5" fill="#FFD700"/>
  <circle cx="115" cy="62" r="3" fill="#FFD700"/>
  <!-- 车身 -->
  <rect x="60" y="120" width="80" height="50" rx="5" fill="#B8860B" opacity="0.6" stroke="#d4af37" stroke-width="1.5"/>
  <!-- 翅膀 -->
  <path d="M60,130 Q40,110 50,95" stroke="#d4af37" stroke-width="2" fill="none"/>
  <path d="M60,135 Q35,120 45,105" stroke="#d4af37" stroke-width="1.5" fill="none"/>
  <path d="M140,130 Q160,110 150,95" stroke="#d4af37" stroke-width="2" fill="none"/>
  <path d="M140,135 Q165,120 155,105" stroke="#d4af37" stroke-width="1.5" fill="none"/>
  <!-- 车轮 -->
  <circle cx="80" cy="180" r="12" fill="none" stroke="#d4af37" stroke-width="2"/>
  <circle cx="120" cy="180" r="12" fill="none" stroke="#d4af37" stroke-width="2"/>
  <line x1="80" y1="168" x2="80" y2="192" stroke="#d4af37" stroke-width="1"/>
  <line x1="68" y1="180" x2="92" y2="180" stroke="#d4af37" stroke-width="1"/>
  <line x1="120" y1="168" x2="120" y2="192" stroke="#d4af37" stroke-width="1"/>
  <line x1="108" y1="180" x2="132" y2="180" stroke="#d4af37" stroke-width="1"/>
  <!-- 拉车的兽 -->
  <circle cx="85" cy="100" r="8" fill="#FFD700" opacity="0.5"/>
  <circle cx="115" cy="100" r="8" fill="#1a1a1a" opacity="0.5"/>
  {card_label(7, "战车", "The Chariot")}"""
    return svg_wrap(inner, ("#B8860B", "#DAA520", "#FFD700"))


# ============================================================
# 8 力量 Strength
# ============================================================
def card_8():
    inner = f"""
  {card_title_top("力量")}
  <!-- 无限符号 -->
  <path d="M75,65 Q85,50 100,65 Q115,80 125,65" stroke="#FFD700" stroke-width="2.5" fill="none" filter="url(#glow)"/>
  <path d="M75,65 Q85,80 100,65 Q115,50 125,65" stroke="#FFD700" stroke-width="2.5" fill="none"/>
  <!-- 狮子 -->
  <ellipse cx="{W/2}" cy="130" r="25" ry="20" fill="#D2691E" opacity="0.7"/>
  <circle cx="90" cy="120" r="12" fill="#D2691E" opacity="0.8"/>
  <!-- 鬃毛 -->
  <path d="M78,110 Q70,100 78,95" stroke="#8B4513" stroke-width="2" fill="none"/>
  <path d="M82,108 Q75,95 82,88" stroke="#8B4513" stroke-width="2" fill="none"/>
  <path d="M98,108 Q105,95 98,88" stroke="#8B4513" stroke-width="2" fill="none"/>
  <path d="M102,110 Q110,100 102,95" stroke="#8B4513" stroke-width="2" fill="none"/>
  <!-- 眼睛 -->
  <circle cx="87" cy="118" r="2" fill="#FFD700"/>
  <circle cx="93" cy="118" r="2" fill="#FFD700"/>
  <!-- 女子的手 -->
  <path d="M70,100 Q65,115 72,125" stroke="#FFDAB9" stroke-width="3" fill="none" stroke-linecap="round"/>
  <!-- 花环 -->
  <path d="M68,100 Q{W/2},85 132,100" stroke="#32CD32" stroke-width="1.5" fill="none"/>
  <circle cx="85" cy="92" r="3" fill="#FF69B4" opacity="0.7"/>
  <circle cx="100" cy="88" r="3" fill="#FFB6C1" opacity="0.7"/>
  <circle cx="115" cy="92" r="3" fill="#FF69B4" opacity="0.7"/>
  <!-- 山丘 -->
  <ellipse cx="{W/2}" cy="200" rx="70" ry="15" fill="#8B4513" opacity="0.3"/>
  {card_label(8, "力量", "Strength")}"""
    return svg_wrap(inner, ("#8B4513", "#D2691E", "#FF8C00"))


# ============================================================
# 9 隐士 The Hermit
# ============================================================
def card_9():
    inner = f"""
  {card_title_top("隐士")}
  <!-- 灯笼 -->
  <circle cx="{W/2}" cy="80" r="12" fill="#FFD700" opacity="0.8" filter="url(#softglow)"/>
  <circle cx="{W/2}" cy="80" r="8" fill="#FFF8DC"/>
  <rect x="{W/2-2}" y="72" width="4" height="3" fill="#d4af37"/>
  <!-- 灯笼架 -->
  <line x1="{W/2}" y1="68" x2="{W/2}" y2="60" stroke="#d4af37" stroke-width="1.5"/>
  <line x1="{W/2-8}" y1="60" x2="{W/2+8}" y2="60" stroke="#d4af37" stroke-width="2"/>
  <!-- 隐士身形 -->
  <path d="M{W/2},95 L{W/2},170" stroke="#696969" stroke-width="3" fill="none"/>
  <path d="M{W/2-15},120 L{W/2},105 L{W/2+15},120" stroke="#696969" stroke-width="2" fill="#808080" opacity="0.5"/>
  <!-- 杖 -->
  <line x1="{W/2+15}" y1="100" x2="{W/2+15}" y2="185" stroke="#8B8682" stroke-width="2.5"/>
  <!-- 雪山 -->
  <polygon points="30,200 60,140 90,200" fill="#A9A9A9" opacity="0.4"/>
  <polygon points="110,200 140,130 170,200" fill="#808080" opacity="0.4"/>
  <polygon points="60,200 100,120 140,200" fill="#696969" opacity="0.3"/>
  <!-- 雪 -->
  <text x="55" y="145" fill="#C0C0C0" font-size="6" opacity="0.5">❄</text>
  <text x="140" y="140" fill="#C0C0C0" font-size="5" opacity="0.4">❄</text>
  {card_label(9, "隐士", "The Hermit")}"""
    return svg_wrap(inner, ("#2F4F4F", "#696969", "#A9A9A9"))


# ============================================================
# 10 命运之轮 Wheel of Fortune
# ============================================================
def card_10():
    inner = f"""
  {card_title_top("命运之轮")}
  <!-- 外圈 -->
  <circle cx="{W/2}" cy="120" r="45" fill="none" stroke="#d4af37" stroke-width="2.5"/>
  <circle cx="{W/2}" cy="120" r="38" fill="none" stroke="#8A2BE2" stroke-width="1.5"/>
  <circle cx="{W/2}" cy="120" r="30" fill="none" stroke="#d4af37" stroke-width="1"/>
  <!-- 轮辐 -->
  <line x1="{W/2}" y1="80" x2="{W/2}" y2="160" stroke="#d4af37" stroke-width="1.5"/>
  <line x1="55" y1="120" x2="145" y2="120" stroke="#d4af37" stroke-width="1.5"/>
  <line x1="68" y1="88" x2="132" y2="152" stroke="#d4af37" stroke-width="1"/>
  <line x1="132" y1="88" x2="68" y2="152" stroke="#d4af37" stroke-width="1"/>
  <!-- 中心 -->
  <circle cx="{W/2}" cy="120" r="10" fill="#4B0082" stroke="#d4af37" stroke-width="1.5"/>
  <text x="{W/2}" y="124" text-anchor="middle" fill="#FFD700" font-size="10">☉</text>
  <!-- 符号 -->
  <text x="{W/2}" y="78" text-anchor="middle" fill="#d4af37" font-size="12">♉</text>
  <text x="{W/2}" y="170" text-anchor="middle" fill="#d4af37" font-size="12">♏</text>
  <text x="50" y="124" fill="#d4af37" font-size="12">♒</text>
  <text x="148" y="124" fill="#d4af37" font-size="12">♌</text>
  <!-- 神秘生物 -->
  <text x="45" y="85" fill="#4169E1" font-size="14" opacity="0.6">🐍</text>
  <text x="140" y="85" fill="#B22222" font-size="14" opacity="0.6">🦅</text>
  {card_label(10, "命运之轮", "Wheel of Fortune")}"""
    return svg_wrap(inner, ("#000080", "#4B0082", "#8A2BE2"))


# ============================================================
# 11 正义 Justice
# ============================================================
def card_11():
    inner = f"""
  {card_title_top("正义")}
  <!-- 天平 -->
  <line x1="{W/2}" y1="70" x2="{W/2}" y2="130" stroke="#d4af37" stroke-width="2"/>
  <line x1="65" y1="90" x2="135" y2="90" stroke="#d4af37" stroke-width="2"/>
  <!-- 左盘 -->
  <path d="M65,90 L55,110 L75,110 Z" fill="none" stroke="#d4af37" stroke-width="1.5"/>
  <line x1="55" y1="110" x2="75" y2="110" stroke="#d4af37" stroke-width="1.5"/>
  <!-- 右盘 -->
  <path d="M135,90 L125,110 L145,110 Z" fill="none" stroke="#d4af37" stroke-width="1.5"/>
  <line x1="125" y1="110" x2="145" y2="110" stroke="#d4af37" stroke-width="1.5"/>
  <!-- 剑 -->
  <line x1="145" y1="70" x2="145" y2="170" stroke="#C0C0C0" stroke-width="3"/>
  <line x1="140" y1="90" x2="150" y2="90" stroke="#C0C0C0" stroke-width="2"/>
  <polygon points="145,70 141,78 149,78" fill="#C0C0C0"/>
  <!-- 紫色帷幕 -->
  <path d="M40,70 Q{W/2},60 160,70" stroke="#00CED1" stroke-width="1" fill="none" opacity="0.5"/>
  <!-- 柱子 -->
  <rect x="45" y="70" width="8" height="120" fill="#20B2AA" opacity="0.3" rx="2"/>
  <rect x="147" y="70" width="8" height="120" fill="#20B2AA" opacity="0.3" rx="2"/>
  {card_label(11, "正义", "Justice")}"""
    return svg_wrap(inner, ("#00CED1", "#20B2AA", "#48D1CC"))


# ============================================================
# 12 倒吊人 The Hanged Man
# ============================================================
def card_12():
    inner = f"""
  {card_title_top("倒吊人")}
  <!-- T型架 -->
  <line x1="55" y1="65" x2="145" y2="65" stroke="#8B8682" stroke-width="4"/>
  <line x1="{W/2}" y1="55" x2="{W/2}" y2="65" stroke="#8B8682" stroke-width="4"/>
  <!-- 倒吊的人 -->
  <circle cx="{W/2}" cy="100" r="10" fill="#FFDAB9" opacity="0.8"/>
  <line x1="{W/2}" y1="110" x2="{W/2}" y2="170" stroke="#5F9EA0" stroke-width="3"/>
  <!-- 双臂展开 -->
  <line x1="{W/2-25}" y1="130" x2="{W/2+25}" y2="130" stroke="#5F9EA0" stroke-width="2.5"/>
  <!-- 绳索 -->
  <line x1="{W/2}" y1="65" x2="{W/2}" y2="90" stroke="#DAA520" stroke-width="2"/>
  <!-- 光环 -->
  <circle cx="{W/2}" cy="100" r="15" fill="none" stroke="#FFD700" stroke-width="1" opacity="0.5"/>
  <!-- 腿交叉 -->
  <line x1="{W/2}" y1="170" x2="{W/2-15}" y2="190" stroke="#5F9EA0" stroke-width="2"/>
  <line x1="{W/2}" y1="170" x2="{W/2+15}" y2="190" stroke="#5F9EA0" stroke-width="2"/>
  <!-- 水/波浪 -->
  <path d="M40,195 Q60,185 80,195 Q100,205 120,195 Q140,185 160,195" stroke="#00CED1" stroke-width="1.5" fill="none" opacity="0.5"/>
  <path d="M35,205 Q60,195 80,205 Q100,215 120,205 Q140,195 165,205" stroke="#00CED1" stroke-width="1" fill="none" opacity="0.3"/>
  <!-- 树叶 -->
  <text x="45" y="80" fill="#32CD32" font-size="8" opacity="0.5">🍃</text>
  <text x="150" y="78" fill="#32CD32" font-size="7" opacity="0.4">🍃</text>
  {card_label(12, "倒吊人", "The Hanged Man")}"""
    return svg_wrap(inner, ("#008B8B", "#2F4F4F", "#5F9EA0"))


# ============================================================
# 13 死神 Death
# ============================================================
def card_13():
    inner = f"""
  {card_title_top("死神")}
  <!-- 骷髅头 -->
  <ellipse cx="{W/2}" cy="95" rx="18" ry="22" fill="#E8E8E8" opacity="0.9"/>
  <ellipse cx="90" cy="90" rx="5" ry="6" fill="#1C1C1C"/>
  <ellipse cx="110" cy="90" rx="5" ry="6" fill="#1C1C1C"/>
  <path d="M95,102 Q100,106 105,102" stroke="#1C1C1C" stroke-width="1.5" fill="none"/>
  <line x1="96" y1="108" x2="96" y2="112" stroke="#1C1C1C" stroke-width="1"/>
  <line x1="100" y1="108" x2="100" y2="113" stroke="#1C1C1C" stroke-width="1"/>
  <line x1="104" y1="108" x2="104" y2="112" stroke="#1C1C1C" stroke-width="1"/>
  <!-- 镰刀 -->
  <path d="M140,70 Q155,90 140,110 Q125,130 135,150" stroke="#C0C0C0" stroke-width="3" fill="none"/>
  <path d="M140,70 Q160,75 155,85" stroke="#C0C0C0" stroke-width="2" fill="none"/>
  <!-- 黑色旗帜 -->
  <rect x="40" y="130" width="35" height="50" fill="#1C1C1C" opacity="0.8"/>
  <circle cx="57" cy="150" r="8" fill="none" stroke="#C0C0C0" stroke-width="1" opacity="0.5"/>
  <text x="57" y="154" text-anchor="middle" fill="#C0C0C0" font-size="8" opacity="0.6">✝</text>
  <!-- 玫瑰 -->
  <circle cx="75" cy="140" r="5" fill="#FF0000" opacity="0.6"/>
  <circle cx="75" cy="140" r="3" fill="#8B0000"/>
  <!-- 月亮 -->
  <circle cx="150" cy="60" r="10" fill="#C0C0C0" opacity="0.3"/>
  <circle cx="154" cy="58" r="9" fill="#1C1C1C" opacity="0.8"/>
  <!-- 地面 -->
  <rect x="20" y="190" width="160" height="5" fill="#3C3C3C" opacity="0.5" rx="2"/>
  {card_label(13, "死神", "Death")}"""
    return svg_wrap(inner, ("#000000", "#1C1C1C", "#3C3C3C"))


# ============================================================
# 14 节制 Temperance
# ============================================================
def card_14():
    inner = f"""
  {card_title_top("节制")}
  <!-- 天使 -->
  <circle cx="{W/2}" cy="80" r="10" fill="#FFDAB9" opacity="0.8"/>
  <!-- 翅膀 -->
  <path d="M{W/2-15},85 Q{W/2-35},70 {W/2-25},55" stroke="#C0C0C0" stroke-width="1.5" fill="none" opacity="0.6"/>
  <path d="M{W/2-12},88 Q{W/2-30},78 {W/2-22},65" stroke="#C0C0C0" stroke-width="1" fill="none" opacity="0.4"/>
  <path d="M{W/2+15},85 Q{W/2+35},70 {W/2+25},55" stroke="#C0C0C0" stroke-width="1.5" fill="none" opacity="0.6"/>
  <path d="M{W/2+12},88 Q{W/2+30},78 {W/2+22},65" stroke="#C0C0C0" stroke-width="1" fill="none" opacity="0.4"/>
  <!-- 两个杯子 -->
  <path d="M65,120 L60,145 L80,145 L75,120 Z" fill="none" stroke="#d4af37" stroke-width="1.5"/>
  <path d="M125,120 L120,145 L140,145 L135,120 Z" fill="none" stroke="#d4af37" stroke-width="1.5"/>
  <!-- 水流 -->
  <path d="M72,145 Q{W/2},160 128,145" stroke="#00CED1" stroke-width="2" fill="none" opacity="0.7"/>
  <path d="M72,150 Q{W/2},170 128,150" stroke="#00CED1" stroke-width="1.5" fill="none" opacity="0.5"/>
  <!-- 太阳 -->
  <circle cx="{W/2}" cy="65" r="6" fill="#FFD700" opacity="0.6" filter="url(#softglow)"/>
  <!-- 鸢尾花 -->
  <path d="M{W/2},175 L{W/2},200" stroke="#32CD32" stroke-width="2"/>
  <circle cx="{W/2}" cy="172" r="6" fill="#66CDAA" opacity="0.6"/>
  <path d="M{W/2-8},175 Q{W/2},165 {W/2+8},175" fill="#2E8B57" opacity="0.5"/>
  <!-- 路径 -->
  <path d="M40,200 Q{W/2},185 160,200" stroke="#2E8B57" stroke-width="1" fill="none" opacity="0.4"/>
  {card_label(14, "节制", "Temperance")}"""
    return svg_wrap(inner, ("#006400", "#2E8B57", "#66CDAA"))


# ============================================================
# 15 恶魔 The Devil
# ============================================================
def card_15():
    inner = f"""
  {card_title_top("恶魔")}
  <!-- 倒五芒星 -->
  <polygon points="{W/2},68 120,105 105,140 95,140 80,105" fill="none" stroke="#FF0000" stroke-width="1.5" opacity="0.6"/>
  <!-- 恶魔之脸 -->
  <ellipse cx="{W/2}" cy="100" rx="22" ry="25" fill="#4A0000" stroke="#800000" stroke-width="1.5"/>
  <!-- 角 -->
  <path d="M78,80 Q70,60 80,55" stroke="#800000" stroke-width="3" fill="none"/>
  <path d="M122,80 Q130,60 120,55" stroke="#800000" stroke-width="3" fill="none"/>
  <!-- 眼睛 -->
  <ellipse cx="90" cy="95" rx="4" ry="5" fill="#FF0000" opacity="0.8"/>
  <ellipse cx="110" cy="95" rx="4" ry="5" fill="#FF0000" opacity="0.8"/>
  <circle cx="90" cy="95" r="2" fill="#FFD700"/>
  <circle cx="110" cy="95" r="2" fill="#FFD700"/>
  <!-- 嘴 -->
  <path d="M88,108 Q100,118 112,108" stroke="#FF0000" stroke-width="1.5" fill="#2A0000"/>
  <!-- 翅膀 -->
  <path d="M60,90 Q40,70 50,50 Q55,65 65,75" fill="#4A0000" opacity="0.6"/>
  <path d="M140,90 Q160,70 150,50 Q145,65 135,75" fill="#4A0000" opacity="0.6"/>
  <!-- 锁链 -->
  <line x1="80" y1="130" x2="70" y2="180" stroke="#808080" stroke-width="2"/>
  <line x1="120" y1="130" x2="130" y2="180" stroke="#808080" stroke-width="2"/>
  <circle cx="70" cy="180" r="5" fill="none" stroke="#808080" stroke-width="1.5"/>
  <circle cx="130" cy="180" r="5" fill="none" stroke="#808080" stroke-width="1.5"/>
  <!-- 火焰 -->
  <text x="55" y="195" fill="#FF4500" font-size="12" opacity="0.6">🔥</text>
  <text x="130" y="195" fill="#FF4500" font-size="12" opacity="0.6">🔥</text>
  {card_label(15, "恶魔", "The Devil")}"""
    return svg_wrap(inner, ("#1A0000", "#4A0000", "#800000"))


# ============================================================
# 16 塔 The Tower
# ============================================================
def card_16():
    inner = f"""
  {card_title_top("塔")}
  <!-- 塔 -->
  <rect x="70" y="80" width="60" height="120" fill="#8B4513" opacity="0.7"/>
  <rect x="75" y="75" width="50" height="15" fill="#A0522D" opacity="0.8"/>
  <!-- 塔顶 -->
  <rect x="80" y="65" width="40" height="15" fill="#654321" opacity="0.8"/>
  <!-- 窗户 -->
  <rect x="90" y="100" width="20" height="25" fill="#000" opacity="0.6" rx="10"/>
  <rect x="90" y="140" width="20" height="20" fill="#000" opacity="0.6" rx="2"/>
  <!-- 闪电 -->
  <path d="M{W/2},40 L95,75 L105,70 L90,100" stroke="#FFD700" stroke-width="3" fill="none" filter="url(#glow)"/>
  <polygon points="100,40 90,65 100,60 85,90" fill="#FFD700" opacity="0.8"/>
  <!-- 火焰 -->
  <circle cx="85" cy="85" r="8" fill="#FF4500" opacity="0.6"/>
  <circle cx="115" cy="88" r="6" fill="#FF6347" opacity="0.5"/>
  <circle cx="100" cy="80" r="5" fill="#FFD700" opacity="0.4"/>
  <!-- 坠落的人 -->
  <circle cx="60" cy="130" r="4" fill="#FFDAB9" opacity="0.6"/>
  <line x1="60" y1="134" x2="55" y2="155" stroke="#5F9EA0" stroke-width="1.5" opacity="0.5"/>
  <circle cx="140" cy="125" r="4" fill="#FFDAB9" opacity="0.6"/>
  <line x1="140" y1="129" x2="145" y2="150" stroke="#5F9EA0" stroke-width="1.5" opacity="0.5"/>
  <!-- 碎片 -->
  <rect x="50" y="170" width="8" height="5" fill="#8B4513" opacity="0.5" transform="rotate(15,54,172)"/>
  <rect x="140" y="175" width="6" height="4" fill="#A0522D" opacity="0.4" transform="rotate(-10,143,177)"/>
  <!-- 雨/碎片 -->
  <text x="45" y="110" fill="#FFD700" font-size="6" opacity="0.4">✦</text>
  <text x="150" y="105" fill="#FFD700" font-size="5" opacity="0.3">✦</text>
  {card_label(16, "塔", "The Tower")}"""
    return svg_wrap(inner, ("#FF4500", "#FF6347", "#FF7F50"))


# ============================================================
# 17 星星 The Star
# ============================================================
def card_17():
    inner = f"""
  {card_title_top("星星")}
  <!-- 大星 -->
  <polygon points="{W/2},60 {W/2+5},75 {W/2+18},75 {W/2+8},85 {W/2+12},100 {W/2},90 {W/2-12},100 {W/2-8},85 {W/2-18},75 {W/2-5},75" fill="#FFD700" filter="url(#glow)"/>
  <!-- 小星 -->
  <text x="45" y="70" fill="#FFD700" font-size="8" opacity="0.8">✦</text>
  <text x="155" y="65" fill="#FFD700" font-size="6" opacity="0.7">✦</text>
  <text x="60" y="100" fill="#FFD700" font-size="5" opacity="0.5">✦</text>
  <text x="140" y="95" fill="#FFD700" font-size="7" opacity="0.6">✦</text>
  <text x="80" y="55" fill="#FFD700" font-size="4" opacity="0.4">✦</text>
  <text x="120" y="50" fill="#FFD700" font-size="5" opacity="0.3">✦</text>
  <!-- 女子 -->
  <circle cx="80" cy="140" r="8" fill="#FFDAB9" opacity="0.7"/>
  <line x1="80" y1="148" x2="80" y2="185" stroke="#87CEEB" stroke-width="2" opacity="0.6"/>
  <!-- 水罐 -->
  <path d="M60,155 L55,180 L75,180 L70,155 Z" fill="none" stroke="#87CEEB" stroke-width="1.5" opacity="0.6"/>
  <!-- 水流 -->
  <path d="M60,180 Q50,195 55,210" stroke="#00CED1" stroke-width="2" fill="none" opacity="0.5"/>
  <path d="M65,180 Q55,200 60,215" stroke="#00CED1" stroke-width="1.5" fill="none" opacity="0.4"/>
  <!-- 池塘 -->
  <ellipse cx="58" cy="210" rx="15" ry="5" fill="#00CED1" opacity="0.3"/>
  <!-- 鸟 -->
  <path d="M130,150 Q135,145 140,150" stroke="#C0C0C0" stroke-width="1.5" fill="none" opacity="0.5"/>
  {card_label(17, "星星", "The Star")}"""
    return svg_wrap(inner, ("#000033", "#000066", "#000099"))


# ============================================================
# 18 月亮 The Moon
# ============================================================
def card_18():
    inner = f"""
  {card_title_top("月亮")}
  <!-- 月亮 -->
  <circle cx="{W/2}" cy="75" r="22" fill="#C0C0C0" opacity="0.8"/>
  <circle cx="{W/2+7}" cy="72" r="20" fill="#0D0D2B" opacity="0.9"/>
  <!-- 月亮脸 -->
  <circle cx="90" cy="72" r="2" fill="#C0C0C0" opacity="0.4"/>
  <circle cx="95" cy="78" r="1.5" fill="#C0C0C0" opacity="0.3"/>
  <!-- 水滴 -->
  <circle cx="80" cy="68" r="3" fill="#C0C0C0" opacity="0.3"/>
  <circle cx="120" cy="72" r="2.5" fill="#C0C0C0" opacity="0.25"/>
  <circle cx="70" cy="78" r="2" fill="#C0C0C0" opacity="0.2"/>
  <!-- 塔 -->
  <rect x="55" y="110" width="15" height="50" fill="#1A1A4E" opacity="0.7"/>
  <rect x="130" y="115" width="15" height="45" fill="#1A1A4E" opacity="0.7"/>
  <!-- 小路 -->
  <path d="M{W/2},120 Q80,150 60,175 Q50,190 55,200" stroke="#C0C0C0" stroke-width="1" fill="none" opacity="0.3"/>
  <path d="M{W/2},120 Q120,150 140,175 Q150,190 145,200" stroke="#C0C0C0" stroke-width="1" fill="none" opacity="0.3"/>
  <!-- 蜿蜒路径 -->
  <path d="M50,200 Q70,190 90,200 Q110,210 130,200 Q150,190 165,200" stroke="#4169E1" stroke-width="1" fill="none" opacity="0.3"/>
  <!-- 狼与狗 -->
  <text x="50" y="190" fill="#696969" font-size="12" opacity="0.6">🐺</text>
  <text x="135" y="188" fill="#A9A9A9" font-size="12" opacity="0.5">🐕</text>
  <!-- 虾 -->
  <text x="95" y="155" fill="#FF6347" font-size="10" opacity="0.4">🦐</text>
  <!-- 星星 -->
  <text x="40" y="60" fill="#C0C0C0" font-size="5" opacity="0.4">✦</text>
  <text x="160" y="55" fill="#C0C0C0" font-size="4" opacity="0.3">✦</text>
  {card_label(18, "月亮", "The Moon")}"""
    return svg_wrap(inner, ("#0D0D2B", "#1A1A4E", "#2D2D6B"))


# ============================================================
# 19 太阳 The Sun
# ============================================================
def card_19():
    inner = f"""
  {card_title_top("太阳")}
  <!-- 太阳 -->
  <circle cx="{W/2}" cy="85" r="28" fill="#FFD700" filter="url(#softglow)"/>
  <circle cx="{W/2}" cy="85" r="22" fill="#FFFF00"/>
  <!-- 太阳光线 -->
  <line x1="{W/2}" y1="50" x2="{W/2}" y2="40" stroke="#FFD700" stroke-width="2.5"/>
  <line x1="{W/2-25}" y1="60" x2="{W/2-33}" y2="52" stroke="#FFD700" stroke-width="2"/>
  <line x1="{W/2+25}" y1="60" x2="{W/2+33}" y2="52" stroke="#FFD700" stroke-width="2"/>
  <line x1="{W/2-35}" y1="85" x2="{W/2-45}" y2="85" stroke="#FFD700" stroke-width="2"/>
  <line x1="{W/2+35}" y1="85" x2="{W/2+45}" y2="85" stroke="#FFD700" stroke-width="2"/>
  <line x1="{W/2-25}" y1="110" x2="{W/2-33}" y2="118" stroke="#FFD700" stroke-width="2"/>
  <line x1="{W/2+25}" y1="110" x2="{W/2+33}" y2="118" stroke="#FFD700" stroke-width="2"/>
  <!-- 太阳脸 -->
  <circle cx="93" cy="80" r="3" fill="#FFA500"/>
  <circle cx="107" cy="80" r="3" fill="#FFA500"/>
  <path d="M93,90 Q100,96 107,90" stroke="#FFA500" stroke-width="1.5" fill="none"/>
  <!-- 孩子/马 -->
  <circle cx="80" cy="165" r="8" fill="#FFDAB9" opacity="0.8"/>
  <line x1="80" y1="173" x2="80" y2="200" stroke="#FFD700" stroke-width="2.5"/>
  <line x1="70" y1="185" x2="90" y2="185" stroke="#FFD700" stroke-width="2"/>
  <!-- 向日葵 -->
  <circle cx="120" cy="160" r="6" fill="#FFD700" opacity="0.7"/>
  <circle cx="120" cy="160" r="3" fill="#8B4513"/>
  <line x1="120" y1="166" x2="120" y2="200" stroke="#32CD32" stroke-width="2"/>
  <circle cx="140" cy="170" r="5" fill="#FFD700" opacity="0.6"/>
  <circle cx="140" cy="170" r="2.5" fill="#8B4513"/>
  <line x1="140" y1="175" x2="140" y2="200" stroke="#32CD32" stroke-width="1.5"/>
  <!-- 围墙 -->
  <rect x="35" y="200" width="130" height="8" fill="#DAA520" opacity="0.4" rx="2"/>
  {card_label(19, "太阳", "The Sun")}"""
    return svg_wrap(inner, ("#FFA500", "#FFD700", "#FFFF00"))


# ============================================================
# 20 审判 Judgement
# ============================================================
def card_20():
    inner = f"""
  {card_title_top("审判")}
  <!-- 天使号角 -->
  <path d="M{W/2},55 Q{W/2+30},65 {W/2+25},90" stroke="#d4af37" stroke-width="3" fill="none"/>
  <circle cx="{W/2}" cy="53" r="5" fill="#FFD700" filter="url(#glow)"/>
  <!-- 旗帜 -->
  <rect x="118" y="58" width="20" height="30" fill="#C0C0C0" opacity="0.6"/>
  <text x="128" y="78" text-anchor="middle" fill="#d4af37" font-size="10">✝</text>
  <!-- 复活的人 -->
  <circle cx="70" cy="140" r="7" fill="#FFDAB9" opacity="0.7"/>
  <line x1="70" y1="147" x2="70" y2="185" stroke="#C0C0C0" stroke-width="2"/>
  <line x1="60" y1="160" x2="80" y2="160" stroke="#C0C0C0" stroke-width="1.5"/>
  <circle cx="100" cy="145" r="7" fill="#FFDAB9" opacity="0.7"/>
  <line x1="100" y1="152" x2="100" y2="185" stroke="#C0C0C0" stroke-width="2"/>
  <line x1="90" y1="165" x2="110" y2="165" stroke="#C0C0C0" stroke-width="1.5"/>
  <circle cx="130" cy="140" r="7" fill="#FFDAB9" opacity="0.7"/>
  <line x1="130" y1="147" x2="130" y2="185" stroke="#C0C0C0" stroke-width="2"/>
  <line x1="120" y1="160" x2="140" y2="160" stroke="#C0C0C0" stroke-width="1.5"/>
  <!-- 光芒 -->
  <line x1="{W/2}" y1="100" x2="60" y2="130" stroke="#FFD700" stroke-width="1" opacity="0.4"/>
  <line x1="{W/2}" y1="100" x2="100" y2="135" stroke="#FFD700" stroke-width="1" opacity="0.4"/>
  <line x1="{W/2}" y1="100" x2="140" y2="130" stroke="#FFD700" stroke-width="1" opacity="0.4"/>
  <!-- 棺材/地面 -->
  <rect x="40" y="190" width="120" height="10" fill="#708090" opacity="0.5" rx="2"/>
  <!-- 山脉 -->
  <polygon points="30,210 100,180 170,210" fill="#A9A9A9" opacity="0.2"/>
  {card_label(20, "审判", "Judgement")}"""
    return svg_wrap(inner, ("#708090", "#C0C0C0", "#DCDCDC"))


# ============================================================
# 21 世界 The World
# ============================================================
def card_21():
    inner = f"""
  {card_title_top("世界")}
  <!-- 花环 -->
  <ellipse cx="{W/2}" cy="120" rx="50" ry="55" fill="none" stroke="#32CD32" stroke-width="3"/>
  <ellipse cx="{W/2}" cy="120" rx="45" ry="50" fill="none" stroke="#228B22" stroke-width="1.5"/>
  <!-- 花朵 -->
  <circle cx="55" cy="100" r="5" fill="#FF69B4" opacity="0.7"/>
  <circle cx="145" cy="100" r="5" fill="#FF69B4" opacity="0.7"/>
  <circle cx="55" cy="140" r="5" fill="#FFB6C1" opacity="0.7"/>
  <circle cx="145" cy="140" r="5" fill="#FFB6C1" opacity="0.7"/>
  <circle cx="{W/2}" cy="65" r="4" fill="#FF1493" opacity="0.6"/>
  <circle cx="{W/2}" cy="175" r="4" fill="#FF1493" opacity="0.6"/>
  <!-- 舞者 -->
  <circle cx="{W/2}" cy="105" r="8" fill="#FFDAB9" opacity="0.8"/>
  <line x1="{W/2}" y1="113" x2="{W/2}" y2="145" stroke="#9370DB" stroke-width="2.5"/>
  <line x1="{W/2-20}" y1="125" x2="{W/2+20}" y2="125" stroke="#9370DB" stroke-width="2"/>
  <line x1="{W/2}" y1="145" x2="{W/2-12}" y2="165" stroke="#9370DB" stroke-width="2"/>
  <line x1="{W/2}" y1="145" x2="{W/2+12}" y2="165" stroke="#9370DB" stroke-width="2"/>
  <!-- 飘带 -->
  <path d="M{W/2-15},120 Q{W/2-30},130 {W/2-20},145" stroke="#DDA0DD" stroke-width="1.5" fill="none" opacity="0.6"/>
  <path d="M{W/2+15},120 Q{W/2+30},130 {W/2+20},145" stroke="#DDA0DD" stroke-width="1.5" fill="none" opacity="0.6"/>
  <!-- 四角符号 -->
  <text x="42" y="80" fill="#4169E1" font-size="12" opacity="0.6">♉</text>
  <text x="148" y="80" fill="#B22222" font-size="12" opacity="0.6">♌</text>
  <text x="42" y="170" fill="#00CED1" font-size="12" opacity="0.6">♒</text>
  <text x="148" y="170" fill="#32CD32" font-size="12" opacity="0.6">♏</text>
  <!-- 彩虹光 -->
  <path d="M50,190 Q{W/2},175 150,190" stroke="#FF0000" stroke-width="1" fill="none" opacity="0.3"/>
  <path d="M50,193 Q{W/2},178 150,193" stroke="#FFD700" stroke-width="1" fill="none" opacity="0.3"/>
  <path d="M50,196 Q{W/2},181 150,196" stroke="#00FF00" stroke-width="1" fill="none" opacity="0.3"/>
  <path d="M50,199 Q{W/2},184 150,199" stroke="#0000FF" stroke-width="1" fill="none" opacity="0.3"/>
  {card_label(21, "世界", "The World")}"""
    return svg_wrap(inner, ("#FF0000", "#00FF00", "#0000FF"))


# ============================================================
# 生成所有卡片
# ============================================================
cards = [
    card_0,
    card_1,
    card_2,
    card_3,
    card_4,
    card_5,
    card_6,
    card_7,
    card_8,
    card_9,
    card_10,
    card_11,
    card_12,
    card_13,
    card_14,
    card_15,
    card_16,
    card_17,
    card_18,
    card_19,
    card_20,
    card_21,
]

for i, gen in enumerate(cards):
    svg_content = gen()
    filepath = os.path.join(OUTPUT_DIR, f"{i:02d}.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated: {filepath}")

print(f"\nDone! Generated {len(cards)} SVG cards.")
