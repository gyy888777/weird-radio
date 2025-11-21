import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 新闻抓取 (保持丰富性) ---
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
        ("AI拍恐怖片", "Sora生成的电影吓坏观众，影评人却打出满分。"),
        ("综艺大反转", "恋爱综艺男嘉宾承认自己是数字人，全场嘉宾死机。")
    ]
    return generate_items(templates, "娱乐", ["吃瓜", "热搜", "反转"])

def get_weird_news():
    templates = [
        ("香蕉抢银行", "男子持香蕉抢劫，因太饿把作案工具吃掉，被当场逮捕。"),
        ("躺平寄生虫", "发现一种不呼吸的生物，彻底丢弃耗能基因，被封'打工人之神'。"),
        ("二哈发报机", "狗子半夜敲饭盆，竟是摩斯密码向隔壁金毛求爱。"),
        ("自动洗澡机", "大爷发明滚筒洗澡机，体验者表示像在坐过山车。")
    ]
    return generate_items(templates, "奇闻", ["离谱", "沙雕", "迷惑"])

def generate_items(templates, category, tags):
    items = []
    selected = random.sample(templates, 3)
    for title, detail in selected:
        items.append({
            "category": category,
            "tag": random.choice(tags),
            "title": title,
            "summary": detail,
            "length": len(title) + len(detail) # 用于前端进度计算
        })
    return items

# --- 2. 极简广播稿 (零废话版) ---
def create_smart_script(all_news, hour_str):
    # 开场只有时间
    intro = f"北京时间{hour_str}点整。"
    
    full_text = intro
    
    for item in all_news:
        # 格式：分类 -> 标题 -> 内容 (极简衔接)
        # 比如：【科技】GPT-6发布。新模型...
        segment = f"【{item['category']}】{item['title']}。{item['summary']} "
        full_text += segment
        item['length'] = len(segment) # 更新精确字数

    outro = "播报结束。"
    full_text += outro
    
    return full_text, len(intro), len(outro)

# --- 3. 音频生成 (超强防封锁版) ---
VOICES = [
    {"id": "yunxi", "name": "zh-CN-YunxiNeural"},
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
                # 【关键】休息10秒！确保老铁能出来！
                await asyncio.sleep(10)
                break
            except Exception as e:
                print(f"   ⚠️ 失败 ({attempt+1}): {e}")
                await asyncio.sleep(10)

# --- 主程序 ---
if __name__ == "__main__":
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    today_str = beijing_now.strftime("%Y-%m-%d")
    hour_str = beijing_now.strftime("%H")
    
    all_news = get_tech_news() + get_ent_news() + get_weird_news()
    
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
