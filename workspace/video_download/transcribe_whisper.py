import whisper
import warnings
import os
import sys

warnings.filterwarnings('ignore')

# Paths
audio_path = r'C:\Users\LWS\.openclaw\workspace\video_download\四年级下册《看看我们的地球》导读课-王秀萍.m4a'
output_path = r'C:\Users\LWS\.openclaw\workspace\video_download\transcript.txt'

print('=' * 60)
print('Whisper Transcription')
print('=' * 60)
print(f'Audio file: {audio_path}')
print(f'Output file: {output_path}')
print('=' * 60)

# Check if audio file exists
if not os.path.exists(audio_path):
    print(f'Error: Audio file not found: {audio_path}', file=sys.stderr)
    sys.exit(1)

# Load the model
print('\n[1/3] Loading Whisper model (large-v2)...')
try:
    model = whisper.load_model('large-v2')
    print('Model loaded successfully')
except Exception as e:
    print(f'Error loading model: {e}', file=sys.stderr)
    sys.exit(1)

# Transcribe the audio
print('\n[2/3] Transcribing audio (this may take 15-30 minutes)...')
print('    Language: Chinese')
print('    Model: large-v2')
print('    Audio duration: ~37 minutes')
print()

try:
    result = model.transcribe(audio_path, language='zh', verbose=True)
    
    # Save the transcript
    print('\n[3/3] Saving transcript...')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result['text'])
    
    text_length = len(result['text'])
    print(f'Transcript saved to: {output_path}')
    print(f'Text length: {text_length:,} characters')
    print('\nDone!')
    
except Exception as e:
    print(f'Error during transcription: {e}', file=sys.stderr)
    sys.exit(1)
