# 提取视频音频为MP3
from moviepy.editor import VideoFileClip
import os

# 视频路径
video_path = r"C:\Users\LWS\.openclaw\workspace\bili_download\四年级下册《看看我们的地球》导读课-王秀萍.flv"
audio_path = r"C:\Users\LWS\.openclaw\workspace\bili_download\audio.mp3"

print(f"正在加载视频: {video_path}")
print(f"文件存在: {os.path.exists(video_path)}")
print(f"文件大小: {os.path.getsize(video_path) / (1024*1024):.2f} MB")

# 加载视频
video = VideoFileClip(video_path)
print(f"\n视频时长: {video.duration:.2f} 秒 ({video.duration/60:.2f} 分钟)")
print(f"视频尺寸: {video.size}")
print(f"视频FPS: {video.fps}")

# 提取音频
print(f"\n正在提取音频...")
audio = video.audio
audio.write_audiofile(audio_path, fps=16000, nbytes=2, buffersize=2000, codec='libmp3lame', bitrate='64k')

print(f"\n✓ 音频已保存到: {audio_path}")
print(f"音频大小: {os.path.getsize(audio_path) / (1024*1024):.2f} MB")

# 关闭资源
video.close()
audio.close()
