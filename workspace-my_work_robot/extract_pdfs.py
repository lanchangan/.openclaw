#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提取验证相关 PDF 书籍的内容"""

import os
import sys
import json
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("请安装 pdfplumber: pip install pdfplumber")
    sys.exit(1)

PDF_DIR = r"D:\飞书\验证书籍"
OUTPUT_DIR = r"C:\Users\LWS\.openclaw\workspace-my_work_robot\knowledge\verification\raw"

def extract_pdf(pdf_path, output_dir, max_pages=None):
    """提取 PDF 内容"""
    pdf_name = Path(pdf_path).stem
    output_file = os.path.join(output_dir, f"{pdf_name}.txt")
    
    print(f"\n处理: {pdf_name}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            pages_to_extract = total_pages if max_pages is None else min(total_pages, max_pages)
            
            print(f"  总页数: {total_pages}, 提取: {pages_to_extract}")
            
            # 提取文本
            all_text = []
            all_text.append(f"# {pdf_name}\n\n")
            all_text.append(f"文件: {pdf_path}\n")
            all_text.append(f"总页数: {total_pages}\n\n")
            all_text.append("---\n\n")
            
            for i, page in enumerate(pdf.pages[:pages_to_extract]):
                text = page.extract_text()
                if text:
                    all_text.append(f"\n## 第 {i+1} 页\n\n")
                    all_text.append(text)
                    all_text.append("\n")
                
                # 进度显示
                if (i + 1) % 50 == 0:
                    print(f"  已处理: {i+1}/{pages_to_extract} 页")
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(''.join(all_text))
            
            print(f"  已保存: {output_file}")
            return True
            
    except Exception as e:
        print(f"  错误: {e}")
        return False

def main():
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 获取所有 PDF 文件
    pdf_files = []
    for root, dirs, files in os.walk(PDF_DIR):
        for f in files:
            if f.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, f))
    
    print(f"找到 {len(pdf_files)} 个 PDF 文件")
    
    # 处理每个 PDF
    results = []
    for pdf_path in pdf_files:
        success = extract_pdf(pdf_path, OUTPUT_DIR)
        results.append({
            "file": pdf_path,
            "success": success
        })
    
    # 打印总结
    print("\n" + "="*50)
    print("处理完成!")
    success_count = sum(1 for r in results if r["success"])
    print(f"成功: {success_count}/{len(results)}")

if __name__ == "__main__":
    main()
