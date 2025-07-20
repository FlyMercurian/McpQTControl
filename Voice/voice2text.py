"""
阿里云语音识别API调用示例
支持音频文件转文字，基于qwen-omni-turbo模型
"""

import os
import base64
from openai import OpenAI

def create_voice_client():
    """创建阿里云语音识别客户端"""
    return OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

def audio_to_text_from_url(audio_url: str, prompt: str = "这段音频在说什么") -> str:
    """
    从音频URL识别语音转文字
    参数：
        audio_url: 音频文件URL
        prompt: 识别提示文字
    返回：识别的文字内容
    """
    client = create_voice_client()
    
    completion = client.chat.completions.create(
        model="qwen-omni-turbo-0119",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": audio_url,
                            "format": "wav",
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            },
        ],
        # 只要文字输出
        modalities=["text"],
        stream=True,
        stream_options={"include_usage": True},
    )

    result_text = ""
    for chunk in completion:
        if chunk.choices:
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                result_text += delta_content
        
    return result_text.strip()

def audio_to_text_from_file(audio_file_path: str, prompt: str = "请将这段音频转换为文字") -> str:
    """
    从本地音频文件识别语音转文字
    参数：
        audio_file_path: 本地音频文件路径
        prompt: 识别提示文字
    返回：识别的文字内容
    """
    # 检查文件是否存在
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_file_path}")
    
    # 读取音频文件并转换为Base64
    try:
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
            
        # 检查文件是否为空
        if len(audio_data) == 0:
            raise ValueError("音频文件为空")
            
        # 转换为Base64，并使用正确的data URI格式
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        data_uri = f"data:audio/wav;base64,{audio_base64}"
        
    except Exception as e:
        raise RuntimeError(f"读取音频文件失败: {str(e)}")
    
    client = create_voice_client()
    
    try:
        completion = client.chat.completions.create(
            model="qwen-omni-turbo-0119",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_audio",
                                                    "input_audio": {
                            "data": data_uri,  # 使用正确的data URI格式
                            "format": "wav",
                        },
                        },
                        {"type": "text", "text": prompt},
                    ],
                },
            ],
            modalities=["text"],
            stream=True,
            stream_options={"include_usage": True},
        )

        result_text = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                result_text += chunk.choices[0].delta.content
            
        result = result_text.strip()
        if not result:
            raise ValueError("语音识别返回空结果")
            
        return result
        
    except Exception as e:
        raise RuntimeError(f"语音识别API调用失败: {str(e)}")

if __name__ == "__main__":
    # 测试示例
    test_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav"
    try:
        result = audio_to_text_from_url(test_url)
        print(f"识别结果: {result}")
    except Exception as e:
        print(f"识别失败: {e}")