import whisper
import warnings
import os
import time

warnings.filterwarnings('ignore')

audio_path = r'C:\Users\LWS\.openclaw\workspace\video_download\四年级下册《看看我们的地球》导读课-王秀萍.m4a'
output_path = r'C:\Users\LWS\.openclaw\workspace\video_download\transcript.txt'

print('=' * 60)
print('开始转录')
print('=' * 60)
print(f'音频文件: {audio_path}')
print(f'输出文件: {output_path}')

# Load model
print('\n[1/3] 加载Whisper模型 (large-v2)...')
model = whisper.load_model('large-v2')
print('模型加载完成')

# Transcribe
print('\n[2/3] 开始转录音频 (约37分钟，需要15-30分钟)...')
start = time.time()
result = model.transcribe(audio_path, language='zh', verbose=True)
elapsed = time.time() - start
print(f'\n转录完成，耗时: {elapsed/60:.1f} 分钟')

# Save
print('\n[3/3] 保存转录文本...')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(result['text'])

print(f'文本已保存: {output_path}')
print(f'文本长度: {len(result["text"]):,} 字符')
print('=' * 60)
print('转录完成！')
print('=' * 60)
