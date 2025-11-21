import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 新闻数据源 (保留最牛的配置) ---
def get_crypto_news():
    templates = [
        ("比特币冲破10万刀", "华尔街疯狂加仓，分析师预测这只是牛市的开始。"),
        ("以太坊GAS费降至冰点", "V神发布新路线图，Layer2生态迎来史诗级爆发。"),
        ("某土狗币一晚百倍", "神秘地址精准抄底，单日获利超千万美元，引发全网FOMO。"),
        ("币安上线新Launchpool", "BNB持有者又有福了，这次的项目背景硬核，预期收益拉满。")
    ]
    return generate_items(templates, "币圈", ["暴富", "行情", "Web3"])

def get_binance_alpha(hour):
    # 模拟生成 Alpha 提醒
    mins = random.randint(10, 55)
    return [{
        "category": "Alpha",
        "tag": "必撸",
        "title": "币安今日空投提醒",
        "summary": f"注意！今日空投领取窗口将在{hour}:{mins}开启，请提前准备好Web3钱包，手慢无。",
        "length": 60
    }]

def get_other_news():
    templates = [
        ("GPT-6发布", "新模型学会了自我编程，效率提升500%，程序员直呼'危'。"),
        ("马斯克火星计划", "SpaceX星舰将不再需要人类驾驶，首批火星船票已售罄。"),
        ("躺平寄生虫", "发现一种不呼吸的生物，彻底丢弃耗能基因，被封'打工人之神'。"),
        ("二哈发报机", "狗子半夜敲饭盆，竟是摩斯密码向隔壁金毛求爱。")
    ]
    return generate_items(templates, "热点", ["科技", "奇闻"])

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

# --- 2. 极简广播稿 (零废话) ---
def create_script(all_news, hour_str):
    # 开场极其简单，直奔主题
    intro = f"北京时间{hour_str}点整。"
    full_text = intro
    
    for item in all_news:
        # 话术：直接读内容，干净利落
        # 比如：【Alpha】币安今日空投提醒。注意！今日空投...
        segment = f"{item['title']}。{item['summary']} "
        full_text += segment
        item['length'] = len(segment)

    outro = "播报结束。"
    full_text += outro
    return full_text, len(intro), len(outro)

# --- 3. 音频生成 (双女主版) ---
async def generate_audio(text):
    # 生成默认晓晓 (radio.mp3)
    print(f"🎙️ 正在生成晓晓 (radio.mp3)...")
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save("radio.mp3")
    
    # 生成“志玲风” (radio_tw.mp3) - 台湾晓雨，声音很软
    print(f"🎙️ 正在生成志玲风 (radio_tw.mp3)...")
    communicate_tw = edge_tts.Communicate(text, "zh-TW-HsiaoYuNeural")
    await communicate_tw.save("radio_tw.mp3")

# --- 主程序 ---
if __name__ == "__main__":
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    today_str = beijing_now.strftime("%Y-%m-%d")
    hour_str = beijing_now.strftime("%H")
    
    # 组合新闻：Alpha 第一，币圈第二，其他最后
    news = get_binance_alpha(hour_str) + get_crypto_news() + get_other_news()
    
    full_
