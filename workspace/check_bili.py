import os

# 检查下载目录
download_dir = "bili_download"

if not os.path.exists(download_dir):
    print(f"目录不存在: {download_dir}")
else:
    print(f"目录存在: {download_dir}")
    print(f"绝对路径: {os.path.abspath(download_dir)}")
    print()
    
    # 列出所有文件
    for root, dirs, files in os.walk(download_dir):
        level = root.replace(download_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            filepath = os.path.join(root, file)
            size = os.path.getsize(filepath)
            print(f'{subindent}{file} ({size:,} bytes = {size/1024/1024:.2f} MB)')
