#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib.request
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

bvid = "BV1u61mBhEj7"
print("Fetching video info...")

# Get video info
api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://www.bilibili.com/',
}

req = urllib.request.Request(api_url, headers=headers)
with urllib.request.urlopen(req, timeout=30) as response:
    data = json.loads(response.read().decode('utf-8'))

if data.get('code') != 0:
    print(f"Error: {data.get('message')}")
    exit(1)

video_info = data['data']
cid = video_info.get('cid')
title = video_info.get('title', 'Unknown')
print(f"Title: {title}")
print(f"CID: {cid}")

# Get subtitle info
subtitle_api = f"https://api.bilibili.com/x/player/wbi/v2?cid={cid}&bvid={bvid}"
req2 = urllib.request.Request(subtitle_api, headers=headers)
with urllib.request.urlopen(req2, timeout=30) as response2:
    subtitle_data = json.loads(response2.read().decode('utf-8'))

if subtitle_data.get('code') != 0:
    print(f"Subtitle API error: {subtitle_data.get('message')}")
    exit(1)

player_data = subtitle_data.get('data', {})
subtitle_info = player_data.get('subtitle', {})
subtitles = subtitle_info.get('subtitles', [])

if not subtitles:
    print("No subtitles found")
    exit(1)

print(f"\nFound {len(subtitles)} subtitle(s)")

# Download each subtitle
for i, sub in enumerate(subtitles, 1):
    sub_url = sub.get('subtitle_url', '')
    sub_lang = sub.get('lan_doc', sub.get('lan', 'unknown'))
    
    print(f"\n[{i}] Language: {sub_lang}")
    
    if not sub_url:
        print("  No URL, skipping")
        continue
    
    print(f"  Downloading...")
    try:
        req3 = urllib.request.Request(sub_url, headers=headers)
        with urllib.request.urlopen(req3, timeout=30) as response3:
            sub_json = json.loads(response3.read().decode('utf-8'))
        
        lang_safe = sub_lang.replace(' ', '_').replace('（', '_').replace('）', '_')
        
        # Save JSON
        json_file = f"subtitle_{lang_safe}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(sub_json, f, ensure_ascii=False, indent=2)
        print(f"  [OK] JSON: {json_file}")
        
        # Generate transcript
        txt_file = f"逐字稿-看看我们的地球导读课.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("逐字稿\n")
            f.write("=" * 60 + "\n\n")
            f.write("视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n")
            f.write("视频链接: https://www.bilibili.com/video/BV1u61mBhEj7/\n")
            f.write("字幕类型: B站自动生成字幕\n\n")
            f.write("=" * 60 + "\n")
            f.write("正文\n")
            f.write("=" * 60 + "\n\n")
            
            for entry in sub_json.get('body', []):
                from_time = entry.get('from', 0)
                content = entry.get('content', '')
                if content:
                    mins = int(from_time // 60)
                    secs = int(from_time % 60)
                    time_str = f"{mins:02d}:{secs:02d}"
                    f.write(f"[{time_str}] {content}\n")
        
        print(f"  [OK] Transcript: {txt_file}")
        
        # Generate timestamped version
        ts_file = f"逐字稿-看看我们的地球导读课-带时间戳.txt"
        with open(ts_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("逐字稿（带时间戳）\n")
            f.write("=" * 60 + "\n\n")
            f.write("视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n\n")
            
            for entry in sub_json.get('body', []):
                from_time = entry.get('from', 0)
                content = entry.get('content', '')
                if content:
                    mins = int(from_time // 60)
                    secs = int(from_time % 60)
                    time_str = f"{mins:02d}:{secs:02d}"
                    f.write(f"[{time_str}] {content}\n")
        
        print(f"  [OK] Timestamped: {ts_file}")
        
        # Generate SRT
        srt_file = f"逐字稿-看看我们的地球导读课.srt"
        with open(srt_file, 'w', encoding='utf-8') as f:
            for j, body in enumerate(sub_json.get('body', []), 1):
                from_time = body.get('from', 0)
                to_time = body.get('to', 0)
                content = body.get('content', '')
                
                def secs_to_srt(secs):
                    hrs = int(secs // 3600)
                    mins = int((secs % 3600) // 60)
                    secs_int = int(secs % 60)
                    millis = int((secs % 1) * 1000)
                    return f"{hrs:02d}:{mins:02d}:{secs_int:02d},{millis:03d}"
                
                f.write(f"{j}\n")
                f.write(f"{secs_to_srt(from_time)} --> {secs_to_srt(to_time)}\n")
                f.write(f"{content}\n\n")
        
        print(f"  [OK] SRT: {srt_file}")
        
    except Exception as e:
        print(f"  [Error] {e}")

print("\n" + "="*60)
print("Done!")
print("="*60)
