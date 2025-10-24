import requests
import json
import sys
import os
API_KEY = os.environ.get('DEEPSEEK_API_KEY')
API_URL = "https://api.deepseek.com/chat/completions"
# 初始对话身份设定（可修改）
messages = [
    {"role": "system", "content": "你是一名专业且耐心的 AI 助手。"}
]

def stream_chat(messages):
    """发送 messages，流式接收模型回复"""
    payload = {
        "model": "deepseek-chat",  
        "stream": True,
        "messages": messages,
    }

    response = requests.post(
        API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json=payload,
        stream=True
    )

    reply = ""  # 用于保存完整回复内容

    for line in response.iter_lines():
        if line:
            text = line.decode("utf-8")

            if text.startswith("data: "):
                data = text[6:]
                if data == "[DONE]":
                    break

                event = json.loads(data)
                delta = event["choices"][0]["delta"]
                if "content" in delta:
                    chunk = delta["content"]
                    reply += chunk
                    print(chunk, end="", flush=True)

    print()  # 换行
    return reply


def chat_loop():
    """可无限对话的 CLI 主循环"""
    print("🎯 Chat CLI 启动（Ctrl+C 退出）\n")

    while True:
        try:
            user_input = input("你：")
        except KeyboardInterrupt:
            print("\n👋 已退出对话")
            sys.exit()

        # 将用户输入加入上下文
        messages.append({"role": "user", "content": user_input})

        print("助手：", end="")

        # 流式回复
        assistant_reply = stream_chat(messages)

        # 将模型回复加入上下文
        messages.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    chat_loop()
