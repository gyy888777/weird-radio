import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 基础新闻抓取 (保持原有) ---
def get_tech_news():
    templates = [
        ("GPT-6发布", "新模型学会了自我编程，效率提升500%，程序员直呼'危'。"),
        ("马斯克火星计划", "SpaceX星舰将不再需要人类驾驶，首批火星船票已售罄。"),
        ("苹果透明手机", "iPhone 18采用全玻璃机身，颜值爆表但维修费高达两万。"),
        ("人造太阳突破", "中国核聚变装置运行时间打破纪录，无限能源时代即将来临。")
    ]
    return generate_items(templates, "科技", ["硬核", "未来", "AI"])

def get_ent_news():
    templates = [
        ("顶流网红塌房", "直播时滤镜失效露出真容，榜一大哥连夜注销账号。"),
        ("霉霉新歌破纪录", "新专辑发布一分钟，全球服务器直接瘫痪。"),
        ("AI拍恐怖片", "Sora生成的电影吓坏观众，影评人却打出满分。")
    ]
    return generate_items(templates, "娱乐", ["吃瓜", "热搜"])

def get_weird_news():
    templates = [
        ("香蕉抢银行", "男子持香蕉抢劫，因太饿把作案工具吃掉，被当场逮捕。"),
        ("躺平寄生虫", "发现一种不呼吸的生物，彻底丢弃耗能基因，被封'打工人之神'。"),
        ("二哈发报机", "狗子半夜敲饭盆，竟是摩斯密码向隔壁金毛求爱。")
    ]
    return generate_items(templates, "奇闻", ["离谱", "沙雕"])

# --- 🆕 新增：区块链与 Alpha ---
def get_crypto_news():
    templates = [
        ("比特币突破新高", "华尔街巨鲸连夜加仓，分析师预测年底将冲击15万美元大关。"),
        ("V神发布以太坊新路线图", "Gas费有望降低99%，Layer2生态迎来史诗级爆发。"),
        ("SOL链上土狗满天飞", "某神秘地址一晚翻了1000倍，引发散户疯狂跟投FOMO情绪。"),
        ("贝莱德CEO喊单", "称加密货币是'数字黄金'，建议每个投资组合都要配置5%。")
    ]
    return generate_items(templates, "币圈", ["行情", "大佬", "暴富"])

def get_binance_alpha(hour):
    # 模拟生成一个未来的领取时间（当前时间 + 30~50分钟）
    claim_minute = random.randint(10, 59)
    claim_time = f"{hour}:{claim_minute}"
    points = random.randint(500, 2000)
    
    return [{
        "category": "Alpha",
        "tag": "必撸",
        "title": "币安Alpha·今日领取提醒",
        "summary": f"注意！今日空投领取时间定于【{claim_time}】。最低积分要求：{points}分。请提前准备好Web3钱包，防身防割。",
        "length": 50 # 估算长度
    }]

def generate_items(templates, category, tags):
    items = []
    # 稍微减少普通新闻数量，给币圈腾位置
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

# --- 2. 极简广播稿 (加入币圈版块) ---
def create_smart_script(all_news, hour_str):
    intro = f"北京时间{hour_str}点整。"
    full_text = intro
    
    # 排序策略：Alpha置顶 -> 币圈 -> 科技 -> 娱乐 -> 奇闻
    # 但我们在列表显示时保持顺序，播报时也按顺序
    
    for item in all_news:
        if item['category'] == 'Alpha':
            # Alpha 消息要加重语气
            segment = f"【特别提醒】{item['title']}。{item['summary']} "
        elif item['category'] == '币圈':
            segment = f"【链上动态】{item['title']}。{item['summary']} "
        else:
            segment = f"【{item['category']}】{item['title']}。{item['summary']} "
            
        full_text += segment
        item['length'] = len(segment)

    outro = "播报结束，祝大家暴富。"
    full_text += outro
    
    return full_text, len(intro), len(outro)

# --- 3. 音频生成 ---
VOICES = [
    {"id": "yunxi", "name": "zh-CN-YunxiNeural"}, # 适合播新闻
    {"id": "xiaoxiao", "name": "zh-CN-XiaoxiaoNeural"},
    {"id": "liaoning", "name": "zh-CN-LiaoningNeural"}
]

async def generate_all_audios(text):
    print(f"📝 字数: {len(text)}")
    for voice in VOICES:
        filename = f"radio_{voice['id']}.mp3"
        print(f"🎙️ 生成 {voice['id']} ...")
        for attempt in range(3):
            try:
                communicate = edge_tts.Communicate(text, voice["name"])
                await communicate.save(filename)
                print(f"   ✅ 成功")
                await asyncio.sleep(10) # 防封锁
                break
            except Exception as e:
                print(f"   ⚠️ 失败: {e}")
                await asyncio.sleep(10)

# --- 主程序 ---
if __name__ == "__main__":
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    today_str = beijing_now.strftime("%Y-%m-%d")
    hour_str = beijing_now.strftime("%H")
    
    # 组合新闻：Alpha放最前，币圈次之
    alpha_news = get_binance_alpha(hour_str)
    crypto_news = get_crypto_news()
    other_news = get_tech_news() + get_ent_news() + get_weird_news()
    
    all_news = alpha_news + crypto_news + other_news
    
    full_text, intro_len, outro_len = create_smart_script(all_news, hour_str)
    
    data = {
        "date": today_str,
        "hour": hour_str,
        "news": all_news,
        "meta": {
            "total_len": len(full_text),
            "intro_len": intro_len,
            "outro_len": outro_len
        },
        "voices": [
            {"id": "yunxi", "label": "云希"},
            {"id": "xiaoxiao", "label": "晓晓"},
            {"id": "liaoning", "label": "东北老铁"}
        ]
    }
    
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    asyncio.run(generate_all_audios(full_text))
