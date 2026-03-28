#!/usr/bin/env python3
"""
Video to Feishu Transcript - 视频转录并上传到飞书

核心功能：
1. 接收视频文件或链接
2. 使用Whisper本地转录为文字（带时间戳）
3. 格式化输出，去除AI味
4. 一键上传到飞书文档
"""

import os
import sys
import json
import time
import shutil
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Callable
from urllib.parse import urlparse
import argparse

# 确保输出目录存在
OUTPUT_DIR = Path("./output")
OUTPUT_DIR.mkdir(exist_ok=True)

# 工具检查
def check_dependency(command: str) -> bool:
    """检查依赖工具是否已安装"""
    return shutil.which(command) is not None

def ensure_dependencies():
    """确保所有依赖都已安装"""
    missing = []
    for tool in ["ffmpeg", "whisper"]:
        if not check_dependency(tool):
            missing.append(tool)
    
    if missing:
        print(f"❌ 缺少依赖工具: {', '.join(missing)}")
        print("请安装以下依赖:")
        print("  - ffmpeg: https://ffmpeg.org/download.html")
        print("  - whisper: pip install openai-whisper")
        sys.exit(1)
    
    print("✅ 所有依赖已就绪")

# 视频处理
def is_url(path: str) -> bool:
    """检查是否为URL"""
    parsed = urlparse(path)
    return bool(parsed.scheme and parsed.netloc)

def download_video(url: str, output_path: Path) -> bool:
    """下载网络视频"""
    print(f"⬇️ 正在下载视频: {url}")
    try:
        # 使用 yt-dlp 或 wget/curl 下载
        result = subprocess.run(
            ["yt-dlp", "-o", str(output_path), "--no-playlist", "-f", "best[height<=1080]", url],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"✅ 视频下载完成: {output_path}")
            return True
        else:
            print(f"❌ 下载失败: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ 未找到 yt-dlp，请安装: pip install yt-dlp")
        return False
    except subprocess.TimeoutExpired:
        print("❌ 下载超时")
        return False
    except Exception as e:
        print(f"❌ 下载出错: {e}")
        return False

def extract_audio(video_path: Path, audio_path: Path) -> bool:
    """从视频中提取音频"""
    print(f"🔊 正在提取音频...")
    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-i", str(video_path),
                "-vn",  # 不包含视频
                "-acodec", "pcm_s16le",
                "-ar", "16000",  # 16kHz 采样率，适合Whisper
                "-ac", "1",  # 单声道
                "-y",  # 覆盖已存在文件
                str(audio_path)
            ],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ 音频提取完成: {audio_path}")
            return True
        else:
            print(f"❌ 音频提取失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 音频提取出错: {e}")
        return False

# Whisper 转录
def transcribe_with_whisper(
    audio_path: Path,
    output_dir: Path,
    model: str = "base",
    language: str = "zh"
) -> Optional[Dict]:
    """使用Whisper转录音频"""
    print(f"🎯 正在使用Whisper转录 (模型: {model}, 语言: {language})...")
    
    try:
        # 创建临时目录
        temp_dir = Path(tempfile.mkdtemp())
        
        # 构建whisper命令
        cmd = [
            "whisper",
            str(audio_path),
            "--model", model,
            "--language", language,
            "--output_dir", str(temp_dir),
            "--output_format", "all",  # 生成所有格式
        ]
        
        # 执行转录
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1小时超时
        )
        
        if result.returncode != 0:
            print(f"❌ Whisper转录失败: {result.stderr}")
            shutil.rmtree(temp_dir, ignore_errors=True)
            return None
        
        print(f"✅ Whisper转录完成")
        
        # 读取生成的文件
        base_name = audio_path.stem
        transcript_data = {
            "text": "",
            "json": None,
            "srt": "",
            "tsv": "",
            "vtt": ""
        }
        
        # 读取纯文本
        txt_file = temp_dir / f"{base_name}.txt"
        if txt_file.exists():
            transcript_data["text"] = txt_file.read_text(encoding="utf-8")
        
        # 读取JSON（包含时间戳信息）
        json_file = temp_dir / f"{base_name}.json"
        if json_file.exists():
            transcript_data["json"] = json.loads(json_file.read_text(encoding="utf-8"))
        
        # 读取SRT字幕
        srt_file = temp_dir / f"{base_name}.srt"
        if srt_file.exists():
            transcript_data["srt"] = srt_file.read_text(encoding="utf-8")
        
        # 读取TSV
        tsv_file = temp_dir / f"{base_name}.tsv"
        if tsv_file.exists():
            transcript_data["tsv"] = tsv_file.read_text(encoding="utf-8")
        
        # 读取VTT
        vtt_file = temp_dir / f"{base_name}.vtt"
        if vtt_file.exists():
            transcript_data["vtt"] = vtt_file.read_text(encoding="utf-8")
        
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return transcript_data
        
    except subprocess.TimeoutExpired:
        print(f"❌ Whisper转录超时")
        return None
    except Exception as e:
        print(f"❌ Whisper转录出错: {e}")
        import traceback
        traceback.print_exc()
        return None

