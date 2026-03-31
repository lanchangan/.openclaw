import requests
import json

# 飞书应用配置
APP_ID = "cli_a92dc000da789cc2"
APP_SECRET = "uRStntqXMbvPZLoAF7XYufH2RIDxExxZ"
OWNER_OPEN_ID = "ou_e7a32d874706bf82f2d409b0427b7e9e"

# 获取 tenant_access_token
def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    resp = requests.post(url, json=data)
    result = resp.json()
    if result.get("code") == 0:
        return result["tenant_access_token"]
    else:
        raise Exception(f"获取token失败: {result}")

# 创建文档
def create_doc(token, title):
    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": title
    }
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()
    if result.get("code") == 0:
        return result["data"]["document"]["document_id"]
    else:
        raise Exception(f"创建文档失败: {result}")

# 写入文档内容
def write_doc(token, doc_id, content):
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children/batch_create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 简化：直接用文本块
    blocks = []
    for line in content.split('\n'):
        if line.strip():
            block = {
                "block_type": 2,  # text block
                "text": {
                    "elements": [{"text_run": {"content": line}}]
                }
            }
            blocks.append(block)
    
    data = {
        "children": blocks[:50],  # 限制数量
        "index": 0
    }
    resp = requests.post(url, headers=headers, json=data)
    return resp.json()

# 主函数
token = get_token()
print(f"Token获取成功")

doc_id = create_doc(token, "股票量化分析与交易技能推荐 - 2026年3月31日")
print(f"文档创建成功: {doc_id}")

# 文档链接
doc_url = f"https://feishu.cn/docx/{doc_id}"
print(f"文档链接: {doc_url}")

# 简单内容
content = """# 股票量化分析与交易技能推荐

搜索日期：2026年3月31日
来源平台：ClawHub + 腾讯技能中心

## 推荐技能 TOP 4

### 1. Stock Copilot Pro
链接：https://clawhub.ai/buxibuxi/stock-copilot-pro
- 全球市场支持（美股/港股/A股）
- 多维分析（基本面+技术面+情绪面）
- 早晚报、行业雷达、自选股管理

### 2. FinLab
链接：https://clawhub.ai/koreal6803/finlab
- 台湾股市量化框架
- 完整回测引擎
- 券商对接自动交易

### 3. Backtest Expert
链接：https://clawhub.ai/veeramanikandanr48/backtest-expert
- 专业回测方法论
- 压力测试、参数敏感性分析

### 4. Ptrade
链接：https://clawhub.ai/coderwpf/ptrade
- A股实盘自动下单
- 融资融券支持

## 推荐组合
- 日常投资分析 → Stock Copilot Pro
- 量化策略开发 → FinLab
- 策略验证 → Backtest Expert
- 实盘交易 → Ptrade

## 重要提示
- 不要让AI直接下单
- 回测不能代表未来
- 小资金验证优先
"""

# 写入内容
result = write_doc(token, doc_id, content)
print(f"内容写入结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
