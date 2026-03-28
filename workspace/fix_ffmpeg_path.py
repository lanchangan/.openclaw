#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复FFmpeg路径问题
"""
import os
import sys
import shutil

# FFmpeg在imageio-ffmpeg中的路径
ffmpeg_source = r"C:\Users\LWS\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

# 目标路径（一个肯定在PATH中的地方）
# 使用Python Scripts目录
target_dir = r"C:\Python314\Scripts"
target_path = os.path.join(target_dir, "ffmpeg.exe")

print("=" * 60)
print("修复FFmpeg路径")
print("=" * 60)

# 检查源文件是否存在
if not os.path.exists(ffmpeg_source):
    print(f"[X] 源文件不存在: {ffmpeg_source}")
    sys.exit(1)

print(f"[OK] 找到源文件: {ffmpeg_source}")

# 确保目标目录存在
os.makedirs(target_dir, exist_ok=True)

# 复制文件
print(f"复制到: {target_path}")
shutil.copy2(ffmpeg_source, target_path)

# 验证
if os.path.exists(target_path):
    print(f"[OK] 复制成功!")
    
    # 测试运行
    import subprocess
    try:
        result = subprocess.run([target_path, "-version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"[OK] FFmpeg运行正常: {version_line}")
            
            # 添加到系统PATH
            print("\n添加到系统PATH...")
            current_path = os.environ.get('PATH', '')
            if target_dir not in current_path:
                # 添加到当前会话
                os.environ['PATH'] = target_dir + os.pathsep + current_path
                print(f"[OK] 已添加到当前会话PATH")
                
                # 永久添加（用户级别）
                import winreg
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                        r"Environment", 
                                        0, 
                                        winreg.KEY_READ | winreg.KEY_WRITE)
                    current_user_path, _ = winreg.QueryValueEx(key, "Path")
                    if target_dir not in current_user_path:
                        new_path = target_dir + os.pathsep + current_user_path
                        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                        winreg.CloseKey(key)
                        print(f"[OK] 已永久添加到用户PATH")
                    else:
                        winreg.CloseKey(key)
                        print(f"[OK] 已经在PATH中")
                except Exception as e:
                    print(f"[!] 无法永久添加: {e}")
            else:
                print(f"[OK] 已经在PATH中")
        else:
            print(f"[X] FFmpeg运行失败")
    except Exception as e:
        print(f"[X] 测试运行失败: {e}")
else:
    print(f"[X] 复制失败")

print("\n" + "=" * 60)
print("修复完成!")
print("=" * 60)
print("\n请重新运行语音识别脚本")
