#!/usr/bin/env python3
"""解析字幕文件为纯文本"""
import re
import os
import sys

def parse_srt(content):
    """解析SRT字幕"""
    # 清理BOM
    if content.startswith('\ufeff'):
        content = content[1:]
    
    # 按空行分割条目
    entries = re.split(r'\n\s*\n|\r\n\s*\r\n', content.strip())
    
    subtitles = []
    for entry in entries:
        lines = [l.strip() for l in entry.split('\n') if l.strip()]
        if len(lines) < 2:
            continue
        
        # 找到时间行
        time_line = None
        text_lines = []
        
        for line in lines:
            if '-->' in line:
                time_line = line
            elif time_line is not None:
                text_lines.append(line)
        
        if text_lines:
            # 清理文本中的HTML标签
            text = ' '.join(text_lines)
            text = re.sub(r'<[^>]+>', '', text)
            subtitles.append(text)
    
    return subtitles

def parse_vtt(content):
    """解析VTT字幕"""
    # 移除WEBVTT头
    if 'WEBVTT' in content:
        content = content.split('WEBVTT', 1)[1]
    
    # 清理BOM
    if content.startswith('\ufeff'):
        content = content[1:]
    
    # 移除注释和样式
    content = re.sub(r'NOTE\s+.*?\n\n', '\n', content, flags=re.DOTALL)
    content = re.sub(r'STYLE\s+.*?\n\n', '\n', content, flags=re.DOTALL)
    
    # 按时间块分割
    pattern = r'\n(?=\d{2}:\d{2}:\d{2}\.\d{3})'
    blocks = re.split(pattern, content)
    
    subtitles = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        
        # 分割时间和文本
        lines = block.split('\n')
        if len(lines) < 2:
            continue
        
        # 第一行应该是时间
        if '-->' not in lines[0]:
            continue
        
        # 收集文本行
        text_lines = []
        for i in range(1, len(lines)):
            line = lines[i].strip()
            # 移除序号
            if line.isdigit():
                continue
            # 移除位置设置
            if re.match(r'^\d+:\d+:\d+', line):
                continue
            if line:
                text_lines.append(line)
        
        if text_lines:
            # 清理HTML标签
            text = ' '.join(text_lines)
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            if text:
                subtitles.append(text)
    
    return subtitles

def main():
    """主函数"""
    # 查找字幕文件
    subtitle_files = []
    for f in os.listdir('.'):
        if f.endswith(('.srt', '.vtt')) and 'bilibili' in f:
            subtitle_files.append(f)
    
    if not subtitle_files:
        print("未找到字幕文件")
        sys.exit(1)
    
    print(f"找到 {len(subtitle_files)} 个字幕文件")
    
    # 解析所有字幕
    all_lines = []
    for sub_file in subtitle_files:
        print(f"\n解析: {sub_file}")
        
        try:
            with open(sub_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if sub_file.endswith('.srt'):
                lines = parse_srt(content)
            else:
                lines = parse_vtt(content)
            
            print(f"  提取了 {len(lines)} 行文本")
            all_lines.extend(lines)
            
        except Exception as e:
            print(f"  解析失败: {e}")
    
    if not all_lines:
        print("\n未能提取到任何文本")
        sys.exit(1)
    
    # 去重并保持顺序
    seen = set()
    unique_lines = []
    for line in all_lines:
        # 规范化用于去重
        key = re.sub(r'\s+', '', line)
        if key and key not in seen:
            seen.add(key)
            unique_lines.append(line)
    
    print(f"\n去重后: {len(unique_lines)} 行")
    
    # 保存结果
    output_file = "transcript.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"视频URL: {URL}\n")
        f.write(f"提取时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"总行数: {len(unique_lines)}\n")
        f.write("=" * 60 + "\n\n")
        
        for i, line in enumerate(unique_lines, 1):
            f.write(f"{i}. {line}\n")
    
    print(f"\n结果已保存: {output_file}")
    print(f"总行数: {len(unique_lines)}")

if __name__ == "__main__":
    main()
