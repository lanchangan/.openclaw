#!/usr/bin/env python3
"""
Bilibili字幕提取脚本
"""

import urllib.request
import urllib.parse
import json
import re
import os

# BV号
bvid = "BV1u61mBhEj7"

# 第一步：获取视频信息（cid）
api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"

print(f"正在获取视频信息: {bvid}")

try:
    # 创建请求
    req = urllib.request.Request(
        api_url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }
    )
    
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        if data.get('code') == 0:
            video_data = data['data']
            title = video_data['title']
            cid = video_data['cid']
            
            print(f"视频标题: {title}")
            print(f"CID: {cid}")
            
            # 第二步：获取字幕信息
            subtitle_url = f"https://api.bilibili.com/x/player/wbi/v2?cid={cid}&bvid={bvid}"
            
            req2 = urllib.request.Request(
                subtitle_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Referer': 'https://www.bilibili.com/'
                }
            )
            
            with urllib.request.urlopen(req2, timeout=30) as response2:
                subtitle_data = json.loads(response2.read().decode('utf-8'))
                
                if subtitle_data.get('code') == 0:
                    player_data = subtitle_data['data']
                    
                    # 检查字幕信息
                    if 'subtitle' in player_data and 'subtitles' in player_data['subtitle']:
                        subtitles = player_data['subtitle']['subtitles']
                        
                        if subtitles:
                            print(f"\n找到 {len(subtitles)} 个字幕文件:")
                            
                            # 优先选择AI生成的字幕（zh-CN）或普通字幕
                            selected_subtitle = None
                            for sub in subtitles:
                                lang = sub.get('lan', '')
                                print(f"  - {lang}: {sub.get('lan_doc', '未知')}")
                                if lang in ['zh-CN', 'zh', 'chi']:
                                    selected_subtitle = sub
                                    break
                            
                            if not selected_subtitle:
                                selected_subtitle = subtitles[0]
                            
                            # 下载字幕内容
                            subtitle_url = selected_subtitle['subtitle_url']
                            print(f"\n正在下载字幕: {selected_subtitle.get('lan_doc', '未知')}")
                            
                            req3 = urllib.request.Request(
                                subtitle_url,
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                                    'Referer': 'https://www.bilibili.com/'
                                }
                            )
                            
                            with urllib.request.urlopen(req3, timeout=30) as response3:
                                subtitle_content = json.loads(response3.read().decode('utf-8'))
                                
                                # 创建输出目录
                                output_dir = f"bili_temp/{bvid}"
                                os.makedirs(output_dir, exist_ok=True)
                                
                                # 保存原始字幕JSON
                                json_path = f"{output_dir}/{bvid}_subtitle.json"
                                with open(json_path, 'w', encoding='utf-8') as f:
                                    json.dump(subtitle_content, f, ensure_ascii=False, indent=2)
                                
                                # 提取纯文本并保存为逐字稿格式
                                if 'body' in subtitle_content:
                                    text_path = f"{output_dir}/{bvid}_transcript.txt"
                                    with open(text_path, 'w', encoding='utf-8') as f:
                                        f.write(f"视频标题: {title}\n")
                                        f.write(f"BV号: {bvid}\n")
                                        f.write(f"字幕来源: Bilibili AI字幕\n")
                                        f.write("=" * 60 + "\n\n")
                                        
                                        for item in subtitle_content['body']:
                                            start_time = item.get('from', 0)
                                            end_time = item.get('to', 0)
                                            content = item.get('content', '')
                                            
                                            # 格式化时间戳
                                            start_min = int(start_time // 60)
                                            start_sec = int(start_time % 60)
                                            end_min = int(end_time // 60)
                                            end_sec = int(end_time % 60)
                                            
                                            timestamp = f"[{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}]"
                                            f.write(f"{timestamp} {content}\n\n")
                                    
                                    print(f"\n✅ 字幕提取完成！")
                                    print(f"📄 逐字稿文件: {text_path}")
                                    print(f"📊 JSON字幕文件: {json_path}")
                                    
                                    # 输出RESULT_JSON格式
                                    result = {
                                        "success": True,
                                        "bvid": bvid,
                                        "title": title,
                                        "files": {
                                            "transcript": text_path,
                                            "json": json_path
                                        }
                                    }
                                    print(f"\nRESULT_JSON:{json.dumps(result)}")
                                else:
                                    print("❌ 字幕内容格式不正确")
                        else:
                            print("❌ 未找到可用的字幕文件")
                    else:
                        print("❌ 该视频没有字幕信息")
                else:
                    print(f"❌ 获取字幕信息失败: {subtitle_data.get('message', '未知错误')}")
        else:
            print(f"❌ 获取视频信息失败: {data.get('message', '未知错误')}")
            
except urllib.error.HTTPError as e:
    print(f"❌ HTTP错误: {e.code} - {e.reason}")
except Exception as e:
    print(f"❌ 发生错误: {str(e)}")
    import traceback
    traceback.print_exc()
