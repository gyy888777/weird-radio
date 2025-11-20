import json
import random
import datetime
import asyncio
import edge_tts

# --- 1. 模拟多领域新闻抓取 (内容不变) ---
def get_tech_news():
    templates = [
        ("OpenAI发布GPT-6", "据称新模型甚至学会了帮程序员写周报，效率提升500%，引发职场焦虑。"),
        ("马斯克宣布移民火星计划提前", "SpaceX星舰将由AI全自动驾驶，不再需要人类宇航员操作，首批志愿者已招募。"),
        ("苹果发布透明iPhone", "整机采用全玻璃机身，虽然被吐槽易碎，但颜值爆表，黄牛价已炒至3万元。"),
        ("全球首个核聚变电站并网", "人类终于实现了无限清洁能源的梦想，专家预测未来电费有望降至1分钱一度。")
    ]
    return generate_items(templates, "科技", ["AI", "硬件", "航天", "能源"])

def get_ent_news():
    templates = [
        ("某顶流明星直播塌房", "因在直播中不小心关闭美颜滤镜，真实颜值曝光，导致数百万粉丝连夜脱粉。"),
        ("泰勒斯威夫特新歌打破吉尼斯纪录", "新专辑发布仅1分钟，全球流媒体服务器全部瘫痪，可见其影响力之大。"),
        ("知名导演宣布用Sora拍电影", "好莱坞编剧和演员公会再次抗议升级，称生成式AI正在抢走所有人的饭碗。"),
        ("国内综艺推出'AI狼人杀'", "让10个AI模型在一起互相欺诈推理，结局反转不断，让人类观众惊掉下巴。")
    ]
    return generate_items(templates, "娱乐", ["吃瓜", "影视", "音乐", "网红"])

def get_weird_news():
    templates = [
        ("男子试图用香蕉抢劫银行", "结果被柜员当场吃掉香蕉，并报了警。场面一度十分尴尬，该男子随后被送医做精神鉴定。"),
        ("科学家发现'躺平'寄生虫", "这种生物彻底丢弃了呼吸相关的基因，连氧气都不吸了，被网友誉为'打工人之神'。"),
        ("二哈学会了摩斯密码", "主人发现这只狗每天有节奏地敲击饭盆，竟然是在向隔壁金毛发送求爱信号。"),
        ("大爷发明自动洗澡机", "虽然洗得很干净，但体验者大爷表示转得有点晕，感觉像进了滚筒洗衣机里。")
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

# --- 2. 生成“不啰嗦”的专业广播稿 (核心升级) ---
def create_smart_script(all_news, date_str, hour_str):
    script = f"各位听众好，现在是北京时间{hour_str}点整。欢迎收听《全网资讯通》。我是您的AI主播。"
    
    # --- 科技板块 ---
    script += "首先进入【科技前沿】板块。"
    for i, item in enumerate([n for n in all_news if n['category'] == '科技']):
        # 话术优化：不再重复标题，而是用连接词引导
        if i == 0: script += f"头条消息：{item['title']}。详细报道称，{item['summary']} "
        else: script += f"另外，{item['title']}。据了解，{item['summary']} "
    
    # --- 娱乐板块 ---
    script += "接下来是【娱乐吃瓜】时间。"
    for i, item in enumerate([n for n in all_news if n['category'] == '娱乐']):
        script += f"关注到{item['title']}。这件事情的背景是，{item['summary']} "

    # --- 奇闻板块 ---
    script += "最后来点【天下奇闻】轻松一下。"
    for i, item in enumerate([n for n in all_news if n['category'] == '奇闻']):
        script += f"你敢信吗？{item['title']}！当时的情况是这样的：{item['summary']} "

    script += "以上就是本时段的全部内容，感谢收听，我们下个整点见！"
    return script

# --- 3. 批量生成音频 (保持防封锁逻辑) ---
VOICES = [
    {"id": "yunxi", "name": "zh-CN-YunxiNeural"},
    {"id": "xiaoxiao", "name": "zh-CN-XiaoxiaoNeural"},
    {"id": "liaoning", "name": "zh-CN-LiaoningNeural"}
]

async def generate_all_audios(text):
    print("开始生成音频...")
    for voice in VOICES:
        filename = f"radio_{voice['id']}.mp3"
        print(f"正在生成: {filename}...")
        try:
            communicate = edge_tts.Communicate(text, voice["name"])
            await communicate.save(filename)
            print(f"✅ {filename} 成功！")
            await asyncio.sleep(2) # 防封锁
        except Exception as e:
            print(f"❌ {filename} 失败: {e}")
    print("所有音频生成完毕！")

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
            {"id": "yunxi", "label": "云希·新闻腔"},
            {"id": "xiaoxiao", "label": "晓晓·温柔"},
            {"id": "liaoning", "label": "老铁·唠嗑"}
        ]
    }
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    full_script = create_smart_script(all_news, today_str, hour_str)
    asyncio.run(generate_all_audios(full_script))
