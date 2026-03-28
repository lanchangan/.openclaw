#!/usr/bin/env python3
"""
使用Whisper转录音频文件
"""

import whisper
import os
import time
import sys

# 音频文件路径
audio_path = '四年级下册《看看我们的地球》导读课-王秀萍.m4a'

# 检查文件
if not os.path.exists(audio_path):
    print(f'错误: 找不到文件: {audio_path}')
    sys.exit(1)

file_size = os.path.getsize(audio_path) / (1024*1024)
print(f'找到音频文件: {audio_path}')
print(f'文件大小: {file_size:.2f} MB')
print()

# 加载Whisper模型 (使用base模型速度较快，medium更准确)
print('正在加载Whisper模型 (medium - 中文识别效果较好)...')
print('首次使用需要下载模型，请耐心等待...')
model = whisper.load_model('medium')
print('模型加载完成！')
print()

# 开始转录
print('开始转录音频...')
print('正在处理中，这可能需要5-10分钟，请不要关闭...')
print()

start_time = time.time()

result = model.transcribe(
    audio_path,
    language='zh',  # 中文
    verbose=True,   # 显示进度
    task='transcribe'
)

end_time = time.time()
duration = end_time - start_time

print()
print(f'转录完成！耗时: {duration/60:.1f} 分钟')
print(f'识别到 {len(result["segments"])} 个段落')
print()

# 保存结果
output_path = '四年级下册《看看我们的地球》导读课-逐字稿.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('视频标题: 四年级下册《看看我们的地球》导读课\n')
    f.write('讲师: 王秀萍\n')
    f.write(f'转录时间: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
    f.write('=' * 60 + '\n\n')
    f.write('【课堂逐字稿】\n\n')
    
    for segment in result['segments']:
        start = segment['start']
        end = segment['end']
        text = segment['text'].strip()
        
        if text:
            # 格式化时间戳
            start_min = int(start // 60)
            start_sec = int(start % 60)
            end_min = int(end // 60)
            end_sec = int(end % 60)
            
            timestamp = f'[{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}]'
            f.write(f'{timestamp} {text}\n\n')

print(f'逐字稿已保存: {output_path}')

# 显示前3段预览
print()
print('预览 (前3段):')
for i, segment in enumerate(result['segments'][:3]):
    text = segment['text'].strip()
    if text:
        print(f'{i+1}. {text}')
