# -*- coding: utf-8 -*-
import os
import json

# List all files in current directory
files = os.listdir('.')
subtitle_files = [f for f in files if 'subtitle_' in f or 'subtitle.' in f]

print(f"Found {len(subtitle_files)} subtitle files:")
for f in subtitle_files:
    size = os.path.getsize(f)
    print(f"  - {f} ({size} bytes)")

# Try to read and display the subtitle content
for sub_file in subtitle_files:
    if sub_file.endswith('.json'):
        print(f"\n{'='*60}")
        print(f"Reading: {sub_file}")
        print('='*60)
        
        try:
            with open(sub_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract subtitle text
            body = data.get('body', [])
            print(f"\nTotal subtitle entries: {len(body)}\n")
            
            # Display first 20 entries
            print("First 20 subtitle entries:")
            print("-" * 60)
            for i, entry in enumerate(body[:20], 1):
                from_time = entry.get('from', 0)
                to_time = entry.get('to', 0)
                content = entry.get('content', '')
                
                mins = int(from_time // 60)
                secs = int(from_time % 60)
                time_str = f"{mins:02d}:{secs:02d}"
                
                print(f"[{time_str}] {content}")
            
            if len(body) > 20:
                print(f"\n... and {len(body) - 20} more entries")
            
            # Save full text to a clean file
            output_filename = "逐字稿-看看我们的地球导读课.txt"
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("逐字稿\n")
                f.write("=" * 60 + "\n\n")
                f.write("视频标题: 四年级下册《看看我们的地球》导读课-王秀萍\n")
                f.write("视频链接: https://www.bilibili.com/video/BV1u61mBhEj7/\n")
                f.write("字幕类型: B站自动生成字幕\n\n")
                f.write("=" * 60 + "\n")
                f.write("正文\n")
                f.write("=" * 60 + "\n\n")
                
                for entry in body:
                    from_time = entry.get('from', 0)
                    content = entry.get('content', '')
                    if content:
                        mins = int(from_time // 60)
                        secs = int(from_time % 60)
                        time_str = f"{mins:02d}:{secs:02d}"
                        f.write(f"[{time_str}] {content}\n")
            
            print(f"\n[OK] Full transcription saved to: {output_filename}")
            
        except Exception as e:
            print(f"Error reading {sub_file}: {e}")
