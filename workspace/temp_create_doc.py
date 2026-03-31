#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建飞书文档并写入股票量化分析技能推荐内容
"""

import json
import requests
import os

# 读取 token
token_file = os.path.expanduser("~/.openclaw/cache/feishu_default_token.cache")
try:
    with open(token_file, 'r') as f:
        token = f.read().strip()
except:
    print("Error: Cannot read token file")
    exit(1)

# 创建文档
create_url = "https://open.feishu.cn/open-apis/docx/v1/documents"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

create_data = {
    "title": "股票量化分析与交易技能推荐 - 2026年3月31日"
}

print("Creating document...")
response = requests.post(create_url, headers=headers, json=create_data)
result = response.json()

if result.get("code") != 0:
    print(f"Error creating document: {result}")
    exit(1)

doc_token = result["data"]["document"]["document_id"]
print(f"Document created: {doc_token}")

# 准备文档内容
content = """# 股票量化分析与交易技能推荐

> 搜索时间：2026年3月31日
> 搜索平台：ClawHub + 腾讯技能中心

---

## 🏆 推荐技能 TOP 4

### 1. Stock Copilot Pro ⭐⭐⭐⭐⭐

**来源：** ClawHub  
**链接：** https://clawhub.ai/buxibuxi/stock-copilot-pro

**功能特点：**

- 🌍 **全球市场支持**：支持美股、港股、A股
- 📈 **多维分析**：基本面分析、技术分析、情绪分析、量化分析
- 📊 **核心功能**：
  - 单股分析（analyze）
  - 多股比较（compare）
  - 自选股/持仓管理（watch）
  - 早报/晚报（brief）
  - 行业热点雷达（radar）
- 🔌 **多数据源**：QVeris API、同花顺iFinD、财达子、Alpha Vantage、Finnhub、X情绪

**安装方式：**
可通过 ClawHub 安装

---

### 2. FinLab ⭐⭐⭐⭐⭐

**来源：** ClawHub  
**链接：** https://clawhub.ai/koreal6803/finlab

**功能特点：**

- 📊 **专业量化框架**：台湾股票市场专用
- 🧪 **回测引擎**：支持完整策略回测
- 📉 **风险控制**：止损、止盈、移动止损
- 🔧 **技术指标**：RSI、MACD、MA等
- 🤖 **自动交易**：支持券商对接下单

**使用示例：**

```python
from finlab import data
from finlab.backtest import sim

close = data.get("price:收盤價")
position = close.rise(10) & (close > close.average(60))
report = sim(position, resample="M")
```

**安装命令：**
```bash
uv pip install "finlab>=1.5.9"
```

---

### 3. Backtest Expert ⭐⭐⭐⭐

**来源：** ClawHub  
**链接：** https://clawhub.ai/veeramanikandanr48/backtest-expert

**功能特点：**

- 🎯 **专业回测方法论**：避免过拟合
- 🔍 **压力测试**：参数敏感性分析
- ⚠️ **风险识别**：常见陷阱检测
- 📚 **最佳实践**：系统化交易策略验证

**核心理念：**
> "找到'最不容易失败'的策略，而不是'纸上利润最高'的策略"

---

### 4. Ptrade ⭐⭐⭐⭐

**来源：** ClawHub  
**链接：** https://clawhub.ai/coderwpf/ptrade

**功能特点：**

- 🔄 **自动下单**：支持A股实盘交易
- 📊 **交易函数**：order(), order_value(), order_market()
- 💰 **融资融券**：margin_trade(), margincash_open()
- ⏰ **盘后交易**：after_trading_order()

---

## 📦 其他相关技能

| 技能名称 | 平台 | 用途 | 详情链接 |
|---------|------|------|----------|
| StockAPI | SkillsBot | 量化数据接口 | https://www.skillsbot.cn/skill/8610 |
| MarketPulse | SkillsBot | 实时/历史行情 | https://www.skillsbot.cn/skill/575 |
| HFT Quant Expert | SkillsBot | 高频量化策略 | https://www.skillsbot.cn/skill/4174 |
| YahooQuery | SkillsBot | 雅虎财经数据 | https://www.skillsbot.cn/skill/848 |

---

## 💡 推荐组合

| 场景 | 推荐技能 | 说明 |
|------|----------|------|
| **日常投资分析** | Stock Copilot Pro | 综合分析+早晚报 |
| **量化策略开发** | FinLab | 回测+因子分析 |
| **策略验证** | Backtest Expert | 压力测试 |
| **实盘交易** | Ptrade | A股自动下单 |

---

## 📋 安装建议

### 方案一：综合分析型

适合日常投资决策

```bash
# 安装 Stock Copilot Pro
clawhub install buxibuxi/stock-copilot-pro
```

### 方案二：量化开发型

适合策略开发和回测

```bash
# 安装 FinLab
uv pip install "finlab>=1.5.9"

# 登录获取 Token
python -c "import finlab; finlab.login()"
```

---

## ⚠️ 注意事项

### 风险提示

1. **量化交易有风险**：过往收益不代表未来表现
2. **需要 API Token**：大部分技能需要申请 API Key
3. **数据延迟**：免费版数据可能有延迟
4. **合规要求**：自动交易需遵守券商规定

### 最佳实践

1. **先回测后实盘**：充分验证策略有效性
2. **小额测试**：先用小资金测试系统稳定性
3. **风险控制**：设置止损、仓位限制
4. **持续监控**：定期检查策略表现

---

## 📚 参考资源

- **ClawHub 官网：** https://clawhub.ai
- **腾讯技能中心：** https://skillhub.tencent.com
- **OpenClaw 文档：** https://docs.openclaw.ai
- **FinLab 文档：** https://github.com/koreal6803/finlab-ai

---

## 🔗 相关文章

1. [1分钟部署OpenClaw全自动股票交易指南](https://zhuanlan.zhihu.com/p/2010104973996872203)
2. [OpenClaw 投资Skills深度解析](https://zhuanlan.zhihu.com/p/2012564209100136790)
3. [我用OpenClaw跑了两周量化交易](https://www.cnblogs.com/informatics/p/19668938)

---

*文档生成时间：2026年3月31日*
*数据来源：ClawHub、腾讯技能中心、Tavily搜索*
"""

# 写入内容
write_url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/bulk_create"

# 获取文档根块
get_blocks_url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks"
blocks_response = requests.get(get_blocks_url, headers=headers)
blocks_result = blocks_response.json()

if blocks_result.get("code") != 0:
    print(f"Error getting blocks: {blocks_result}")
    exit(1)

# 找到页面块
page_block = None
for item in blocks_result["data"]["items"]:
    if item["block_type"] == "page":
        page_block = item
        break

if not page_block:
    print("Error: No page block found")
    exit(1)

page_id = page_block["block_id"]
print(f"Page ID: {page_id}")

# 构建内容块
# 这里简化处理，直接发送内容
print("Content prepared, please use feishu_doc write tool")
print(f"Document token: {doc_token}")
print(f"Document URL: https://feishu.cn/docx/{doc_token}")
