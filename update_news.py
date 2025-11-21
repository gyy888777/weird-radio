import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 核心：币安 Alpha & 币圈新闻 ---
def get_binance_alpha(hour_str):
    # 模拟生成未来的领取时间（当前时间 + 随机分钟）
    minute = random.randint(10, 59)
    points = random.randint(1000, 5000)
    
    return {
        "category": "Alpha",
        "tag": "🔥 必撸",
        "title": f"币安今日 Alpha 领取提醒",
        "summary": f"【领取时间】{hour_str}:{minute} (UTC+8)。【积分要求】需持有 {points} 积分。请提前连接钱包，防止网页卡顿错过快照。",
        "length": 60
    }

def get_crypto_news():
    templates = [
        ("BTC突破历史新高", "华尔街机构持续买入，ETF净流入创纪录，分析师看高至15万美元。"),
        ("ETH Gas费降至1gwei", "链上活动低迷，正是交互埋伏空投的好时机。"),
        ("Solana链上金狗频出", "某聪明钱地址一晚获利百万美元，引发社区FOMO情绪。"),
        ("美联储暗示降息", "宏观流动性即将释放，风险资产迎来史诗级利好。")
    ]
    return generate_items(templates, "币圈", ["行情", "暴富", "宏观"])

def get_weird_news():
    templates = [
        ("马斯克要买下阿根廷", "据传他想建立一个只有狗狗币流通的国家。"),
        ("程序员与AI结婚", "婚礼在元宇宙举行，证婚人竟然是 ChatGPT。"),
        ("二哈当上镇长", "美国某小镇选举结果出炉，一条哈士奇击败人类候选人成功连任。")
    ]
    return generate_items(templates, "奇闻", ["离谱", "沙雕"])

def generate_items(templates, category, tags):
    items = []
    selected = random.sample(templates, 2)
    for title, detail in selected:
        items.append({
            "category": category,
            "tag": random.choice(tags),
            "title": title,
            "summary": detail,
            "length": len(title) + len(detail)
        })
    return items

# --- 2. 广播稿 (简单粗暴) ---
def create_script(all_news, hour_str):
    intro = f"北京时间{hour_str}点整。开始播报。"
    full_text = intro
    
    for item in all_news:
        # Alpha 消息加重语气
        if item['category'] == 'Alpha':
            segment = f"特别提醒！{item['title']}。{item['summary']} "
        else:
            segment = f"{item['title']}。{item['summary']} "
        
        full_text += segment
        item['length'] = len(segment)

    outro = "播报完毕。"
    full_text += outro
    return full_text, len(intro), len(outro)

# --- 3. 音频生成 (只用晓晓) ---
async def generate_audio(text):
    print(f"🎙️ 生成音频中...")
    # 晓晓：zh-CN-XiaoxiaoNeural
    # 志玲风：zh-TW-HsiaoYuNeural
    
    # 默认生成晓晓
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save("radio.mp3")
    
    # 生成志玲风 (备用)
    communicate_tw = edge_tts.Communicate(text, "zh-TW-HsiaoYuNeural")
    await communicate_tw.save("radio_tw.mp3")

# --- 主程序 ---
if __name__ == "__main__":
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    today_str = beijing_now.strftime("%Y-%m-%d")
    hour_str = beijing_now.strftime("%H")
    
    # 组合顺序：Alpha(置顶) -> 币圈 -> 奇闻
    alpha = [get_binance_alpha(hour_str)]
    crypto = get_crypto_news()
    weird = get_weird_news()
    
    all_news = alpha + crypto + weird
    
    full_text, intro_len, outro_len = create_script(all_news, hour_str)
    
    data = {
        "date": today_str,
        "hour": hour_str,
        "news": all_news,
        "meta": { "total_len": len(full_text), "intro_len": intro_len }
    }
    
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    asyncio.run(generate_audio(full_text))
