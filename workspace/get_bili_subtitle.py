#!/usr/bin/env python3
"""
获取B站视频字幕
B站视频URL: https://www.bilibili.com/video/BV1u61mBhEj7/
"""
import re
import json
import urllib.request
import urllib.parse
import ssl

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 视频BV号
bvid = "BV1u61mBhEj7"

# 获取视频页面的HTML
url = f"https://www.bilibili.com/video/{bvid}/"
print(f"正在获取视频页面: {url}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
}

req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        html = response.read().decode('utf-8')
        print(f"✓ 页面获取成功，大小: {len(html):,} 字符")
        
        # 尝试从页面中提取 __INITIAL_STATE__ 或 __playinfo__
        # 方法1: 查找 __INITIAL_STATE__
        initial_state_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.+?});', html)
        
        # 方法2: 查找 __playinfo__
        playinfo_match = re.search(r'window\.__playinfo__\s*=\s*({.+?});', html)
        
        # 方法3: 查找字幕相关的API响应
        subtitle_match = re.search(r'"subtitle"\s*:\s*({[^}]+})', html)
        
        print(f"\n搜索结果:")
        print(f"  __INITIAL_STATE__: {'✓ 找到' if initial_state_match else '✗ 未找到'}")
        print(f"  __playinfo__: {'✓ 找到' if playinfo_match else '✗ 未找到'}")
        print(f"  字幕数据: {'✓ 找到' if subtitle_match else '✗ 未找到'}")
        
        # 尝试解析字幕数据
        if initial_state_match:
            try:
                initial_state = json.loads(initial_state_match.group(1))
                print(f"\n✓ __INITIAL_STATE__ 解析成功")
                
                # 查找字幕信息
                if 'videoData' in initial_state:
                    video_data = initial_state['videoData']
                    print(f"  视频标题: {video_data.get('title', 'N/A')}")
                    print(f"  BV号: {video_data.get('bvid', 'N/A')}")
                    
                    # 检查字幕
                    if 'subtitle' in video_data:
                        subtitle_info = video_data['subtitle']
                        print(f"\n  ✓ 找到字幕信息:")
                        print(f"    字幕列表: {subtitle_info}")
                        
                        # 下载字幕
                        if 'list' in subtitle_info and subtitle_info['list']:
                            for sub in subtitle_info['list']:
                                sub_url = sub.get('subtitle_url') or sub.get('url')
                                sub_lang = sub.get('lan_doc', sub.get('lan', 'unknown'))
                                
                                if sub_url:
                                    print(f"\n  正在下载字幕: {sub_lang}")
                                    print(f"  URL: {sub_url}")
                                    
                                    # 下载字幕文件
                                    sub_req = urllib.request.Request(sub_url, headers=headers)
                                    with urllib.request.urlopen(sub_req, timeout=30) as sub_response:
                                        sub_data = json.loads(sub_response.read().decode('utf-8'))
                                        
                                        # 保存JSON格式
                                        json_filename = f"subtitle_{sub_lang}.json"
                                        with open(json_filename, 'w', encoding='utf-8') as f:
                                            json.dump(sub_data, f, ensure_ascii=False, indent=2)
                                        print(f"  ✓ JSON格式已保存: {json_filename}")
                                        
                                        # 转换为SRT格式
                                        srt_filename = f"subtitle_{sub_lang}.srt"
                                        with open(srt_filename, 'w', encoding='utf-8') as f:
                                            for i, body in enumerate(sub_data.get('body', []), 1):
                                                from_time = body.get('from', 0)
                                                to_time = body.get('to', 0)
                                                content = body.get('content', '')
                                                
                                                # 转换为SRT时间格式 HH:MM:SS,mmm
                                                def secs_to_srt(secs):
                                                    hrs = int(secs // 3600)
                                                    mins = int((secs % 3600) // 60)
                                                    secs_int = int(secs % 60)
                                                    millis = int((secs % 1) * 1000)
                                                    return f"{hrs:02d}:{mins:02d}:{secs_int:02d},{millis:03d}"
                                                
                                                f.write(f"{i}\n")
                                                f.write(f"{secs_to_srt(from_time)} --> {secs_to_srt(to_time)}\n")
                                                f.write(f"{content}\n\n")
                                        
                                        print(f"  ✓ SRT格式已保存: {srt_filename}")
                                        
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
                                            
                                            for body in sub_data.get('body', []):
                                                content = body.get('content', '')
                                                if content:
                                                    f.write(f"{content}\n")
                                        
                                        print(f"  ✓ 逐字稿已保存: {txt_filename}")
                                        
                                        # 生成带时间戳的逐字稿
                                        ts_filename = f"subtitle_{sub_lang}_timestamped.txt"
                                        with open(ts_filename, 'w', encoding='utf-8') as f:
                                            f.write("=" * 60 + "\n")
                                            f.write("逐字稿（带时间戳）\n")
                                            f.write("=" * 60 + "\n\n")
                                            f.write(f"视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n\n")
                                            
                                            for body in sub_data.get('body', []):
                                                from_time = body.get('from', 0)
                                                content = body.get('content', '')
                                                if content:
                                                    # 格式化时间 mm:ss
                                                    mins = int(from_time // 60)
                                                    secs = int(from_time % 60)
                                                    time_str = f"{mins:02d}:{secs:02d}"
                                                    f.write(f"[{time_str}] {content}\n")
                                        
                                        print(f"  ✓ 带时间戳逐字稿已保存: {ts_filename}")
                        
                        print("\n" + "=" * 60)
                        print("✅ 所有字幕处理完成！")
                        print("=" * 60)
                    
                    else:
                        print("\n  ✗ 该视频没有可用的字幕")
                        print("    可能需要使用语音识别（ASR）来生成逐字稿")
                        
            except json.JSONDecodeError as e:
                print(f"\n✗ JSON解析失败: {e}")
                print("  尝试提取原始文本...")
                
except urllib.error.HTTPError as e:
    print(f"\n✗ HTTP错误: {e.code} - {e.reason}")
except urllib.error.URLError as e:
    print(f"\n✗ URL错误: {e.reason}")
except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback
    traceback.print_exc()
