import whisper
import warnings
import os
import sys
import time

warnings.filterwarnings('ignore')

# Paths
audio_path = r'C:\Users\LWS\.openclaw\workspace\video_download\四年级下册《看看我们的地球》导读课-王秀萍.m4a'
output_path = r'C:\Users\LWS\.openclaw\workspace\video_download\transcript.txt'
log_path = r'C:\Users\LWS\.openclaw\workspace\video_download\transcribe.log'

def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f'[{timestamp}] {msg}'
    print(log_msg)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

log('=' * 60)
log('Whisper Transcription Started')
log('=' * 60)
log(f'Audio file: {audio_path}')
log(f'Output file: {output_path}')

# Check if audio file exists
if not os.path.exists(audio_path):
    log(f'ERROR: Audio file not found: {audio_path}')
    sys.exit(1)

file_size = os.path.getsize(audio_path)
log(f'Audio file size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)')

# Load the model
log('[1/3] Loading Whisper model (large-v2)...')
try:
    model = whisper.load_model('large-v2')
    log('Model loaded successfully')
except Exception as e:
    log(f'ERROR loading model: {e}')
    sys.exit(1)

# Transcribe the audio
log('[2/3] Transcribing audio (this will take 15-30 minutes)...')
log('Language: Chinese (zh)')
log('Model: large-v2')
log('Audio duration: ~37 minutes')

try:
    start_time = time.time()
    result = model.transcribe(audio_path, language='zh', verbose=True)
    elapsed = time.time() - start_time
    
    log(f'Transcription completed in {elapsed/60:.1f} minutes')
    
    # Save the transcript
    log('[3/3] Saving transcript...')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result['text'])
    
    text_length = len(result['text'])
    log(f'Transcript saved to: {output_path}')
    log(f'Text length: {text_length:,} characters')
    log('=' * 60)
    log('TRANSCRIPTION COMPLETE')
    log('=' * 60)
    
except Exception as e:
    log(f'ERROR during transcription: {e}')
    import traceback
    log(traceback.format_exc())
    sys.exit(1)
