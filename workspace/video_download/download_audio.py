import yt_dlp
import os

# B站视频URL
url = 'https://www.bilibili.com/video/BV1u61mBhEj7/'

print(f'开始下载音频: {url}')

# 下载最佳音频格式
ydl_opts = {
    'format': 'ba',  # 最佳音频
    'outtmpl': '%(title)s.%(ext)s',
    'quiet': False,
}

# 切换到视频下载目录
os.chdir(r'C:\Users\LWS\.openclaw\workspace\video_download')

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    print(f'\n下载完成: {info.get("title")}')
    print(f'文件名: {info.get("title")}.{info.get("ext", "m4a")}')
