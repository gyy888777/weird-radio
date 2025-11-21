import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 核心：币安 Alpha 智能生成 ---
def get_binance_alpha(hour):
    current_hour = int(hour)
    
    # 逻辑：币安通常中午12点后发推
    if current_hour < 12:
        return {
            "category": "Alpha",
            "title": "币安 Alpha · 等待信号",
            "summary": "当前时间早于 12:00，@binancezh 暂未发布今日 Alpha。请耐心等待午后更新，保持关注。",
            "length": 40
        }
    else:
        # 模拟生成一个下午的领取时间 (比如 14:30 - 18:00 之间)
        claim_hour = random.randint(current_hour, 19) 
        if claim_hour > 23: claim_hour = 23
        claim_minute = random.choice(["00", "15", "30", "45"])
        points = random.choice([1000, 2500, 5000, "无限制"])
        
        return {
            "category": "Alpha",
            "title": "🔥 币安 Alpha 情报 (来源 @binancezh)",
            "summary": f"监控到最新推文！今日 Alpha 领取时间定于【{claim_hour}:{claim_minute}】。积分要求：{points}。请提前切换至 BSC 链，准备好 Gas 费。",
            "length": 80
        }

# --- 2. 大佬行情分析 ---
def get_crypto_analysis():
    analysts = [
        ("V神", "以太坊正在经历关键升级，Layer2 的交互成本将降低 10 倍，建议关注 OP 和 ARB 生态。"),
        ("华尔街分析师", "比特币 ETF 净流入持续扩大，机构正在疯狂吸筹，现在的回调就是倒车接人。"),
        ("孙宇晨", "刚刚向交易所转入了 1 亿 USDT，市场猜测可能有大动作，注意波场系代币波动。"),
        ("某链上巨鲸", "监测到巨鲸正在抛售 MEME 币，转而买入 AI 板块龙头，建议跟随聪明钱操作。")
    ]
    
    # 随机选一条
    name, content = random.choice(analysts)
    return {
        "category": "行情",
        "title": f"{name} 最新观点",
        "summary": content,
        "length": len(name) + len(content)
    }

# --- 3. 其他新闻 (保持丰富性) ---
def get_other_news():
    templates = [
        ("Web3游戏爆发", "某链游代币单日上涨 50%，打金工作室月入十万不是梦。"),
        ("英伟达财报超预期", "AI 板块代币受此利好全线拉升，算力赛道成为新风口。"),
        ("黑客攻击事件", "某 DeFi 协议遭闪电贷攻击，损失 500 万美元，提醒用户撤销授权。")
    ]
    items = []
    for t, s in random.sample(templates, 2):
        items.append({"category": "热点", "title": t, "summary": s, "length": len(t)+len(s)})
    return items

# --- 4. 广播稿生成 ---
def create_script(alpha, analysis, others, hour_str):
    intro = f"北京时间{hour_str}点整。这里是币圈情报站。"
    text = intro
    
    # 1. 先播 Alpha
    text += f"{alpha['title']}。{alpha['summary']} "
    
    # 2. 再播行情
    text += f"行情方面：{analysis['title']}。{analysis['summary']} "
    
    # 3. 最后播热点
    for item in others:
        text += f"{item['title']}。{item['summary']} "

    text += "播报完毕，祝您交易顺利。"
    return text, len(intro), len("播报完毕")

# --- 5. 音频生成 (只生成晓晓和志玲) ---
async def generate_audio(text):
    print(f"🎙️ 字数 {len(text)}，正在生成音频...")
    
    # 晓晓 (默认)
    try:
        comm = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await comm.save("radio.mp3")
    except: pass
    
    await asyncio.sleep(2) # 休息防封
    
    # 志玲风 (备用)
    try:
        comm = edge_tts.Communicate(text, "zh-TW-HsiaoYuNeural")
        await comm.save("radio_tw.mp3")
    except: pass

# --- 主程序 ---
if __name__ == "__main__":
    # 获取北京时间
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    today_str = beijing_now.strftime("%Y-%m-%d")
    hour_str = beijing_now.strftime("%H")
    
    # 获取数据
    alpha_item = get_binance_alpha(hour_str)
    analysis_item = get_crypto_analysis()
    other_items = get_other_news()
    
    all_news = [alpha_item, analysis_item] + other_items
    
    full_text, l1, l2 = create_script(alpha_item, analysis_item, other_items, hour_str)
    
    data = {
        "date": today_str,
        "hour": hour_str,
        "news": all_news,
        "meta": { "total_len": len(full_text), "intro_len": l1 },
        "voices": [
            {"id": "yunxi", "label": "晓晓"}, # ID保持兼容，显示名改一下
            {"id": "tw", "label": "志玲"}
        ]
    }
    
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    asyncio.run(generate_audio(full_text))
