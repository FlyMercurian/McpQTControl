import os
from openai import OpenAI
import base64
import numpy as np
import soundfile as sf
import requests

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="sk-20daa801ffcc4b3cad6f3b6353de6ebe",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def encode_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")


base64_audio = encode_audio(r"D:\AIPro\MCPControl\McpQTControl\voice\voice_record_1753007815.wav")

completion = client.chat.completions.create(
    model="qwen-omni-turbo-0119",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": f"data:audio/wav;base64,{base64_audio}",
                        "format": "wav",
                    },
                },
                {"type": "text", "text": "这段音频在说什么"},
            ],
        },
    ],
    # 只要文字输出
    modalities=["text"],
    # stream 必须设置为 True，否则会报错
    stream=True,
    stream_options={"include_usage": True},
)

result_text = ""
for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content:
        result_text += chunk.choices[0].delta.content

print(f"识别结果: {result_text.strip()}")