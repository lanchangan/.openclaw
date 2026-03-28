# Skill Vetting - 技能安全审核工具

自动审核新安装的技能是否安全，防止恶意代码、权限滥用和隐私泄露。

## 功能特性

### 🔍 多层安全扫描
- **静态代码扫描**：分析技能代码中的恶意特征
- **动态行为分析**：在沙箱中运行技能，监控实际行为
- **权限一致性检查**：验证技能声明的权限和实际使用是否一致

### 📊 智能风险评估
- 四级风险评级：安全/低风险/中风险/高风险
- 自动生成详细的安全评估报告
- 提供明确的安装建议和修复方案

### 🛡️ 自动防护机制
- 自动拦截高风险技能安装
- 中风险技能需要用户确认后安装
- 监控已安装技能的运行行为
- 异常行为自动告警和阻止

### 📝 完整审计记录
- 保存所有技能的审核历史
- 支持安全审计和追溯
- 跟踪技能版本更新的安全变化

## 安装方法

### 手动安装
1. 将本技能文件夹放到 `~/.openclaw/skills/skill-vetting/`
2. 重启OpenClaw服务即可自动加载

### 自动安装
```bash
clawhub install skill-vetting
```

## 使用方法

### 手动审核技能
```bash
# 审核指定技能
python ~/.openclaw/skills/skill-vetting/scripts/audit_skill.py <技能路径>

# 审核并自动批准低风险技能
python ~/.openclaw/skills/skill-vetting/scripts/audit_skill.py <技能路径> --auto-approve

# 仅进行静态扫描
python ~/.openclaw/skills/skill-vetting/scripts/scan_skill.py <技能路径>
```

### 自动审核
技能安装时会自动触发审核流程：
1. ✅ 低风险技能：自动通过安装
2. 🟡 中风险技能：提示用户确认
3. 🔴 高风险技能：自动阻止安装

## 配置选项

在 `~/.openclaw/config.yaml` 中可以配置审核策略：

```yaml
skill_vetting:
  # 审核严格程度：low/medium/high
  strictness: medium
  # 自动阻止高风险技能
  auto_block_high_risk: true
  # 自动批准低风险技能
  auto_approve_low_risk: true
  # 扫描超时时间（秒）
  scan_timeout: 30
  # 保留的审核记录数量
  max_audit_records: 100
```

## 审核规则

### 高风险（自动阻止）
- 包含恶意代码特征（挖矿、勒索、后门等）
- 未经授权访问系统敏感文件
- 执行未声明的危险系统命令
- 收集并上传用户隐私数据

### 中风险（需用户确认）
- 使用了未声明的权限
- 包含可疑的网络请求
- 执行系统命令但已声明权限
- 包含硬编码的敏感信息

### 低风险（自动通过）
- 代码格式不规范
- 注释中包含敏感词
- 非功能性的小问题
- 不影响安全的警告

### 安全（自动通过）
- 无任何安全问题
- 权限声明和实际使用一致
- 代码功能符合描述

## 目录结构

```
skill-vetting/
├── SKILL.md              # 技能定义文件
├── README.md             # 使用说明
├── scripts/
│   ├── scan_skill.py     # 静态扫描脚本
│   ├── audit_skill.py    # 完整审核脚本
│   └── monitor_skill.py  # 运行时监控脚本
└── rules/
    └── malicious_patterns.yaml  # 恶意特征库
```

## 安全最佳实践

1. **始终审核新技能**：安装任何第三方技能前都要进行安全审核
2. **定期扫描已安装技能**：每月至少扫描一次已安装的技能
3. **及时更新安全规则**：定期更新恶意特征库到最新版本
4. **最小权限原则**：只给技能授予必要的最小权限

## 问题反馈

如果发现误报或者漏报，请提交Issue到我们的GitHub仓库。
