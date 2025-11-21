import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 新闻抓取 (内容保持丰富) ---
def get_tech_news():
    templates = [
        ("GPT-6 震撼发布", "新模型不再需要提示词，它能直接预判你想写什么代码，程序员惊呼'失业倒计时'。"),
        ("马斯克殖民火星", "SpaceX 星舰成功回收，马斯克宣布首批火星船票售价 10 万美元，还可以分期付款。"),
        ("苹果发布透明手机", "iPhone 18 采用全玻璃机身，虽然只有手掌大小，但维修费高达两万，被网友戏称'传家宝'。"),
        ("可控核聚变突破", "中国“人造太阳”运行时间打破纪录，无限清洁能源时代或许真的要来了。")
    ]
    return generate_items(templates, "科技", ["硬核", "未来", "AI"])

def get_ent_news():
    templates = [
        ("顶流塌房", "某千万粉丝网红直播时滤镜失效，真实颜值吓退榜一大哥，账号连夜注销。"),
        ("泰勒演唱会", "霉霉新歌引发小型地震，地质学家表示，这其实是数万粉丝同时蹦迪导致的共振。"),
        ("AI拍电影", "好莱坞导演用 Sora 生成了一部恐怖片，观众吓得爆米花撒了一地，影评人打出满分。"),
        ("综艺反转", "恋爱综艺大结局，男嘉宾竟然承认自己是 AI 数字人，女嘉宾当场死机。")
    ]
    return generate_items(templates, "娱乐", ["吃瓜", "热搜", "反转"])

def get_weird_news():
    templates = [
        ("香蕉抢银行", "男子手持香蕉闯入银行，结果因太饿把'凶器'吃掉了，随后被保安请去喝茶。"),
        ("躺平寄生虫", "科学家发现一种连呼吸都懒得做的生物，它彻底丢弃了耗能基因，被网友奉为'打工人之神'。"),
        ("二哈发报机", "主人发现狗子半夜敲饭盆，翻译后发现竟然是摩斯密码，内容是'隔壁金毛单身'。"),
        ("自动洗澡机", "大爷发明滚筒式洗澡机，虽然洗得干净，但体验者表示出来后感觉天旋地转。")
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
            # 计算这一条新闻的字数（用于前端同步进度）
            "length": len(title) + len(detail)
        })
    return items

# --- 2. 智能脚本生成 (计算长度) ---
def create_script_and_meta(all_news, hour_str):
    # 开场白 (极简)
    intro = f"北京时间{hour_str}点。全网资讯通，开始播报。"
    outro = "以上是本小时资讯，下个整点见。"
    
    full_text = intro
    
    # 拼接正文
    for item in all_news:
        # 话术：分类 + 标题 + 内容
        segment = f"【{item['category']}】{item['title']}。{item['summary']} "
        full_text += segment
        # 更新该条目的字数，包含引导词
        item['length'] = len(segment)

    full_text += outro
    
    return full_text, len(intro), len(outro)

# --- 3. 音频生成 (防哑火增强版) ---
VOICES = [
    {"id": "yunxi", "name": "zh-CN-YunxiNeural"},
    {"id": "xiaoxiao", "name": "zh-CN-XiaoxiaoNeural"},
    {"id": "liaoning", "name": "zh-CN-LiaoningNeural"}
]

async def generate_all_audios(text):
    print(f"📝 广播稿 ({len(text)}字): {text[:50]}...")
    
    for voice in VOICES:
        filename = f"radio_{voice['id']}.mp3"
        print(f"🎙️ 正在生成: {voice['label']}...")
        
        for attempt in range(3): # 重试3次
            try:
                communicate = edge_tts.Communicate(text, voice["name"])
                await communicate.save(filename)
                print(f"   ✅ {filename} 完成")
                # 关键：休息5秒，防止老铁哑火
                await asyncio.sleep(5)
                break
            except Exception as e:
                print(f"   ⚠️ 失败 ({attempt+1}): {e}")
                await asyncio.sleep(5)

# --- 主程序 ---
if __name__ == "__main__":
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    today_str = beijing_now.strftime("%Y-%m-%d")
    hour_str = beijing_now.strftime("%H")
    
    all_news = get_tech_news() + get_ent_news() + get_weird_news()
    
    full_text, intro_len, outro_len = create_script_and_meta(all_news, hour_str)
    
    data = {
        "date": today_str,
        "hour": hour_str,
        "news": all_news,
        "meta": {
            "total_text_len": len(full_text),
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
