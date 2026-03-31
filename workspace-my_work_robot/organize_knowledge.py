#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""整理验证知识库"""

import os
import re
from pathlib import Path

RAW_DIR = r"C:\Users\LWS\.openclaw\workspace-my_work_robot\knowledge\verification\raw"
OUTPUT_DIR = r"C:\Users\LWS\.openclaw\workspace-my_work_robot\knowledge\verification"

def read_raw_file(filename_pattern):
    """读取原始文件（处理编码问题）"""
    for f in os.listdir(RAW_DIR):
        if filename_pattern.lower() in f.lower():
            path = os.path.join(RAW_DIR, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                return file.read()
    return None

def extract_toc(content, max_items=50):
    """提取目录结构"""
    toc = []
    lines = content.split('\n')
    for line in lines:
        # 匹配章节标题
        if re.match(r'^(Chapter|CHAPTER|第.*章|\d+\.\s)', line.strip()):
            toc.append(line.strip())
        elif re.match(r'^#{1,3}\s+\d+', line.strip()):
            toc.append(line.strip())
        if len(toc) >= max_items:
            break
    return toc

def extract_sections(content, keywords):
    """提取包含关键词的章节"""
    sections = []
    lines = content.split('\n')
    current_section = []
    in_section = False
    
    for i, line in enumerate(lines):
        # 检查是否进入目标章节
        for kw in keywords:
            if kw.lower() in line.lower() and ('##' in line or 'Chapter' in line or '第' in line):
                in_section = True
                current_section = [line]
                break
        
        if in_section:
            current_section.append(line)
            # 检查是否离开章节（下一个章节开始）
            if i > 0 and ('## 第' in line or '## Chapter' in line or re.match(r'^#\s+\d+', line)):
                if len(current_section) > 10:
                    sections.append('\n'.join(current_section[:-1]))
                current_section = [line]
                in_section = False
    
    return sections

# 创建 SystemVerilog 基础文档
print("创建 SystemVerilog 基础文档...")
sv_content = read_raw_file("SystemVerilog for Verification")
if sv_content:
    # 提取关键章节
    print(f"  - 文件大小: {len(sv_content)} 字符")

# 创建 UVM 框架文档
print("创建 UVM 框架文档...")
uvm_content = read_raw_file("UVM实战")
if uvm_content:
    print(f"  - 文件大小: {len(uvm_content)} 字符")

uvm_guide = read_raw_file("UVM1.1")
if uvm_guide:
    print(f"  - 文件大小: {len(uvm_guide)} 字符")

# 创建 VMM 方法论文档
print("创建 VMM 方法论文档...")
vmm_content = read_raw_file("Verification Methodology")
if vmm_content:
    print(f"  - 文件大小: {len(vmm_content)} 字符")

print("\n原始内容已加载，开始生成知识文档...")
