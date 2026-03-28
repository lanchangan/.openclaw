# -*- coding: utf-8 -*-
import os
import subprocess
import sys

# Set UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

video_dir = "bili_download"
output_dir = "transcription_output"
os.makedirs(output_dir, exist_ok=True)

# Find MP4 files
mp4_files = []
for f in os.listdir(video_dir):
    if f.endswith('.mp4'):
        mp4_files.append(os.path.join(video_dir, f))

mp4_files.sort()
print(f"找到 {len(mp4_files)} 个MP4文件")

# Extract audio from each video
audio_files = []

for i, video_path in enumerate(mp4_files):
    print(f"\n处理视频 {i+1}/{len(mp4_files)}: {os.path.basename(video_path)}")
    
    audio_path = os.path.join(output_dir, f"audio_{i:02d}.wav")
    audio_files.append(audio_path)
    
    # Check if ffmpeg exists
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        ffmpeg_exists = result.returncode == 0
    except:
        ffmpeg_exists = False
    
    if ffmpeg_exists:
        # Use ffmpeg
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            '-y',
            audio_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            file_size = os.path.getsize(audio_path) / (1024*1024)
            print(f"  音频提取成功: {file_size:.2f} MB")
        else:
            print(f"  FFmpeg错误: {result.stderr[:200]}")
    else:
        # Try moviepy
        print("  尝试使用moviepy...")
        try:
            from moviepy.editor import VideoFileClip
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, fps=16000, nbytes=2, codec='pcm_s16le')
            video.close()
            file_size = os.path.getsize(audio_path) / (1024*1024)
            print(f"  音频提取成功(moviepy): {file_size:.2f} MB")
        except Exception as e:
            print(f"  提取失败: {e}")

print(f"\n{'='*60}")
print("音频提取完成！")
print(f"{'='*60}")
print(f"\n音频文件列表:")
for af in audio_files:
    if os.path.exists(af):
        size = os.path.getsize(af) / (1024*1024)
        print(f"  {os.path.basename(af)}: {size:.2f} MB")
