#!/usr/bin/env python3
"""
B站视频下载和字幕提取工具
"""
import subprocess
import json
import os
import re
import sys

# 配置
YTDLP = r"C:\Users\LWS\AppData\Roaming\Python\Python313\Scripts\yt-dlp.exe"
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"  # 假设ffmpeg安装位置
URL = "https://www.bilibili.com/video/BV1u61mBhEj7"
OUTPUT_DIR = r"C:\Users\LWS\.openclaw\workspace\temp"

def run_cmd(cmd, timeout=120, cwd=None):
    """运行命令"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=timeout,
            cwd=cwd or OUTPUT_DIR,
            shell=True
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def download_video():
    """下载视频"""
    print("正在下载视频...")
    
    output_file = os.path.join(OUTPUT_DIR, "video.mp4")
    
    cmd = f'"{YTDLP}" -f "bestvideo[height<=720]+bestaudio/best[height<=720]" --merge-output-format mp4 -o "{output_file}" "{URL}"'
    
    stdout, stderr, rc = run_cmd(cmd, timeout=300)
    
    if rc == 0 and os.path.exists(output_file):
        print(f"视频下载成功: {output_file}")
        return output_file
    else:
        print(f"视频下载失败")
        print(f"stdout: {stdout[:500]}")
        print(f"stderr: {stderr[:500]}")
        return None

def extract_audio(video_file):
    """从视频提取音频"""
    print("正在提取音频...")
    
    audio_file = os.path.join(OUTPUT_DIR, "audio.wav")
    
    # 使用ffmpeg提取音频
    ffmpeg_path = FFMPEG
    if not os.path.exists(ffmpeg_path):
        # 尝试其他路径
        ffmpeg_path = r"C:\ffmpeg\ffmpeg.exe"
    if not os.path.exists(ffmpeg_path):
        ffmpeg_path = "ffmpeg"  # 尝试系统PATH
    
    cmd = f'"{ffmpeg_path}" -i "{video_file}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_file}" -y'
    
    stdout, stderr, rc = run_cmd(cmd, timeout=120)
    
    if rc == 0 and os.path.exists(audio_file):
        print(f"音频提取成功: {audio_file}")
        return audio_file
    else:
        print(f"音频提取失败")
        print(f"stderr: {stderr[:500]}")
        return None

def main():
    print("=" * 60)
    print("B站视频下载和字幕提取工具")
    print("=" * 60)
    print(f"URL: {URL}")
    print()
    
    # 下载视频
    video_file = download_video()
    
    if not video_file:
        print("\n视频下载失败，尝试直接下载音频...")
        # 尝试直接下载音频
        print("尝试使用yt-dlp直接下载音频...")
        audio_file = os.path.join(OUTPUT_DIR, "audio_direct.wav")
        cmd = f'"{YTDLP}" -x --audio-format wav --audio-quality 0 -o "{audio_file}" "{URL}"'
        stdout, stderr, rc = run_cmd(cmd, timeout=300)
        if rc == 0:
            print("音频下载成功")
        else:
            print("音频下载失败")
            return
    else:
        # 提取音频
        audio_file = extract_audio(video_file)
    
    if audio_file:
        print(f"\n音频文件已准备: {audio_file}")
        print("接下来可以使用Whisper进行转录")
    else:
        print("\n无法获取音频")

if __name__ == "__main__":
    main()
