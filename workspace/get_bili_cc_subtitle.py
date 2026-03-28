#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取B站CC字幕
"""
import json
import urllib.request
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

bvid = "BV1u61mBhEj7"
print("="*60)
print("获取B站视频字幕")
print("="*60)
print(f"BV号: {bvid}\n")

# 获取视频基本信息
api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.bilibili.com/',
}

print("[1] 获取视频信息...")
req = urllib.request.Request(api_url, headers=headers)
with urllib.request.urlopen(req, timeout=30) as response:
    data = json.loads(response.read().decode('utf-8'))

if data.get('code') != 0:
    print(f"错误: {data.get('message')}")
    exit(1)

video_info = data['data']
cid = video_info.get('cid')
title = video_info.get('title', 'Unknown')
duration = video_info.get('duration', 0)

print(f"  标题: {title}")
print(f"  CID: {cid}")
print(f"  时长: {duration}秒 ({duration//60}分{duration%60}秒)\n")

# 获取播放器信息（包含字幕）
print("[2] 获取字幕信息...")
player_url = f"https://api.bilibili.com/x/player/wbi/v2?cid={cid}&bvid={bvid}"
req2 = urllib.request.Request(player_url, headers=headers)
with urllib.request.urlopen(req2, timeout=30) as response2:
    player_data = json.loads(response2.read().decode('utf-8'))

if player_data.get('code') != 0:
    print(f"错误: {player_data.get('message')}")
    exit(1)

data = player_data.get('data', {})
subtitle_info = data.get('subtitle', {})
subtitles = subtitle_info.get('subtitles', [])

if not subtitles:
    print("  该视频没有字幕文件")
    print("\n尝试使用备用方法获取字幕...")
    # 尝试从视频页面直接获取
    print("  (备用方法需要浏览器环境，当前暂不支持)")
    exit(0)

print(f"  找到 {len(subtitles)} 个字幕文件:\n")

# 下载每个字幕
for idx, sub in enumerate(subtitles, 1):
    sub_url = sub.get('subtitle_url', '')
    sub_lang = sub.get('lan_doc') or sub.get('lan', 'unknown')
    
    print(f"[{idx}] 语言: {sub_lang}")
    print(f"     URL: {sub_url[:60]}...")
    
    if not sub_url:
        print("     跳过 (无URL)")
        continue
    
    try:
        # 下载字幕JSON
        req3 = urllib.request.Request(sub_url, headers=headers)
        with urllib.request.urlopen(req3, timeout=30) as response3:
            sub_data = json.loads(response3.read().decode('utf-8'))
        
        # 处理文件名
        lang_safe = sub_lang.replace(' ', '_').replace('（', '_').replace('）', '_')
        
        # 1. 保存原始JSON
        json_file = f"subtitle_{lang_safe}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(sub_data, f, ensure_ascii=False, indent=2)
        print(f"     已保存: {json_file}")
        
        # 2. 生成逐字稿 (带时间戳)
        transcript_file = f"逐字稿-{lang_safe}-带时间戳.txt"
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("逐字稿（带时间戳）\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n")
            f.write(f"视频链接: https://www.bilibili.com/video/{bvid}/\n")
            f.write(f"字幕语言: {sub_lang}\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("=" * 70 + "\n")
            f.write("正文\n")
            f.write("=" * 70 + "\n\n")
            
            for entry in sub_data.get('body', []):
                from_time = entry.get('from', 0)
                content = entry.get('content', '').strip()
                if content:
                    mins = int(from_time // 60)
                    secs = int(from_time % 60)
                    time_str = f"{mins:02d}:{secs:02d}"
                    f.write(f"[{time_str}] {content}\n")
        
        print(f"     已保存: {transcript_file}")
        
        # 3. 生成纯文本逐字稿 (无时间戳)
        pure_txt_file = f"逐字稿-{lang_safe}.txt"
        with open(pure_txt_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("逐字稿\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n")
            f.write(f"视频链接: https://www.bilibili.com/video/{bvid}/\n")
            f.write(f"字幕语言: {sub_lang}\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("=" * 70 + "\n")
            f.write("正文\n")
            f.write("=" * 70 + "\n\n")
            
            for entry in sub_data.get('body', []):
                content = entry.get('content', '').strip()
                if content:
                    f.write(f"{content}\n")
        
        print(f"     已保存: {pure_txt_file}")
        
        # 4. 生成SRT字幕文件
        srt_file = f"逐字稿-{lang_safe}.srt"
        with open(srt_file, 'w', encoding='utf-8') as f:
            for idx, body in enumerate(sub_data.get('body', []), 1):
                from_time = body.get('from', 0)
                to_time = body.get('to', 0)
                content = body.get('content', '')
                
                def secs_to_srt(secs):
                    hrs = int(secs // 3600)
                    mins = int((secs % 3600) // 60)
                    secs_int = int(secs % 60)
                    millis = int((secs % 1) * 1000)
                    return f"{hrs:02d}:{mins:02d}:{secs_int:02d},{millis:03d}"
                
                f.write(f"{idx}\n")
                f.write(f"{secs_to_srt(from_time)} --> {secs_to_srt(to_time)}\n")
                f.write(f"{content}\n\n")
        
        print(f"     已保存: {srt_file}")
        
    except Exception as e:
        print(f"     错误: {e}")

print("\n" + "="*70)
print("处理完成!")
print("="*70)
