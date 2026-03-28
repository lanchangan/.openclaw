#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整流程：从视频提取音频 -> Whisper语音识别 -> 生成逐字稿
"""
import os
import sys
import subprocess
import json
from datetime import datetime

# 设置UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("视频转逐字稿工具")
print("流程: 视频 -> 音频提取 -> Whisper识别 -> 逐字稿")
print("=" * 70)

# 视频目录
video_dir = "bili_download"
output_dir = "transcription_output"
os.makedirs(output_dir, exist_ok=True)

# 查找视频文件
video_files = []
if os.path.exists(video_dir):
    for f in os.listdir(video_dir):
        if f.endswith('.mp4'):
            video_files.append(os.path.join(video_dir, f))

video_files.sort()

if not video_files:
    print(f"\n错误: 在 {video_dir} 目录中未找到MP4视频文件")
    print("请确保视频已下载")
    exit(1)

print(f"\n找到 {len(video_files)} 个视频文件:")
for i, vf in enumerate(video_files, 1):
    size_mb = os.path.getsize(vf) / (1024*1024)
    print(f"  [{i}] {os.path.basename(vf)} ({size_mb:.1f} MB)")

# 检查依赖
print("\n" + "=" * 70)
print("步骤 1: 检查依赖")
print("=" * 70)

# 检查moviepy
try:
    from moviepy.editor import VideoFileClip
    print("[OK] moviepy 已安装")
    moviepy_available = True
except ImportError:
    print("[X] moviepy 未安装，尝试安装...")
    subprocess.run([sys.executable, "-m", "pip", "install", "moviepy", "-q"])
    try:
        from moviepy.editor import VideoFileClip
        print("[OK] moviepy 安装成功")
        moviepy_available = True
    except:
        print("[X] moviepy 安装失败")
        moviepy_available = False

# 检查whisper
try:
    import whisper
    print("[OK] whisper 已安装")
    whisper_available = True
except ImportError:
    print("[X] whisper 未安装，尝试安装...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-U", "openai-whisper", "-q"])
    try:
        import whisper
        print("[OK] whisper 安装成功")
        whisper_available = True
    except:
        print("[X] whisper 安装失败")
        whisper_available = False

if not moviepy_available or not whisper_available:
    print("\n错误: 必要的依赖安装失败")
    exit(1)

# 提取音频
print("\n" + "=" * 70)
print("步骤 2: 从视频提取音频")
print("=" * 70)

audio_files = []

for i, video_path in enumerate(video_files, 1):
    print(f"\n处理视频 {i}/{len(video_files)}: {os.path.basename(video_path)}")
    
    audio_path = os.path.join(output_dir, f"audio_{i:02d}.wav")
    audio_files.append(audio_path)
    
    try:
        print(f"  正在提取音频到: {audio_path}")
        
        # 使用moviepy提取音频
        video = VideoFileClip(video_path)
        audio = video.audio
        
        # 写入WAV文件 (16kHz, 单声道 - Whisper推荐)
        audio.write_audiofile(
            audio_path,
            fps=16000,      # 16kHz采样率
            nbytes=2,       # 16-bit
            codec='pcm_s16le',
            verbose=False,
            logger=None
        )
        
        video.close()
        audio.close()
        
        # 检查文件大小
        file_size_mb = os.path.getsize(audio_path) / (1024*1024)
        print(f"  [OK] 音频提取成功: {file_size_mb:.1f} MB")
        
    except Exception as e:
        print(f"  [错误] 音频提取失败: {e}")
        import traceback
        traceback.print_exc()

if not audio_files or not all(os.path.exists(f) for f in audio_files):
    print("\n错误: 音频提取失败")
    exit(1)

# 使用Whisper进行语音识别
print("\n" + "=" * 70)
print("步骤 3: Whisper语音识别")
print("=" * 70)

print("\n加载Whisper模型 (base - 适合中文)...")
model = whisper.load_model("base")
print("[OK] 模型加载完成\n")

all_results = []

for i, audio_path in enumerate(audio_files, 1):
    print(f"识别音频 {i}/{len(audio_files)}: {os.path.basename(audio_path)}")
    print("-" * 50)
    
    try:
        # 执行语音识别
        result = model.transcribe(
            audio_path,
            language="zh",      # 中文
            verbose=True,       # 显示进度
            fp16=False          # CPU模式
        )
        
        all_results.append(result)
        
        # 显示统计信息
        duration = result.get('duration', 0)
        segments = len(result.get('segments', []))
        text_len = len(result.get('text', ''))
        
        print(f"\n[OK] 识别完成!")
        print(f"     时长: {duration:.1f}秒")
        print(f"     段落: {segments}个")
        print(f"     字数: {text_len}字\n")
        
    except Exception as e:
        print(f"[错误] 识别失败: {e}")
        import traceback
        traceback.print_exc()

# 生成最终逐字稿
print("\n" + "=" * 70)
print("步骤 4: 生成逐字稿文件")
print("=" * 70)

# 1. 生成带时间戳的逐字稿
timestamp_file = "逐字稿-看看我们的地球导读课-带时间戳.txt"
print(f"\n生成: {timestamp_file}")

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

print(f"  [OK] 已保存: {timestamp_file}")

# 2. 生成纯文本逐字稿 (无时间戳)
pure_file = "逐字稿-看看我们的地球导读课.txt"
print(f"\n生成: {pure_file}")

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

print(f"  [OK] 已保存: {pure_file}")

# 3. 生成SRT字幕文件
srt_file = "逐字稿-看看我们的地球导读课.srt"
print(f"\n生成: {srt_file}")

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

print(f"  [OK] 已保存: {srt_file}")

# 完成
print("\n" + "=" * 70)
print("全部完成!")
print("=" * 70)
print("\n生成的文件:")
print(f"  1. {timestamp_file} (带时间戳)")
print(f"  2. {pure_file} (纯文本)")
print(f"  3. {srt_file} (SRT字幕)")
