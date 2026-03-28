#!/usr/bin/env python3
"""
使用Whisper转录音频文件
"""

import whisper
import os
import sys

def transcribe_audio(audio_path, output_path=None, model_size="medium"):
    """
    使用Whisper转录音频
    
    Args:
        audio_path: 音频文件路径
        output_path: 输出文件路径（可选）
        model_size: 模型大小 (tiny, base, small, medium, large)
    """
    print(f"正在加载Whisper模型: {model_size}...")
    model = whisper.load_model(model_size)
    
    print(f"开始转录音频: {audio_path}")
    print("这可能需要几分钟，请耐心等待...")
    
    # 转录音频
    result = model.transcribe(
        audio_path,
        language="zh",  # 指定中文
        verbose=True,
        task="transcribe"
    )
    
    # 如果未指定输出路径，则使用默认路径
    if output_path is None:
        base_name = os.path.splitext(audio_path)[0]
        output_path = f"{base_name}_transcript.txt"
    
    # 保存逐字稿
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"视频标题: 四年级下册《看看我们的地球》导读课\n")
        f.write(f"讲师: 王秀萍\n")
        f.write(f"转录时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write("【课堂逐字稿】\n\n")
        
        # 按段落输出
        for segment in result["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"].strip()
            
            if text:
                # 格式化时间戳
                start_min = int(start_time // 60)
                start_sec = int(start_time % 60)
                end_min = int(end_time // 60)
                end_sec = int(end_time % 60)
                
                timestamp = f"[{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}]"
                f.write(f"{timestamp} {text}\n\n")
    
    print(f"\n✅ 转录完成！")
    print(f"📄 逐字稿已保存: {output_path}")
    print(f"📝 总时长: {result['segments'][-1]['end']:.2f} 秒")
    
    return output_path

if __name__ == "__main__":
    # 音频文件路径
    audio_path = "四年级下册《看看我们的地球》导读课-王秀萍.m4a"
    
    # 检查文件是否存在
    if not os.path.exists(audio_path):
        print(f"错误: 找不到音频文件: {audio_path}")
        print("请确认音频文件路径正确")
        sys.exit(1)
    
    print(f"找到音频文件: {audio_path}")
    print(f"文件大小: {os.path.getsize(audio_path) / (1024*1024):.2f} MB")
    
    # 开始转录
    output_file = transcribe_audio(audio_path, model_size="medium")
    
    print("\n🎉 全部完成！")
