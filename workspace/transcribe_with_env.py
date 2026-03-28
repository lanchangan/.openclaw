#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Whisper进行语音识别 - 配置FFmpeg环境
"""
import os
import sys
import json
import subprocess
from datetime import datetime

# 设置UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

# 关键：设置FFmpeg路径
ffmpeg_path = r'C:\Users\LWS\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
os.environ['IMAGEIO_FFMPEG_EXE'] = ffmpeg_path

# 同时添加到PATH
os.environ['PATH'] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ.get('PATH', '')

print("=" * 70)
print("Whisper语音识别")
print("=" * 70)

# 验证FFmpeg
print("\n验证FFmpeg...")
try:
    result = subprocess.run([ffmpeg_path, '-version'], 
                          capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print(f"[OK] FFmpeg就绪")
    else:
        print("[X] FFmpeg运行失败")
        exit(1)
except Exception as e:
    print(f"[X] FFmpeg检查失败: {e}")
    exit(1)

# 查找视频文件
video_dir = "bili_download"
video_files = []

if os.path.exists(video_dir):
    for f in os.listdir(video_dir):
        if f.endswith('.mp4'):
            video_files.append(os.path.join(video_dir, f))

video_files.sort()

if not video_files:
    print(f"\n错误: 未找到视频文件")
    exit(1)

print(f"\n找到 {len(video_files)} 个视频文件:")
for i, vf in enumerate(video_files, 1):
    size_mb = os.path.getsize(vf) / (1024*1024)
    print(f"  [{i}] {os.path.basename(vf)} ({size_mb:.1f} MB)")

# 加载Whisper
print("\n加载Whisper模型 (base)...")
import whisper
model = whisper.load_model("base")
print("[OK] 模型加载完成!\n")

# 处理每个视频
all_results = []

for i, video_path in enumerate(video_files, 1):
    print(f"{'='*70}")
    print(f"处理视频 {i}/{len(video_files)}: {os.path.basename(video_path)}")
    print(f"{'='*70}\n")
    
    try:
        print("开始识别...")
        result = model.transcribe(
            video_path,
            language="zh",
            verbose=True,
            fp16=False
        )
        
        all_results.append(result)
        
        duration = result.get('duration', 0)
        segments = len(result.get('segments', []))
        text_len = len(result.get('text', ''))
        
        print(f"\n[OK] 识别完成!")
        print(f"     时长: {duration:.1f}秒 ({duration/60:.1f}分钟)")
        print(f"     段落: {segments}个")
        print(f"     字数: {text_len}字\n")
        
    except Exception as e:
        print(f"\n[错误] {e}")
        import traceback
        traceback.print_exc()

if not all_results:
    print("错误: 没有识别结果")
    exit(1)

# 生成输出文件
print("\n" + "=" * 70)
print("生成逐字稿文件")
print("=" * 70)

# 1. 带时间戳
timestamp_file = "逐字稿-看看我们的地球导读课-带时间戳.txt"
print(f"\n[1] 生成: {timestamp_file}")

with open(timestamp_file, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("逐字稿（带时间戳）\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n")
    f.write(f"视频链接: https://www.bilibili.com/video/BV1u61mBhEj7/\n")
    f.write(f"识别方式: Whisper AI语音识别\n")
    f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write("=" * 70 + "\n")
    f.write("正文\n")
    f.write("=" * 70 + "\n\n")
    
    for part_idx, result in enumerate(all_results, 1):
        if len(all_results) > 1:
            f.write(f"\n--- 第{part_idx}部分 ---\n\n")
        
        for segment in result.get('segments', []):
            start = segment['start']
            text = segment['text'].strip()
            
            if text:
                mins = int(start // 60)
                secs = int(start % 60)
                time_str = f"{mins:02d}:{secs:02d}"
                f.write(f"[{time_str}] {text}\n")

print(f"  [OK] {timestamp_file} ({os.path.getsize(timestamp_file)/1024:.1f