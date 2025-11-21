import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 数据源 (模拟真实推特) ---

def get_binance_alpha(hour):
    current_hour = int(hour)
    
    # 逻辑：只有 12 点以后才会有 Alpha
    # 如果没到 12 点，直接返回 None (代表没消息)
    if current_hour < 12:
        return None 
    
    # 模拟下午/晚上的 Alpha
    claim_minute = random.choice(["15", "30", "45"])
    points = random.choice([1000, 2000, 3500, 5000])
    
    return {
        "category": "Alpha",
        "tag": "🔥 重点",
        "title": "币安 Alpha · 限时开启",
        "summary": f"大家要注意哦，币安中文官推刚刚更新了。今天的领取时间是【{current_hour}:{claim_minute}】。积分门槛是 {points} 分。记得提前准备好钱包，不要错过啦。",
        "length": 60
    }

def get_crypto_news():
    templates = [
        ("BTC 突破新高", "华尔街那边好像又在疯狂买入呢，看来大牛市真的要来了。"),
        ("以太坊 Gas 费好低", "现在交互真的很划算，V神说 Layer2 的体验会越来越好哦。"),
        ("Solana 上又出金狗了", "听说有个聪明钱地址一晚翻了好多倍，大家投资要注意风险哦。"),
        ("美联储可能会降息", "这对市场可是个大好消息呢，流动性又要好起来了。")
    ]
    # 随机选 2 条
    return generate_items(templates, "币圈", ["行情", "动态"])

def get_other_news():
    templates = [
        ("马斯克又发推特了", "他好像真的想把人类送上火星呢，真是一个疯狂又迷人的梦想。"),
        ("OpenAI 发布了新模型", "AI 进化的速度好快呀，感觉我们的生活每天都在变。"),
        ("科学家发现了新生物", "大自然真的好神奇，还有好多我们不知道的秘密呢。")
    ]
    # 随机选 1 条
    return generate_items(templates, "趣闻", ["科技", "生活"])

def generate_items(templates, category, tags):
    items = []
    for title, detail in random.sample(templates, len(templates) if len(templates)<2 else 2):
        items.append({
            "category": category,
            "tag": random.choice(tags),
            "title": title,
            "summary": detail,
            "length": len(title) + len(detail)
        })
    return items

# --- 2. 广播稿生成 (志玲姐姐版) ---
def create_chiling_script(alpha, crypto, others, hour_str):
    # 志玲风开场：温柔、亲切
    intro = f"哈喽大家好呀，现在是北京时间 {hour_str} 点整。我是你们的 AI 助理志玲。来看看今天币圈发生了什么吧~"
    
    text = intro
    
    # 1. 只有当 Alpha 存在时，才播报！
    if alpha:
        text += f"首先有一个非常重要的好消息要告诉大家。{alpha['summary']} "
    
    # 2. 播报行情 (温柔衔接)
    text += "然后是行情方面。 "
    for item in crypto:
        text += f"{item['title']}。{item['summary']} "
        
    # 3. 播报其他
    text += "最后还有一条有意思的新闻。 "
    for item in others:
        text += f"{item['title']}。{item['summary']} "

    outro = "好啦，今天的播报就到这里。要记得按时吃饭，照顾好自己哦。拜拜~"
    text += outro
    
    return text, len(intro), len(outro)

# --- 3. 音频生成 (指定台湾腔) ---
async def generate_audio(text):
    print(f"🎙️ 志玲姐姐正在录音 ({len(text)}字)...")
    
    # 强制使用 zh-TW-HsiaoYuNeural (最像林志玲的官方音色)
    # 语速稍微慢一点点 (-5%)，更显温柔
    communicate = edge_tts.Communicate(text, "zh-TW-HsiaoYuNeural", rate="-5%")
    await communicate.save("radio.mp3")

# --- 主程序 ---
if __name__ == "__main__":
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    today_str = beijing_now.strftime("%Y-%m-%d")
    hour_str = beijing_now.strftime("%H")
    
    # 获取数据
    alpha_item = get_binance_alpha(hour_str) # 可能是 None
    crypto_items = get_crypto_news()
    other_items = get_other_news()
    
    # 组合列表：把 None 过滤掉
    all_news = []
    if alpha_item:
        all_news.append(alpha_item)
    all_news.extend(crypto_items)
    all_news.extend(other_items)
    
    # 生成文案
    full_text, l1, l2 = create_chiling_script(alpha_item, crypto_items, other_items, hour_str)
    
    # 保存数据 (前端只用展示 title 和 summary，不需要管 voices 了，因为我们只用一个声音)
    data = {
        "date": today_str,
        "hour": hour_str,
        "news": all_news,
        "meta": { "total_len": len(full_text), "intro_len": l1 }
    }
    
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    asyncio.run(generate_audio(full_text))