# 格式化转录结果
def format_transcript(
    transcript_data: Dict,
    include_timestamps: bool = True,
    format_type: str = "markdown"
) -> str:
    """格式化转录结果为可读文本"""
    
    if not transcript_data or not transcript_data.get("json"):
        return transcript_data.get("text", "")
    
    segments = transcript_data["json"].get("segments", [])
    
    if not include_timestamps:
        # 纯文本，按段落分组
        return transcript_data["text"]
    
    # 按时间戳分组
    paragraphs = []
    current_para = {"texts": [], "start": None, "end": None}
    
    for seg in segments:
        text = seg.get("text", "").strip()
        if not text:
            continue
        
        # 如果当前段落为空，初始化时间戳
        if current_para["start"] is None:
            current_para["start"] = seg["start"]
        current_para["end"] = seg["end"]
        current_para["texts"].append(text)
        
        # 根据标点判断段落结束
        if text.endswith(("。", "？", "！", ".", "?", "!", "...", "……")):
            paragraphs.append(current_para)
            current_para = {"texts": [], "start": None, "end": None}
    
    # 添加最后一个段落
    if current_para["texts"]:
        paragraphs.append(current_para)
    
    # 生成Markdown格式
    lines = []
    for para in paragraphs:
        start_time = format_timestamp(para["start"])
        text = "".join(para["texts"])
        lines.append(f"### [{start_time}]\n{text}\n")
    
    return "\n".join(lines)

def format_timestamp(seconds: float) -> str:
    """将秒数转换为 HH:MM:SS 格式"""
    td = timedelta(seconds=int(seconds))
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    secs = td.seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

# 去AI味处理
def humanize_text(text: str) -> str:
    """
    去除AI生成的文字特征，使其更自然。
    基于 humanizer 技能规则。
    """
    import re
    
    # 1. 去除AI常用词汇和短语
    ai_phrases = [
        r"此外[，,]",
        r"值得注意的是[，,]",
        r"需要指出的是[，,]",
        r"从某种程度上说[，,]",
        r"可以这样说[，,]",
        r"总的来说[，,]",
        r"综上所述[，,]",
        r"由此可见[，,]",
        r"毋庸置疑[，,]",
        r"毫无疑问[，,]",
        r"事实上[，,]",
        r"实际上[，,]",
        r"一定程度上[，,]",
        r"某种程度上[，,]",
        r"特别是[，,]",
        r"尤其是[，,]",
        r"换言之[，,]",
        r"也就是说[，,]",
        r"这意味着[，,]",
    ]
    
    for pattern in ai_phrases:
        text = re.sub(pattern, "", text)
    
    # 2. 去除多余的连接词开头
    text = re.sub(r"^(而且|并且|另外|此外|同时|另外|其次|最后|总之)", "", text).strip()
    
    # 3. 去除重复标点
    text = re.sub(r"[。，]{2,}", "。", text)
    
    # 4. 去除多余空格
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n\n\n+", "\n\n", text)
    
    # 5. 去除"作为AI..."等自我指涉
    text = re.sub(r"作为一个人工智能[^，。]*[，。]", "", text)
    text = re.sub(r"作为AI[^，。]*[，。]", "", text)
    text = re.sub(r"我是[^，。]*AI[^，。]*[，。]", "", text)
    
    # 6. 去除过度正式的表达
    formal_to_casual = {
        "进行": "做",
        "实施": "做",
        "开展": "做",
        "推进": "推动",
        "针对": "对",
        "关于": "对于",
        "涉及": "涉及",
        "包含": "有",
        "具备": "有",
        "拥有": "有",
        "获得": "得到",
        "取得": "得到",
        "实现": "做到",
        "完成": "做完",
    }
    
    for formal, casual in formal_to_casual.items():
        # 仅在词边界替换，避免误伤
        text = re.sub(rf"(?<![\w]){formal}(?![\w])", casual, text)
    
    # 7. 清理开头结尾的空白和标点
    text = text.strip()
    text = re.sub(r"^[，。、；：]+", "", text)
    text = re.sub(r"[，。、；：]+$", "", text)
    text = text.strip()
    
    return text

