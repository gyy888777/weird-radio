import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 模拟新闻抓取 (保持不变) ---
def get_tech_news():
    templates = [
        ("GPT-6震惊硅谷", "新模型甚至学会了帮程序员写周报，效率提升500%，引发职场焦虑。"),
        ("马斯克火星计划", "SpaceX星舰将由AI全自动驾驶，不再需要人类宇航员操作。"),
        ("苹果发布透明iPhone", "整机采用全玻璃机身，虽然易碎但颜值爆表，黄牛价已炒至3万元。"),
        ("核聚变电站并网", "人类终于实现了无限清洁能源，电费有望降至1分钱一度。")
    ]
    return generate_items(templates, "科技", ["AI", "硬件", "航天", "能源"])

def get_ent_news():
    templates = [
        ("顶流明星直播塌房", "因不小心关闭美颜滤镜，真实颜值曝光，百万粉丝连夜脱粉。"),
        ("泰勒新歌打破纪录", "新专辑发布仅1分钟，全球流媒体服务器全部瘫痪。"),
        ("知名导演用Sora拍电影", "好莱坞抗议升级，称AI正在抢走所有演员的饭碗。"),
        ("综艺推出'AI狼人杀'", "10个AI互相欺诈，结局反转让人类观众惊掉下巴。")
    ]
    return generate_items(templates, "娱乐", ["吃瓜", "影视", "音乐", "网红"])

def get_weird_news():
    templates = [
        ("男子用香蕉抢银行", "结果被柜员当场吃掉香蕉。场面一度尴尬，男子随后被送医鉴定。"),
        ("发现'躺平'寄生虫", "这种生物彻底丢弃了呼吸基因，连氧气都不吸了，被誉为'打工人之神'。"),
        ("二哈学会摩斯密码", "这只狗每天敲饭盆，竟然是在向隔壁金毛发送求爱信号。"),
        ("大爷发明自动洗澡机", "虽然洗得干净，但大爷表示有点晕，像进了滚筒洗衣机。")
    ]
    return generate_items(templates, "奇闻", ["离谱", "沙雕", "生物", "迷惑"])

def generate_items(templates, category, tags):
    items = []
    selected = random.sample(templates, 3)
    for title, detail in selected:
        items.append({
            "category": category,
            "tag": random.choice(tags),
            "title": title,
            "summary": detail
        })
    return items

# --- 2. 极简广播稿 (去废话版) ---
def create_smart_script(all_news, hour_str):
    # 直接报时，不废话
    script = f"北京时间{hour_str}点整。全网资讯通为您播报。"
    
    for item in all_news:
        # 这种格式听起来最像新闻联播/电台
        script += f"【{item['category']}消息】{item['title']}。{item['summary']} "

    script += "播报结束，下个整点见。"
    return script

# --- 3. 音频生成 (增强版) ---
VOICES = [
    {"id": "yunxi", "name": "zh-CN-YunxiNeural"},
    {"id": "xiaoxiao", "name": "zh-CN-XiaoxiaoNeural"},
    {"id": "liaoning", "name": "zh-CN-LiaoningNeural"}
]

async def generate_all_audios(text):
    print(f"正在生成广播稿，字数：{len(text)}...")
    
    for voice in VOICES:
        filename = f"radio_{voice['id']}.mp3"
        print(f"正在生成: {filename}...")
        
        # 重试机制，确保老铁的声音能出来
        for attempt in range(3):
            try:
                communicate = edge_tts.Communicate(text, voice["name"])
                await communicate.save(filename)
                print(f"✅ {filename} 成功！")
                await asyncio.sleep(1) 
                break # 成功了就跳出重试循环
            except Exception as e:
                print(f"⚠️ 失败 (尝试 {attempt+1}/3): {e}")
                await asyncio.sleep(3) # 失败了多歇一会

    print("所有任务完成。")

# --- 主程序 ---
if __name__ == "__main__":
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    today_str = beijing_now.strftime("%Y-%m-%d")
    hour_str = beijing_now.strftime("%H")
    
    all_news = get_tech_news() + get_ent_news() + get_weird_news()
    
    data = {
        "date": today_str,
        "hour": hour_str,
        "news": all_news,
        "voices": [
            {"id": "yunxi", "label": "云希·新闻"},
            {"id": "xiaoxiao", "label": "晓晓·治愈"},
            {"id": "liaoning", "label": "老铁·搞笑"}
        ]
    }
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    full_script = create_smart_script(all_news, hour_str)
    asyncio.run(generate_all_audios(full_script))
