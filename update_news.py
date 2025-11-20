import json
import random
import datetime
import asyncio
import edge_tts

def fetch_weird_news():
    sources = ["某男子", "某大妈", "一只哈士奇", "程序员", "外星人爱好者"]
    actions = ["试图用意念炒股", "宣称发明了永动火锅", "半夜对着空气吵架", "因为太无聊数完了草莓籽", "把自己打包寄给了前任"]
    results = ["结果股价大跌", "被邻居报警带走", "意外获得了诺贝尔奖", "目前已拥有百万粉丝", "导致快递站瘫痪"]
    
    news_list = []
    for _ in range(3):
        title = f"{random.choice(sources)}{random.choice(actions)}，{random.choice(results)}"
        summary = f"据本台刚刚收到的消息，{title}。目击者表示场面一度非常尴尬，专家建议大家不要模仿。"
        news_list.append({
            "tag": random.choice(["离谱", "迷惑", "人类"]),
            "title": title,
            "summary": summary
        })
    return news_list

def create_script(news_list, date_str):
    script = f"这里是奇闻电台，今天是{date_str}。我是你们的 AI 主播云希。让我们来看看今天发生了什么离谱的事儿。"
    for idx, item in enumerate(news_list):
        script += f"第{idx+1}条新闻：{item['title']}。{item['summary']} "
    script += "以上就是今天的全部内容，咱们明天见！"
    return script

async def generate_audio(text):
    print("正在生成 AI 配音...")
    communicate = edge_tts.Communicate(text, "zh-CN-YunxiNeural")
    await communicate.save("daily_radio.mp3")
    print("音频生成完毕：daily_radio.mp3")

if __name__ == "__main__":
    today = datetime.date.today().strftime("%Y-%m-%d")
    news = fetch_weird_news()
    
    data = { "date": today, "news": news }
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("数据保存完毕：news_data.json")

    radio_script = create_script(news, today)
    asyncio.run(generate_audio(radio_script))
