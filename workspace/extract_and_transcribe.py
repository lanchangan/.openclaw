#!/usr/bin/env python3
"""
提取视频音频并使用Whisper进行语音识别
"""
import os
import subprocess
import sys

# 视频文件路径
video_dir = "bili_download"
output_dir = "transcription_output"
os.makedirs(output_dir, exist_ok=True)

# 查找MP4文件
mp4_files = []
for f in os.listdir(video_dir):
    if f.endswith('.mp4'):
        mp4_files.append(os.path.join(video_dir, f))

mp4_files.sort()
print(f"找到 {len(mp4_files)} 个MP4文件")
for i, f in enumerate(mp4_files):
    print(f"  [{i+1}] {os.path.basename(f)}")

# 合并音频文件列表
audio_files = []

for i, video_path in enumerate(mp4_files):
    print(f"\n{'='*60}")
    print(f"处理视频 {i+1}/{len(mp4_files)}")
    print(f"{'='*60}")
    
    # 提取音频 - 使用FFmpeg
    audio_path = os.path.join(output_dir, f"audio_{i:02d}.wav")
    audio_files.append(audio_path)
    
    print(f"提取音频到: {audio_path}")
    
    # 使用ffmpeg提取音频
    cmd = [
        'ffmpeg', '-i', video_path,
        '-vn',  # 无视频
        '-acodec', 'pcm_s16le',  # PCM 16-bit
        '-ar', '16000',  # 16kHz采样率 (Whisper推荐)
        '-ac', '1',  # 单声道
        '-y',  # 覆盖已有文件
        audio_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            file_size = os.path.getsize(audio_path) / (1024*1024)
            print(f"✓ 音频提取成功: {file_size:.2f} MB")
        else:
            print(f"✗ FFmpeg错误: {result.stderr}")
            # 尝试使用Python的moviepy
            print("尝试使用moviepy...")
            try:
                from moviepy.editor import VideoFileClip
                video = VideoFileClip(video_path)
                video.audio.write_audiofile(audio_path, fps=16000, nbytes=2, codec='pcm_s16le')
                video.close()
                file_size = os.path.getsize(audio_path) / (1024*1024)
                print(f"✓ 音频提取成功(moviepy): {file_size:.2f} MB")
            except Exception as e:
                print(f"✗ moviepy也失败了: {e}")
    except Exception as e:
        print(f"✗ 错误: {e}")

# 合并音频文件（如果需要）
if len(audio_files) > 1:
    print(f"\n{'='*60}")
    print("合并音频文件...")
    print(f"{'='*60}")
    
    # 创建合并列表文件
    merge_list = os.path.join(output_dir, "merge_list.txt")
    with open(merge_list, 'w') as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")
    
    # 合并音频
    merged_audio = os.path.join(output_dir, "merged_audio.wav")
    cmd = [
        'ffmpeg', '-f', 'concat', '-safe', '0',
        '-i', merge_list, '-y', merged_audio
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        file_size = os.path.getsize(merged_audio) / (1024*1024)
        print(f"✓ 音频合并成功: {file_size:.2f} MB")
        final_audio = merged_audio
    else:
        print(f"✗ 合并失败，将使用第一个音频文件")
        final_audio = audio_files[0]
else:
    final_audio = audio_files[0] if audio_files else None

# 使用Whisper进行语音识别
if final_audio and os.path.exists(final_audio):
    print(f"\n{'='*60}")
    print("开始语音识别 (Whisper)")
    print(f"{'='*60}")
    
    try:
        import whisper
        
        print("加载Whisper模型 (base)...")
        model = whisper.load_model("base")
        
        print(f"识别音频: {final_audio}")
        result = model.transcribe(
            final_audio,
            language="zh",
            verbose=True
        )
        
        # 保存结果
        # 1. 完整文本
        text_file = os.path.join(output_dir, "transcription_full.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("逐字稿 - 完整文本\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n")
            f.write(f"视频链接: https://www.bilibili.com/video/BV1u61mBhEj7/\n")
            f.write(f"识别时间: {os.popen('date /t').read().strip()}\n\n")
            f.write("=" * 60 + "\n")
            f.write("正文\n")
            f.write("=" * 60 + "\n\n")
            f.write(result["text"])
        
        print(f"\n✓ 完整文本已保存: {text_file}")
        
        # 2. 带时间戳的版本
        ts_file = os.path.join(output_dir, "transcription_with_timestamps.txt")
        with open(ts_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("逐字稿 - 带时间戳\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n\n")
            
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                
                # 格式化时间 mm:ss
                start_str = f"{int(start//60):02d}:{int(start%60):02d}"
                end_str = f"{int(end//60):02d}:{int(end%60):02d}"
                
                f.write(f"[{start_str} - {end_str}] {text}\n\n")
        
        print(f"✓ 带时间戳版本已保存: {ts_file}")
        
        # 3. SRT字幕格式
        srt_file = os.path.join(output_dir, "transcription.srt")
        with open(srt_file, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result["segments"], 1):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                
                # SRT时间格式: HH:MM:SS,mmm
                def secs_to_srt(secs):
                    hrs = int(secs // 3600)
                    mins = int((secs % 3600) // 60)
                    secs_int = int(secs % 60)
                    millis = int((secs % 1) * 1000)
                    return f"{hrs:02d}:{mins:02d}:{secs_int:02d},{millis:03d}"
                
                f.write(f"{i}\n")
                f.write(f"{secs_to_srt(start)} --> {secs_to_srt(end)}\n")
                f.write(f"{text}\n\n")
        
        print(f"✓ SRT字幕已保存: {srt_file}")
        
        # 4. JSON格式
        import json
        json_file = os.path.join(output_dir, "transcription.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✓ JSON格式已保存: {json_file}")
        
        print("\n" + "=" * 60)
        print("✅ 全部完成！")
        print("=" * 60)
        print(f"\n📊 统计信息:")
        print(f"   音频时长: {result.get('duration', 'N/A'):.1f} 秒 ({result.get('duration', 0)/60:.1f} 分钟)")
        print(f"   转录文字数: {len(result['text'])} 字符")
        print(f"   段落数: {len(result['segments'])}")
        
        print(f"\n📁 输出文件:")
        print(f"   1. {text_file}")
        print(f"   2. {ts_file}")
        print(f"   3. {srt_file}")
        print(f"   4. {json_file}")
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()

else:
    print("\n✗ 没有找到音频文件")
