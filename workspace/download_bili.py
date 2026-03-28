#!/usr/bin/env python3
# 下载B站视频
import subprocess
import sys
import os

# 视频链接
url = "https://www.bilibili.com/video/BV1u61mBhEj7/"
output_dir = "bili_download"

# 确保目录存在
os.makedirs(output_dir, exist_ok=True)

# 使用 yt-dlp 下载
# --cookies-from-browser 可以获取登录状态（如果需要高清）
cmd = [
    sys.executable, "-m", "yt_dlp",
    "--format", "best[ext=mp4]/best",  # 最好质量的MP4
    "--output", f"{output_dir}/%(title)s.%(ext)s",
    "--no-warnings",
    "--progress",
    url
]

print(f"开始下载视频...")
print(f"命令: {' '.join(cmd)}")
print()

result = subprocess.run(cmd, capture_output=False, text=True)

if result.returncode == 0:
    print("\n✅ 下载完成！")
else:
    print(f"\n❌ 下载失败，返回码: {result.returncode}")
    sys.exit(1)
