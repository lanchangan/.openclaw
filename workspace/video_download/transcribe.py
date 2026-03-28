import whisper
import warnings
import os
import time

warnings.filterwarnings('ignore')

audio_path = r'C:\Users\LWS\.openclaw\workspace\video_download\四年级下册《看看我们的地球》导读课-王秀萍.m4a'
output_path = r'C:\Users\LWS\.openclaw\workspace\video_download\transcript.txt'

print('=' * 60)
print('Whisper语音转录')
print('=' * 60)

if not os.path.exists(audio_path):
    print(f'错误: 找不到音频文件')
    exit(1)

file_size = os.path.getsize(audio_path)
print(f'音频: {os.path.basename(audio_path)}')
print(f'大小: {file_size/1024/1024:.1f} MB')
print()

print('[1/3] 加载Whisper模型 (large-v2)...')
start = time.time()
model = whisper.load_model('large-v2')
print(f'完成，耗时: {time.time()-start:.1f}秒')
print()

print('[2/3] 转录中 (约需15-25分钟)...')
start = time.time()
result = model.transcribe(audio_path, language='zh', verbose=True)
elapsed = time.time() - start
print(f'\n转录完成！耗时: {elapsed/60:.1f} 分钟')
print()

print('[3/3] 保存文本...')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(result['text'])

print(f'已保存: {output_path}')
print(f'字符数: {len(result["text"]):,}')
print()
print('=' * 60)
print('完成！')
print('=' * 60)
