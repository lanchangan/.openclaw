#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过B站API获取视频字幕
"""
import json
import urllib.request
import urllib.parse
import ssl
import re
import os

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 视频BV号
bvid = "BV1u61mBhEj7"

print(f"正在获取视频 {bvid} 的字幕信息...\n")

# 方法1: 通过B站API获取视频信息和字幕
# 首先获取cid
api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.bilibili.com/',
}

try:
    req = urllib.request.Request(api_url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        if data.get('code') == 0:
            video_info = data['data']
            
            print(f"✓ 视频信息获取成功!")
            print(f"  标题: {video_info.get('title', 'N/A')}")
            print(f"  BV号: {video_info.get('bvid', 'N/A')}")
            print(f"  时长: {video_info.get('duration', 'N/A')} 秒")
            
            # 获取cid
            cid = video_info.get('cid')
            print(f"  CID: {cid}")
            
            # 检查是否有字幕
            subtitle_url = video_info.get('subtitle_url')
            if subtitle_url:
                print(f"\n✓ 找到字幕URL: {subtitle_url}")
            
            # 尝试获取字幕列表
            if cid:
                print(f"\n正在通过API获取字幕列表...")
                subtitle_api = f"https://api.bilibili.com/x/player/wbi/v2?cid={cid}&bvid={bvid}"
                
                req2 = urllib.request.Request(subtitle_api, headers=headers)
                with urllib.request.urlopen(req2, timeout=30) as response2:
                    subtitle_data = json.loads(response2.read().decode('utf-8'))
                    
                    if subtitle_data.get('code') == 0:
                        player_data = subtitle_data.get('data', {})
                        subtitle_info = player_data.get('subtitle', {})
                        
                        if subtitle_info:
                            subtitles = subtitle_info.get('subtitles', [])
                            if subtitles:
                                print(f"\n✓ 找到 {len(subtitles)} 个字幕:")
                                
                                for i, sub in enumerate(subtitles, 1):
                                    sub_url = sub.get('subtitle_url', '')
                                    sub_lang = sub.get('lan_doc', sub.get('lan', 'unknown'))
                                    
                                    print(f"\n  [{i}] 语言: {sub_lang}")
                                    print(f"       URL: {sub_url}")
                                    
                                    if sub_url:
                                        # 下载字幕
                                        print(f"       正在下载...")
                                        try:
                                            req3 = urllib.request.Request(sub_url, headers=headers)
                                            with urllib.request.urlopen(req3, timeout=30) as response3:
                                                sub_json = json.loads(response3.read().decode('utf-8'))
                                                
                                                # 保存JSON
                                                json_filename = f"subtitle_{sub_lang}.json"
                                                with open(json_filename, 'w', encoding='utf-8') as f:
                                                    json.dump(sub_json, f, ensure_ascii=False, indent=2)
                                                print(f"       ✓ JSON已保存: {json_filename}")
                                                
                                                # 生成SRT
                                                srt_filename = f"subtitle_{sub_lang}.srt"
                                                with open(srt_filename, 'w', encoding='utf-8') as f:
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
                                                
                                                print(f"       ✓ SRT已保存: {srt_filename}")
                                                
                                                # 生成纯文本逐字稿
                                                txt_filename = f"subtitle_{sub_lang}.txt"
                                                with open(txt_filename, 'w', encoding='utf-8') as f:
                                                    f.write("=" * 60 + "\n")
                                                    f.write("逐字稿\n")
                                                    f.write("=" * 60 + "\n\n")
                                                    f.write(f"视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n")
                                                    f.write(f"视频链接: https://www.bilibili.com/video/BV1u61mBhEj7/\n")
                                                    f.write(f"字幕语言: {sub_lang}\n\n")
                                                    f.write("=" * 60 + "\n")
                                                    f.write("正文\n")
                                                    f.write("=" * 60 + "\n\n")
                                                    
                                                    for body in sub_json.get('body', []):
                                                        content = body.get('content', '')
                                                        if content:
                                                            f.write(f"{content}\n")
                                                
                                                print(f"       ✓ 逐字稿已保存: {txt_filename}")
                                                
                                                # 生成带时间戳的逐字稿
                                                ts_filename = f"subtitle_{sub_lang}_timestamped.txt"
                                                with open(ts_filename, 'w', encoding='utf-8') as f:
                                                    f.write("=" * 60 + "\n")
                                                    f.write("逐字稿（带时间戳）\n")
                                                    f.write("=" * 60 + "\n\n")
                                                    f.write(f"视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n\n")
                                                    
                                                    for body in sub_json.get('body', []):
                                                        from_time = body.get('from', 0)
                                                        content = body.get('content', '')
                                                        if content:
                                                            mins = int(from_time // 60)
                                                            secs = int(from_time % 60)
                                                            time_str = f"{mins:02d}:{secs:02d}"
                                                            f.write(f"[{time_str}] {content}\n")
                                                
                                                print(f"       ✓ 带时间戳逐字稿已保存: {ts_filename}")
                                                
                                        except Exception as e:
                                            print(f"       ✗ 下载失败: {e}")
                            else:
                                print("\n✗ 未找到字幕文件")
                        else:
                            print("\n✗ 字幕信息为空")
                    else:
                        print(f"\n✗ 字幕API错误: {subtitle_data.get('message', 'Unknown error')}")
        else:
            print(f"\n✗ API错误: {data.get('message', 'Unknown error')}")
            
except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("处理完成!")
print("="*60)
