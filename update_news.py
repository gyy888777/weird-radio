import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 模拟多领域新闻抓取 ---
# 实际项目中，这里应该替换为去 36Kr(科技), 微博(娱乐), 贴吧(奇闻) 的爬虫

def get_tech_news():
    templates = [
        ("OpenAI发布GPT-6", "新模型甚至学会了帮程序员写周报，效率提升500%。"),
        ("马斯克宣布移民火星计划提前", "SpaceX星舰由AI自动驾驶，不再需要人类宇航员操作。"),
        ("苹果发布透明iPhone", "整机采用全玻璃机身，虽然易碎但颜值爆表，售价高达3万元。"),
        ("全球首个核聚变电站并网", "人类终于实现了无限清洁能源，电费有望降至1分钱一度。")
    ]
    return generate_items(templates, "科技", ["AI", "硬件", "航天", "能源"])

def get_ent_news():
    templates = [
        ("某顶流明星塌房", "因在直播中不小心关闭美颜，导致粉丝大量脱粉。"),
        ("泰勒斯威夫特新歌打破纪录", "新专辑发布仅1分钟，全球流媒体服务器全部瘫痪。"),
        ("知名导演宣布用Sora拍电影", "好莱坞罢工抗议升级，称AI正在抢走所有演员的饭碗。"),
        ("国内综艺推出'AI狼人杀'", "让10个AI在一起互相欺诈，结局反转让人类观众惊掉下巴。")
    ]
    return generate_items(templates, "娱乐", ["吃瓜", "影视", "音乐", "网红"])

def get_weird_news():
    templates = [
        ("男子试图用香蕉抢劫银行", "结果被柜员当场吃掉香蕉，场面一度十分尴尬。"),
        ("科学家发现不呼吸的寄生虫", "这种生物彻底躺平，连氧气都不吸了，被誉为'打工人之神'。"),
        ("二哈学会了摩斯密码", "这只狗每天敲击饭盆，竟然是在向隔壁金毛发送求爱信号。"),
        ("大爷发明自动洗澡机", "虽然洗得很干净，但大爷表示有点晕，像进了滚筒洗衣机。")
    ]
    return generate_items(templates, "奇闻", ["离谱", "沙雕", "生物", "迷惑"])

def generate_items(templates, category, tags):
    items = []
    # 随机选 3 条
    selected = random.sample(templates, 3)
    for title, detail in selected:
        items.append({
            "category": category, # 新增分类字段
            "tag": random.choice(tags),
            "title": title,
            "summary": detail # 这里只存详情，不重复标题
        })
    return items

# --- 2. 生成“不啰嗦”的广播稿 ---
def create_smart_script(all_news, date_str, hour_str):
    # 开场白
    script = f"各位听众好，现在是北京时间{hour_str}点整。欢迎收听《全网资讯通》。我是AI主播。"
    
    # --- 科技板块 ---
    script += "首先关注【科技前沿】。"
    for item in [n for n in all_news if n['category'] == '科技']:
        # 话术优化：标题 + 详情
        script += f"{item['title']}。据悉，{item['summary']} "
    
    # --- 娱乐板块 ---
    script += "接下来是【娱乐吃瓜】时间。"
    for item in [n for n in all_news if n['category'] == '娱乐']:
        script += f"关于{item['title']}的消息。{item['summary']} "

    # --- 奇闻板块 ---
    script += "最后来点【天下奇闻】轻松一下。"
    for item in [n for n in all_news if n['category'] == '奇闻']:
        script += f"你敢信吗？{item['title']}！具体情况是这样的：{item['summary']} "

    script += "以上就是本时段的全部内容，感谢收听，我们下个整点见！"
    return script

# --- 3. 批量生成音频 ---
VOICES = [
    {"id": "yunxi", "name": "zh-CN-YunxiNeural"},   # 男声
    {"id": "xiaoxiao", "name": "zh-CN-XiaoxiaoNeural"}, # 女声
    {"id": "liaoning", "name": "zh-CN-LiaoningNeural"}  # 东北
]

async def generate_all_audios(text):
    print("开始生成音频...")
    tasks = []
    for voice in VOICES:
        filename = f"radio_{voice['id']}.mp3"
        print(f"生成: {filename}...")
        communicate = edge_tts.Communicate(text, voice["name"])
        tasks.append(communicate.save(filename))
    
    await asyncio.gather(*tasks)
    print("音频生成完毕！")

# --- 主程序 ---
if __name__ == "__main__":
    # 1. 修正时区时间
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    today_str = beijing_now.strftime("%Y-%m-%d")
    hour_str = beijing_now.strftime("%H")
    
    # 2. 聚合所有新闻 (3科技 + 3娱乐 + 3奇闻 = 9条)
    all_news = get_tech_news() + get_ent_news() + get_weird_news()
    
    # 3. 保存数据
    data = {
        "date": today_str,
        "hour": hour_str,
        "news": all_news,
        "voices": [
            {"id": "yunxi", "label": "云希·新闻腔"},
            {"id": "xiaoxiao", "label": "晓晓·温柔"},
            {"id": "liaoning", "label": "老铁·唠嗑"}
        ]
    }
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 4. 生成音频
    full_script = create_smart_script(all_news, today_str, hour_str)
    asyncio.run(generate_all_audios(full_script))
