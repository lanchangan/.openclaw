#!/usr/bin/env python3
"""
提取B站视频字幕/转录文本
支持自动字幕下载和解析
"""
import subprocess
import json
import re
import os
import sys

# 配置
YTDLP = r"C:\Users\LWS\AppData\Local\Programs\Python\Python313\Scripts\yt-dlp.exe"
URL = "https://www.bilibili.com/video/BV1u61mBhEj7"
OUTPUT_DIR = r"C:\Users\LWS\.openclaw\workspace\temp"

def run_cmd(cmd, timeout=120):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=timeout,
            cwd=OUTPUT_DIR
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def get_video_info():
    """获取视频信息"""
    print("正在获取视频信息...")
    cmd = [YTDLP, "--dump-json", "--skip-download", URL]
    stdout, stderr, rc = run_cmd(cmd)
    
    if rc != 0:
        print(f"获取视频信息失败: {stderr}")
        return None
    
    try:
        data = json.loads(stdout)
        return {
            'title': data.get('title', 'Unknown'),
            'duration': data.get('duration', 0),
            'uploader': data.get('uploader', 'Unknown'),
            'subtitles': data.get('subtitles', {}),
            'automatic_captions': data.get('automatic_captions', {})
        }
    except Exception as e:
        print(f"解析视频信息失败: {e}")
        return None

def download_subtitles():
    """下载字幕文件"""
    print("\n正在下载字幕...")
    
    # 清理旧文件
    for f in os.listdir(OUTPUT_DIR):
        if f.startswith('bilibili_video') and f.endswith(('.vtt', '.srt', '.json')):
            try:
                os.remove(os.path.join(OUTPUT_DIR, f))
            except:
                pass
    
    # 下载自动字幕
    output_base = os.path.join(OUTPUT_DIR, "bilibili_video")
    cmd = [
        YTDLP,
        "--write-auto-subs",
        "--sub-langs", "zh-CN,zh-TW,zh-Hans,zh-Hant,zh",
        "--convert-subs", "srt",
        "--skip-download",
        "-o", output_base,
        URL
    ]
    
    stdout, stderr, rc = run_cmd(cmd, timeout=180)
    
    # 检查下载的文件
    subtitle_files = []
    for f in os.listdir(OUTPUT_DIR):
        if f.startswith('bilibili_video') and f.endswith(('.vtt', '.srt')):
            subtitle_files.append(os.path.join(OUTPUT_DIR, f))
    
    if subtitle_files:
        print(f"成功下载 {len(subtitle_files)} 个字幕文件:")
        for f in subtitle_files:
            print(f"  - {os.path.basename(f)}")
        return subtitle_files
    else:
        print("未找到字幕文件")
        print(f"stdout: {stdout[:500]}")
        print(f"stderr: {stderr[:500]}")
        return []

def parse_srt(content):
    """解析SRT字幕文件"""
    # 清理BOM
    if content.startswith('\ufeff'):
        content = content[1:]
    
    # 按序号分割
    pattern = r'\n\s*\n|\r\n\s*\r\n'
    entries = re.split(pattern, content.strip())
    
    subtitles = []
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        lines = entry.split('\n')
        if len(lines) < 2:
            continue
        
        # 第一行是序号，跳过
        # 第二行是时间
        time_line = None
        text_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if i == 0 and line.isdigit():
                continue
            if '-->' in line and time_line is None:
                time_line = line
            elif line:
                text_lines.append(line)
        
        if time_line and text_lines:
            # 解析时间
            time_match = re.match(r'(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,.]\d{3})', time_line)
            if time_match:
                start = time_match.group(1).replace(',', '.')
                end = time_match.group(2).replace(',', '.')
                subtitles.append({
                    'start': start,
                    'end': end,
                    'text': ' '.join(text_lines)
                })
    
    return subtitles

def parse_vtt(content):
    """解析VTT字幕文件"""
    # 移除WEBVTT头
    if 'WEBVTT' in content:
        content = content.split('WEBVTT', 1)[1]
    
    # 清理BOM
    if content.startswith('\ufeff'):
        content = content[1:]
    
    lines = content.strip().split('\n')
    subtitles = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 跳过空行和注释
        if not line or line.startswith('NOTE'):
            i += 1
            continue
        
        # 跳过序号
        if line.isdigit():
            i += 1
            continue
        
        # 时间行
        time_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})', line)
        if time_match:
            start = time_match.group(1)
            end = time_match.group(2)
            
            # 收集文本行
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip():
                text_lines.append(lines[i].strip())
                i += 1
            
            if text_lines:
                subtitles.append({
                    'start': start,
                    'end': end,
                    'text': ' '.join(text_lines)
                })
        
        i += 1
    
    return subtitles

def main():
    """主函数"""
    print("=" * 60)
    print("B站视频字幕提取工具")
    print("=" * 60)
    
    # 获取视频信息
    info = get_video_info()
    if info:
        print(f"\n视频标题: {info['title']}")
        print(f"UP主: {info['uploader']}")
        print(f"时长: {info['duration']} 秒")
    
    # 下载字幕
    subtitle_files = download_subtitles()
    
    if not subtitle_files:
        print("\n未找到字幕，尝试下载音频进行转录...")
        sys.exit(1)
    
    # 解析字幕文件
    all_subtitles = []
    for sub_file in subtitle_files:
        print(f"\n正在解析: {os.path.basename(sub_file)}")
        
        try:
            with open(sub_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 根据扩展名选择解析器
            if sub_file.endswith('.srt'):
                subtitles = parse_srt(content)
            elif sub_file.endswith