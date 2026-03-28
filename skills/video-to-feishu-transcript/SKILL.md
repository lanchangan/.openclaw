---
name: video-to-feishu-transcript
version: 1.0.0
description: |
  将视频自动转录为文字并上传到飞书文档。支持本地视频文件或链接，使用Whisper本地转录，
  自动去除AI味道，一键生成自然流畅的文字记录并上传至飞书文档。
triggers:
  - "视频转录"
  - "视频转文字"
  - "转录视频"
  - "视频字幕"
  - "视频转飞书"
  - "transcribe video"
  - "视频转文档"
  - "视频文字稿"
metadata:
  clawdbot:
    emoji: "📝"
    requires:
      bins: ["ffmpeg", "whisper"]
    install:
      - id: ffmpeg
        kind: brew
        formula: ffmpeg
        bins: ["ffmpeg"]
        label: "Install ffmpeg (brew)"
      - id: whisper
        kind: pip
        package: openai-whisper
        bins: ["whisper"]
        label: "Install Whisper (pip)"
---

# Video to Feishu Transcript

将视频自动转录为自然流畅的文字记录，并上传到飞书文档。

## 功能特点

- **支持多种输入**: 本地视频文件或下载链接
- **本地Whisper转录**: 无需API调用，保护隐私
- **带时间戳**: 支持段落级时间戳，方便回溯
- **去除AI味**: 自动优化文字，去除机器生成的生硬感
- **一键上传飞书**: 直接生成飞书文档，方便分享协作

## 使用方法

### 转录本地视频文件

```bash
python3 {baseDir}/scripts/transcribe.py "/path/to/video.mp4"
```

### 转录在线视频链接

```bash
python3 {baseDir}/scripts/transcribe.py "https://example.com/video.mp4"
```

### 完整流程：转录并上传到飞书

```bash
# 1. 执行转录（会自动上传到飞书）
python3 {baseDir}/scripts/transcribe.py "/path/to/video.mp4" --upload --title "会议记录"

# 2. 或使用交互式向导
python3 {baseDir}/scripts/wizard.py
```

## 参数说明

### transcribe.py 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 视频文件路径或URL | 必填 |
| `--model` | Whisper模型 | `base` |
| `--language` | 音频语言 | `zh` (中文) |
| `--output` | 输出目录 | `./output` |
| `--upload` | 上传到飞书 | `False` |
| `--title` | 飞书文档标题 | 使用视频名 |
| `--humanize` | 去除AI味 | `True` |
| `--timestamps` | 添加时间戳 | `True` |

### 可用模型

- `tiny`: 最快，准确率较低
- `base`: 推荐，速度与准确率平衡
- `small`: 较慢，准确率更高
- `medium`: 慢，高准确率
- `large`: 最慢，最高准确率

## 输出格式

### 1. 转录结果文件

```
output/
├── {video_name}_transcript.txt      # 纯文本转录
├── {video_name}_with_timestamps.txt # 带时间戳版本
├── {video_name}_humanized.txt       # 去AI味版本
└── {video_name}_final.md            # 最终Markdown格式
```

### 2. 飞书文档结构

```markdown
# 【视频转录】{标题}

## 视频信息
- 文件名: {filename}
- 时长: {duration}
- 转录时间: {timestamp}
- 使用模型: {model}

## 转录内容

### [00:00:00] 开场
{内容段落}

### [00:05:32] 主题一
{内容段落}
...
```

## 依赖安装

### macOS

```bash
# 安装 ffmpeg
brew install ffmpeg

# 安装 whisper
pip install openai-whisper
```

### Ubuntu/Debian

```bash
# 安装 ffmpeg
sudo apt update
sudo apt install ffmpeg

# 安装 whisper
pip install openai-whisper
```

### Windows

```bash
# 使用 chocolatey 安装 ffmpeg
choco install ffmpeg

# 安装 whisper
pip install openai-whisper
```

## 注意事项

1. **硬件要求**: Whisper需要一定的计算资源，建议使用有GPU的机器进行大规模转录
2. **音频质量**: 音频清晰度直接影响转录准确率，建议使用高质量音频源
3. **语言设置**: 正确设置`--language`参数可提升准确率
4. **隐私保护**: 所有转录在本地完成，音频数据不会上传到云端
5. **网络视频**: 下载网络视频需要对应网站支持，部分网站可能需要额外配置

## 故障排除

### 常见问题

**Q: 提示"whisper command not found"**
```bash
# 检查安装
pip show openai-whisper
# 确认 PATH 包含 Python Scripts 目录
```

**Q: 转录结果为空或不准确**
- 检查音频语言参数是否正确
- 尝试使用更大的模型（如 small/medium）
- 检查音频质量是否足够清晰

**Q: 上传飞书失败**
- 检查 Feishu 集成是否已配置
- 确认有足够的权限创建文档
- 查看具体错误信息进行排查

## 进阶用法

### 批量处理多个视频

```bash
# 批量转录目录下所有视频
for video in *.mp4; do
    python3 {baseDir}/scripts/transcribe.py "$video" --upload
done
```

### 自定义后处理

```python
# 在 transcribe.py 基础上添加自定义处理
import sys
sys.path.insert(0, '{baseDir}/scripts')
from transcribe import main

# 自定义处理函数
def custom_process(text):
    # 添加自定义处理逻辑
    return processed_text

# 调用转录
main(custom_processor=custom_process)
```

---

**版本**: 1.0.0  
**更新日期**: 2025-03-19  
**作者**: OpenClaw
