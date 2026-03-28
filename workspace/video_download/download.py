import yt_dlp
import os

# Change to the correct directory
os.chdir(r'C:\Users\LWS\.openclaw\workspace\video_download')

# B站视频URL
url = 'https://www.bilibili.com/video/BV1u61mBhEj7/'

print(f'Starting download: {url}')

# 下载最佳音频格式
ydl_opts = {
    'format': 'ba',
    'outtmpl': '%(title)s.%(ext)s',
    'quiet': False,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    print(f'\nDownload completed!')
    print(f'Title: {info.get("title")}')
