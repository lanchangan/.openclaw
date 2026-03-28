#!/usr/bin/env python3
"""提取B站视频字幕/音频转录"""
import subprocess
import json
import sys
import os

# 设置yt-dlp路径
YTDLP = r"C:\Users\LWS\AppData\Local\Programs\Python\Python313\Scripts\yt-dlp.exe"
URL = "https://www.bilibili.com/video/BV1u61mBhEj7"

def check_subtitles():
    """检查可用字幕"""
    print("正在检查可用字幕...")
    try:
        result = subprocess.run(
            [YTDLP, "--list-subs", "--dump-json", URL],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # 解析JSON输出
        lines = result.stdout.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and line.startswith('{'):
                try:
                    data = json.loads(line)
                    if 'subtitles' in data:
                        print("找到字幕信息:")
                        print(json.dumps(data['subtitles'], indent=2, ensure_ascii=False))
                        return data.get('subtitles', {})
                except:
                    pass
        
        print("未找到字幕信息，将尝试下载音频进行转录...")
        return None
        
    except Exception as e:
        print(f"检查字幕时出错: {e}")
        return None

def download_audio():
    """下载音频用于转录"""
    output_path = r"C:\Users\LWS\.openclaw\workspace\temp\bilibili_audio"
    
    print("正在下载音频...")
    try:
        result = subprocess.run(
            [
                YTDLP,
                "-x",  # 提取音频
                "--audio-format", "mp3",
                "--audio-quality", "0",
                "-o", f"{output_path}.%(ext)s",
                URL
            ],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            print(f"音频下载成功: {output_path}.mp3")
            return f"{output_path}.mp3"
        else:
            print(f"下载失败: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"下载音频时出错: {e}")
        return None

if __name__ == "__main__":
    # 先检查字幕
    subtitles = check_subtitles()
    
    if not subtitles:
        # 没有字幕，下载音频
        audio_file = download_audio()
        if audio_file:
            print(f"\n音频已下载到: {audio_file}")
            print("请使用Whisper或其他转录工具进行音频转录")
        else:
            print("下载音频失败")
            sys.exit(1)
    else:
        print("\n字幕信息已获取，可以使用yt-dlp下载字幕:")
        print(f"{YTDLP} --write-subs --sub-langs zh-CN {URL}")
