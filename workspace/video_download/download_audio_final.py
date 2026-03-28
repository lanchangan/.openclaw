import yt_dlp
import os
import sys

# Setup paths
output_dir = r'C:\Users\LWS\.openclaw\workspace\video_download'
os.chdir(output_dir)

# Bilibili video URL
url = 'https://www.bilibili.com/video/BV1u61mBhEj7/'

print(f'=' * 60)
print(f'Downloading audio from: {url}')
print(f'Output directory: {output_dir}')
print(f'=' * 60)

ydl_opts = {
    'format': 'ba',
    'outtmpl': '%(title)s.%(ext)s',
    'quiet': False,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Unknown')
        print(f'\n✓ Download completed!')
        print(f'  Title: {title}')
        
        # List files in directory
        print(f'\nFiles in directory:')
        for f in os.listdir('.'):
            if os.path.isfile(f):
                size = os.path.getsize(f)
                print(f'  - {f} ({size:,} bytes)')
        
except Exception as e:
    print(f'\n✗ Error: {e}', file=sys.stderr)
    sys.exit(1)
