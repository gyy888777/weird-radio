import json
import random
import datetime
import asyncio
import edge_tts
import os

# --- 1. 模拟抓取奇闻 (为了效果，这次来点不一样的假新闻) ---
def fetch_weird_news():
    sources = ["一位物理学家", "某大爷", "名叫'二狗'的猫", "AI机器人", "神秘富豪"]
    actions = ["声称发现了时间裂缝", "在公园练成了御剑术", "学会了用摩斯密码点外卖", "开始信奉飞天意面神教", "要把地球这颗行星买下来"]
    results = ["结果只是眼花了", "被广场舞大妈围观", "成功点到了五斤小鱼干", "要求给服务器放产假", "因为没摇到号放弃了"]
    
    news_list = []
    for i in range(5): # 更新到 5 条新闻
        title = f"{random.choice(sources)}{random.choice(actions)}，{random.choice(results)}"
        summary = f"据不可靠消息，{title}。这件事发生在{random.randint(1,23)}小时前，引发了网友的激烈讨论。专家表示：这很难评。"
        news_list.append({
            "tag": random.choice(["离谱", "迷惑", "科技", "生物", "人类"]),
            "title": title,
            "summary": summary
        })
    return news_list

# --- 2. 生成广播稿 ---
def create_script(news_list, date_str, hour_str):
    # 开场白加入时间点
    script = f"欢迎收听奇闻电台，现在是北京时间{hour_str}点整。让我们看看过去一小时发生了什么离谱事儿。"
    for idx, item in enumerate(news_list):
        script += f"新闻{idx+1}：{item['title']}。{item['summary']} "
    script += "好的，本时段播报结束，咱们下个整点见！"
    return script

# --- 3. 批量生成多种声音的音频 ---
# 定义我们想要的声音列表
VOICES = [
    {"id": "yunxi", "name": "zh-CN-YunxiNeural"},   # 活泼男声
    {"id": "xiaoxiao", "name": "zh-CN-XiaoxiaoNeural"}, # 温暖女声
    {"id": "liaoning", "name": "zh-CN-LiaoningNeural"}  # 搞笑东北话
]

async def generate_all_audios(text):
    print("开始批量生成音频...")
    tasks = []
    for voice in VOICES:
        filename = f"radio_{voice['id']}.mp3"
        print(f"正在生成: {filename} (使用 {voice['name']})...")
        communicate = edge_tts.Communicate(text, voice["name"])
        tasks.append(communicate.save(filename))
    
    # 并发执行，更快
    await asyncio.gather(*tasks)
    print("所有音频生成完毕！")

# --- 主程序 ---
if __name__ == "__main__":
    # 获取时间和新闻
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))) # 北京时间
    today_str = now.strftime("%Y-%m-%d")
    hour_str = now.strftime("%H")
    
    news = fetch_weird_news()
    
    # 保存数据
    data = {
        "date": today_str,
        "hour": hour_str,
        "news": news,
        # 把可用的声音列表也存进去，给前端用
        "voices": [
            {"id": "yunxi", "label": "云希·讲故事"},
            {"id": "xiaoxiao", "label": "晓晓·治愈系"},
            {"id": "liaoning", "label": "东北老铁·搞笑"}
        ]
    }
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("数据保存完毕：news_data.json")

    # 生成广播稿和音频
    radio_script = create_script(news, today_str, hour_str)
    asyncio.run(generate_all_audios(radio_script))