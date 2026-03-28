# Self-Optimization Skill for OpenClaw

自动自我优化技能，帮助AI助手持续改进自身性能和工作效率。

## 功能特性

### 🧠 记忆优化
- 自动梳理每日记忆，提炼重要信息到长期记忆
- 智能归档过期记忆，保持记忆库精简
- 自动去重和分类，提升记忆检索效率

### ⚡ 流程优化
- 分析任务执行记录，识别低效步骤
- 自动生成优化后的工作流模板
- 总结最佳实践，减少重复劳动

### 📚 技能学习
- 自动发现缺失的技能，从ClawHub安装
- 学习新工具的使用方法和最佳实践
- 持续更新技能库，扩展能力边界

### 🔍 自我诊断
- 定期检查系统状态和工具可用性
- 自动修复常见配置和权限问题
- 生成详细的诊断报告，便于问题排查

## 安装方法

### 自动安装（推荐）
```bash
clawhub install self-optimization
```

### 手动安装
1. 下载本技能文件夹到 `~/.openclaw/skills/self-optimization/`
2. 给脚本添加执行权限：
   ```bash
   chmod +x ~/.openclaw/skills/self-optimization/scripts/*.py
   ```
3. 重启OpenClaw即可生效

## 使用方法

### 手动触发
```bash
# 执行记忆优化
python ~/.openclaw/skills/self-optimization/scripts/optimize_memory.py

# 执行自我诊断
python ~/.openclaw/skills/self-optimization/scripts/self_diagnose.py
```

### 自动触发
技能会在以下场景自动运行：
1. 空闲时间（无用户任务时）
2. 任务执行完成后（自动复盘）
3. 遇到错误或失败后（自动诊断修复）
4. 每天凌晨自动执行全量优化

## 配置说明

### 记忆优化配置
- `MEMORY_DIR`: 短期记忆目录（默认：~/.openclaw/workspace/memory）
- `LONG_TERM_MEMORY`: 长期记忆文件路径（默认：~/.openclaw/workspace/MEMORY.md）
- `ARCHIVE_DAYS`: 记忆归档天数（默认：7天）

### 自我诊断配置
- `REPORT_PATH`: 诊断报告保存路径（默认：~/.openclaw/workspace/memory/diagnose_report.json）
- `AUTO_FIX`: 是否自动修复发现的问题（默认：true）

## 目录结构

```
self-optimization/
├── SKILL.md              # 技能定义文件（必须）
├── README.md             # 说明文档
├── scripts/              # 可执行脚本
│   ├── optimize_memory.py   # 记忆优化脚本
│   ├── optimize_workflow.py # 流程优化脚本
│   ├── learn_skills.py      # 技能学习脚本
│   └── self_diagnose.py     # 自我诊断脚本
└── references/           # 参考文档
    └── best_practices.md    # 最佳实践指南
```

## 版本历史

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持记忆优化和自我诊断功能
- 包含基础的流程优化框架

## 许可证

MIT License
