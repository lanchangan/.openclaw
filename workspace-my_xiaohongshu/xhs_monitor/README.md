# 小红书私信自动回复监控

## 功能说明

24小时监控小红书私信，自动根据消息内容回复：

| 消息类型 | 回复内容 |
|---------|---------|
| 咨询教室/场地 | 引导加联系方式（lzab0502） |
| 咨询商品/价格 | 回复产品介绍和价格 |
| 其他消息 | 自动回复 |

## 快速开始

### 1. 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 2. 启动监控

双击 `start_monitor.bat` 或运行：

```bash
python xhs_monitor.py
```

### 3. 首次登录

首次运行时会弹出浏览器窗口，请在浏览器中登录小红书账号，登录完成后回到命令行按回车键继续。

## 配置说明

编辑 `config.json`：

```json
{
  "wechat_id": "lzab0502",
  "poll_interval": 30,
  "auto_reply": true
}
```

| 配置项 | 说明 |
|--------|------|
| wechat_id | 你的联系方式 |
| poll_interval | 检查消息间隔（秒） |
| auto_reply | 是否自动回复 |

## 文件结构

```
xhs_monitor/
├── xhs_monitor.py    # 主监控脚本
├── xhs_browser.py    # 浏览器自动化
├── config.json       # 配置文件
├── cookies.json      # 登录信息（自动生成）
├── start_monitor.bat # Windows启动脚本
├── README.md         # 说明文档
└── logs/             # 日志目录
```

## 注意事项

- 首次使用需要手动在浏览器登录
- 登录信息会保存在 `cookies.json` 中
- 建议定期检查日志 `logs/xhs_monitor.log`
- 如遇Cookie过期，删除 `cookies.json` 重新登录即可
