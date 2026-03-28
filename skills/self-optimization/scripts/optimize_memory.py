#!/usr/bin/env python3
"""
记忆优化脚本：自动梳理daily memory并更新长期记忆
"""
import os
import json
from datetime import datetime, timedelta

MEMORY_DIR = "~/.openclaw/workspace/memory"
LONG_TERM_MEMORY = "~/.openclaw/workspace/MEMORY.md"

def load_memory_file(path):
    """加载记忆文件内容"""
    try:
        with open(os.path.expanduser(path), 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"加载文件失败 {path}: {e}")
        return ""

def save_memory_file(path, content):
    """保存记忆文件内容"""
    try:
        os.makedirs(os.path.dirname(os.path.expanduser(path)), exist_ok=True)
        with open(os.path.expanduser(path), 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"保存文件成功 {path}")
    except Exception as e:
        print(f"保存文件失败 {path}: {e}")

def get_recent_days(days=7):
    """获取最近N天的日期字符串"""
    dates = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(date)
    return dates

def extract_important_content(content):
    """提取重要内容（简单规则：包含重要关键词的行）"""
    important_keywords = ["决策", "重要", "经验", "教训", "记住", "注意", "TODO", "提醒", "配置", "密码", "密钥", "API"]
    lines = content.split('\n')
    important_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 检查是否包含重要关键词
        if any(keyword in line for keyword in important_keywords):
            important_lines.append(line)
        # 检查是否是标题
        if line.startswith('#') or line.startswith('##') or line.startswith('###'):
            important_lines.append(line)
    
    return '\n'.join(important_lines)

def optimize_memory():
    """执行记忆优化"""
    print("开始记忆优化...")
    
    # 获取最近7天的记忆文件
    recent_dates = get_recent_days(7)
    all_important_content = []
    
    for date in recent_dates:
        file_path = f"{MEMORY_DIR}/{date}.md"
        content = load_memory_file(file_path)
        if content:
            important = extract_important_content(content)
            if important:
                all_important_content.append(f"## {date}\n{important}\n")
    
    # 读取现有长期记忆
    long_term_content = load_memory_file(LONG_TERM_MEMORY)
    
    # 合并新的重要内容
    new_content = long_term_content + "\n\n### 自动更新记忆 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    new_content += "\n".join(all_important_content)
    
    # 保存更新后的长期记忆
    save_memory_file(LONG_TERM_MEMORY, new_content)
    
    # 归档旧的记忆文件
    archive_dir = f"{MEMORY_DIR}/archive"
    os.makedirs(os.path.expanduser(archive_dir), exist_ok=True)
    
    for date in recent_dates:
        src_path = f"{MEMORY_DIR}/{date}.md"
        dest_path = f"{archive_dir}/{date}.md"
        if os.path.exists(os.path.expanduser(src_path)):
            os.rename(os.path.expanduser(src_path), os.path.expanduser(dest_path))
            print(f"归档记忆文件 {date}.md")
    
    print("记忆优化完成！")

if __name__ == "__main__":
    optimize_memory()