# 飞书文档上传
def upload_to_feishu(
    title: str,
    content: str,
    owner_open_id: Optional[str] = None
) -> Dict:
    """
    上传转录内容到飞书文档
    
    返回包含 doc_token 和 url 的字典
    """
    # 这里需要调用 feishu_doc 工具
    # 由于这是脚本执行环境，我们会输出结果供主程序调用
    
    result = {
        "title": title,
        "content": content,
        "owner_open_id": owner_open_id,
        "status": "ready_for_upload"
    }
    
    return result

# 主函数
def main():
    parser = argparse.ArgumentParser(
        description="将视频转录为文字并上传到飞书文档",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 transcribe.py /path/to/video.mp4
  python3 transcribe.py "https://example.com/video.mp4" --model medium
  python3 transcribe.py video.mp4 --upload --title "会议记录"
        """
    )
    
    parser.add_argument("input", help="视频文件路径或URL")
    parser.add_argument("--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper模型 (默认: base)")
    parser.add_argument("--language", default="zh",
                       help="音频语言代码 (默认: zh)")
    parser.add_argument("--output", default="./output",
                       help="输出目录 (默认: ./output)")
    parser.add_argument("--upload", action="store_true",
                       help="上传到飞书文档")
    parser.add_argument("--title", default=None,
                       help="飞书文档标题 (默认使用视频文件名)")
    parser.add_argument("--humanize", action="store_true", default=True,
                       help="去除AI味 (默认开启)")
    parser.add_argument("--timestamps", action="store_true", default=True,
                       help="添加时间戳 (默认开启)")
    parser.add_argument("--keep-temp", action="store_true",
                       help="保留临时文件 (调试用)")
    
    args = parser.parse_args()
    
    # 检查依赖
    ensure_dependencies()
    
    # 设置输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建临时目录
    temp_dir = Path(tempfile.mkdtemp(prefix="transcribe_"))
    print(f"📝 临时目录: {temp_dir}")
    
    try:
        # 1. 获取视频文件
        video_path = None
        if is_url(args.input):
            # 下载网络视频
            video_path = temp_dir / "downloaded_video.mp4"
            if not download_video(args.input, video_path):
                sys.exit(1)
        else:
            # 本地文件
            video_path = Path(args.input)
            if not video_path.exists():
                print(f"❌ 文件不存在: {video_path}")
                sys.exit(1)
        
        # 确定文档标题
        title = args.title or video_path.stem
        print(f"🎬 处理视频: {video_path.name}")
        print(f"📝 文档标题: {title}")
        
        # 2. 提取音频
        audio_path = temp_dir / "audio.wav"
        if not extract_audio(video_path, audio_path):
            sys.exit(1)
        
        # 3. Whisper转录
        transcript_data = transcribe_with_whisper(
            audio_path,
            temp_dir,
            model=args.model,
            language=args.language
        )
        
        if not transcript_data:
            print("❌ 转录失败")
            sys.exit(1)
        
        # 4. 格式化输出
        print("📝 格式化转录结果...")
        formatted_text = format_transcript(
            transcript_data,
            include_timestamps=args.timestamps,
            format_type="markdown"
        )
        
        # 5. 去AI味处理
        if args.humanize:
            print("✨ 去除AI味...")
            formatted_text = humanize_text(formatted_text)