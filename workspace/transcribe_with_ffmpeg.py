#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Whisper进行语音识别 - 使用imageio-ffmpeg
"""
import os
import sys
import json
from datetime import datetime

# 设置UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

# 设置FFmpeg路径
os.environ['IMAGEIO_FFMPEG_EXE'] = r'C:\Users\LWS\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'

print("=" * 70)
print("Whisper语音识别")
print("=" * 70)

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
print("\n[1] 生成带时间戳的逐字稿...")
timestamp_file = "逐字稿-看看我们的地球导读课-带时间戳.txt"

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

print(f"  [OK] {timestamp_file} ({os.path.getsize(timestamp_file)/1024:.1f} KB)")

# 2. 纯文本
print("\n[2] 生成纯文本逐字稿...")
pure_file = "逐字稿-看看我们的地球导读课.txt"

with open(pure_file, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("逐字稿\n")
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
        
        full_text = result.get('text', '').strip()
        f.write(full_text + "\n")

print(f"  [OK] {pure_file} ({os.path.getsize(pure_file)/1024:.1f} KB)")

# 3. SRT字幕
print("\n[3] 生成SRT字幕文件...")
srt_file = "逐字稿-看看我们的地球导读课.srt"

def secs_to_srt(secs):
    hrs = int(secs // 3600)
    mins = int((secs % 3600) // 60)
    secs_int = int(secs % 60)
    millis = int((secs % 1) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs_int:02d},{millis:03d}"

with open(srt_file, 'w', encoding='utf-8') as f:
    idx = 1
    for result in all_results:
        for segment in result.get('segments', []):
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip()
            
            if text:
                f.write(f"{idx}\n")
                f.write(f"{secs_to_srt(start)} --> {secs_to_srt(end)}\n")
                f.write(f"{text}\n\n")
                idx += 1

print(f"  [OK] {srt_file} ({os.path.getsize(srt_file)/1024:.1f} KB)")

# 4. JSON数据
print("\n[4] 生成JSON数据文件...")
json_file = "逐字稿-看看我们的地球导读课.json"

combined_data = {
    "video_info": {
        "title": "四年级下册《看看我们的地球》导读课-王秀萍",
        "bvid": "BV1u61mBhEj7",
        "url": "https://www.bilibili.com/video/BV1u61mBhEj7/",
        "parts": len(all_results)
    },
    "transcription": {
        "engine": "Whisper",
        "model": "base",
        "language": "zh",
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    "results": all_results
}

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=2)

print(f"  [OK] {json_file} ({os.path.getsize(json_file)/1024:.1f} KB)")

# 完成摘要
print("\n" + "=" * 70)
print("全部完成!")
print("=" * 70)

total_duration = sum(r.get('duration', 0) for r in all_results)
total_segments = sum(len(r.get('segments', [])) for r in all_results)
total_chars = sum(len(r.get('text', '')) for r in all_results)

print(f"\n统计信息:")
print(f"  视频总时长: {total_duration:.1f}秒 ({total_duration/60:.1f}分钟)")
print(f"  识别段落数: {total_segments}个")
print(f"  总字数: {total_chars}字")
print(f"  视频分段数: {len(all_results)}段")

print(f"\n生成的文件:")
print(f"  1. {timestamp_file} - 带时间戳的逐字稿")
print(f"  2. {pure_file} - 纯文本逐字稿")
print(f"  3. {srt_file} - SRT字幕文件")
print(f"  4. {json_file} - 完整数据JSON")

print("\n" + "=" * 70)
