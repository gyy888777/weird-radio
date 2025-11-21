import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 数据源 (精准控制) ---
def get_binance_alpha(hour):
    current_hour = int(hour)
    
    # 【核心逻辑】
    # 如果还没到 12 点，直接返回 None。
    # 这样列表中就没有这条数据，AI 就绝对不会念“等待信号”这种废话了。
    if current_hour < 12:
        return None 
    
    # 模拟下午/晚上的 Alpha (12点后)
    claim_minute = random.choice(["15", "30", "45"])
    points = random.choice([1000, 2000, 3500, 5000])
    
    return {
        "category": "Alpha",
        "tag": "🔥 必撸",
        "title": "币安 Alpha · 领取提醒",
        "summary": f"币安中文号刚发推了，今天的领取时间是【{current_hour}:{claim_minute}】。积分门槛 {points} 分。请提前准备。",
        "length": 60
    }

def get_crypto_news():
    templates = [
        ("BTC 持续震荡", "大盘目前在 9 万刀附近横盘，主力似乎在洗盘。"),
        ("ETH 链上遇冷", "Gas 费降到了 2 gwei，适合趁现在做交互。"),
        ("Solana 金狗爆发", "聪明钱地址又翻倍了，注意冲高回落风险。"),
        ("贝莱德增持比特币", "机构依然在买买买，长期看涨逻辑不变。")
    ]
    # 随机选 3 条
    return generate_items(templates, "币圈", ["行情", "观察"])

def generate_items(templates, category, tags):
    items = []
    for title, detail in random.sample(templates, 3):
        items.append({
            "category": category,
            "tag": random.choice(tags),
            "title": title,
            "summary": detail,
            "length": len(title) + len(detail)
        })
    return items

# --- 2. 广播稿生成 (志玲姐姐·极简版) ---
def create_chiling_script(alpha_item, other_items, hour_str):
    # 志玲风开场
    text = f"哈喽，现在是北京时间 {hour_str} 点。我是志玲。"
    
    # --- 场景 A：有 Alpha (下午/晚上) ---
    if alpha_item:
        text += f"重点提醒大家，{alpha_item['summary']} "
        # 有 Alpha 时，只再多念 1 条行情标题，主次分明
        if other_items:
            text += f"另外关注一下：{other_items[0]['title']}。"
            
    # --- 场景 B：无 Alpha (早上) ---
    else:
        # 早上没 Alpha，就简单报一下行情，不提“没消息”这回事
        text += "早间行情播报。"
        # 只念标题，不念长篇大论
        for item in other_items[:2]: # 只念前2条
            text += f"{item['title']}。 "

    text += "播报结束，祝好运~"
    return text

# --- 3. 音频生成 (指定台湾
