#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提取协议&标准目录下的PDF内容"""

import os
import pdfplumber
from pathlib import Path

PDF_DIR = r"D:\飞书\协议&标准"
OUTPUT_DIR = r"C:\Users\LWS\.openclaw\workspace-my_work_robot\knowledge\protocols_raw"

# 文件分类
WIFI_FILES = ["802.11-be", "802.11ax", "WIFI7"]
VERIFICATION_FILES = ["UVM", "1800", "uvm", "VCS"]
DESIGN_FILES = ["AXI", "AMBA", "I2C"]

def extract_pdf(pdf_path, output_dir, max_pages=None):
    """提取PDF内容"""
    pdf_name = Path(pdf_path).stem
    output_file = os.path.join(output_dir, f"{pdf_name}.txt")
    
    print(f"\n处理: {pdf_name}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            pages_to_extract = total_pages if max_pages is None else min(total_pages, max_pages)
            
            print(f"  总页数: {total_pages}, 提取: {pages_to_extract}")
            
            all_text = []
            all_text.append(f"# {pdf_name}\n\n")
            all_text.append(f"文件: {pdf_path}\n")
            all_text.append(f"总页数: {total_pages}\n\n")
            
            for i, page in enumerate(pdf.pages[:pages_to_extract]):
                text = page.extract_text()
                if text:
                    all_text.append(f"\n## 第 {i+1} 页\n\n")
                    all_text.append(text)
                    all_text.append("\n")
                
                if (i + 1) % 100 == 0:
                    print(f"  已处理: {i+1}/{pages_to_extract} 页")
            
            with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(''.join(all_text))
            
            print(f"  已保存: {output_file}")
            return True, pdf_name, total_pages
            
    except Exception as e:
        print(f"  错误: {e}")
        return False, pdf_name, 0

def classify_file(filename):
    """分类文件"""
    filename_lower = filename.lower()
    
    for keyword in WIFI_FILES:
        if keyword.lower() in filename_lower:
            return "wifi"
    
    for keyword in VERIFICATION_FILES:
        if keyword.lower() in filename_lower:
            return "verification"
    
    for keyword in DESIGN_FILES:
        if keyword.lower() in filename_lower:
            return "design"
    
    return "other"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 获取所有PDF文件
    pdf_files = []
    for f in os.listdir(PDF_DIR):
        if f.lower().endswith('.pdf'):
            pdf_files.append((os.path.join(PDF_DIR, f), f))
    
    print(f"找到 {len(pdf_files)} 个 PDF 文件")
    
    # 分类统计
    categories = {"wifi": [], "verification": [], "design": [], "other": []}
    
    for pdf_path, filename in pdf_files:
        category = classify_file(filename)
        categories[category].append((pdf_path, filename))
    
    print("\n文件分类:")
    for cat, files in categories.items():
        print(f"  {cat}: {len(files)} 个文件")
        for _, f in files:
            print(f"    - {f}")
    
    # 提取所有PDF
    results = []
    for pdf_path, filename in pdf_files:
        success, name, pages = extract_pdf(pdf_path, OUTPUT_DIR)
        category = classify_file(filename)
        results.append({
            "file": filename,
            "category": category,
            "success": success,
            "pages": pages
        })
    
    # 打印总结
    print("\n" + "="*60)
    print("处理完成!")
    success_count = sum(1 for r in results if r["success"])
    total_pages = sum(r["pages"] for r in results)
    print(f"成功: {success_count}/{len(results)}")
    print(f"总页数: {total_pages}")
    
    # 按分类统计
    print("\n按分类统计:")
    for cat in ["wifi", "verification", "design"]:
        cat_results = [r for r in results if r["category"] == cat]
        cat_pages = sum(r["pages"] for r in cat_results)
        print(f"  {cat}: {len(cat_results)} 文件, {cat_pages} 页")

if __name__ == "__main__":
    main()
