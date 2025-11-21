import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 新闻抓取 (内容保持不变) ---
def get_tech_news():
    templates = [
        ("GPT-6发布", "新模型甚至学会了帮程序员写周报，效率提升500%，引发职场焦虑。"),
        ("马斯克火星计划", "SpaceX星舰将由AI全自动驾驶，不再需要人类宇航员操作。"),
        ("苹果发布透明iPhone", "整机采用全玻璃机身，虽然易碎但颜值爆表，黄牛价已炒至3万元。"),
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
            "length": len(title) + len(detail)
        })
    return items

# --- 2. 极简广播稿 (零废话) ---
def create_smart_script(all_news, hour_str):
    # 开场只有时间
    intro = f"北京时间{hour_str}点整。"
    full_text = intro
    
    for item in all_news:
        # 极简衔接
        segment = f"{item['title']}。{item['summary']} "
        full_text += segment
        item['length'] = len(segment)

    outro = "播报结束。"
    full_text += outro
    
    return full_text, len(intro), len(outro)

# --- 3. 音频生成 (单人极速版) ---
async def generate_audio(text):
    print(f"📝 字数: {len(text)}")
    filename = "radio_xiaoxiao.mp3" # 固定文件名
    voice = "zh-CN-XiaoxiaoNeural"  # 只用晓晓
    
    print(f"🎙️ 正在生成晓晓的声音...")
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)
        print(f"✅ {filename} 生成成功！")
    except Exception as e:
        print(f"❌ 失败: {e}")

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
        }
    }
    
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    asyncio.run(generate_audio(full_text))
