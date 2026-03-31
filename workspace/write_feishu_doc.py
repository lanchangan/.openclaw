import requests
import json

# 飞书应用配置
APP_ID = "cli_a92dc000da789cc2"
APP_SECRET = "uRStntqXMbvPZLoAF7XYufH2RIDxExxZ"
DOC_ID = "Nct2dFS2Ao3FPxxUzS2ct3rLn3C"

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

# 写入文档内容 - 使用更简单的方式
def write_doc_simple(token, doc_id):
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 创建标题块
    blocks_data = [
        {
            "block_type": 3,  # heading1
            "heading1": {
                "elements": [{"text_run": {"content": "股票量化分析与交易技能推荐"}}]
            }
        },
        {
            "block_type": 2,  # text
            "text": {
                "elements": [{"text_run": {"content": "搜索日期：2026年3月31日 | 来源：ClawHub + 腾讯技能中心"}}]
            }
        },
        {
            "block_type": 3,  # heading1
            "heading1": {
                "elements": [{"text_run": {"content": "推荐技能 TOP 4"}}]
            }
        },
        {
            "block_type": 4,  # heading2
            "heading2": {
                "elements": [{"text_run": {"content": "1. Stock Copilot Pro ⭐⭐⭐⭐⭐"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "链接：https://clawhub.ai/buxibuxi/stock-copilot-pro"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "功能：全球市场支持（美股/港股/A股）、多维分析、早晚报、行业雷达、自选股管理"}}]
            }
        },
        {
            "block_type": 4,
            "heading2": {
                "elements": [{"text_run": {"content": "2. FinLab ⭐⭐⭐⭐⭐"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "链接：https://clawhub.ai/koreal6803/finlab"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "功能：台湾股市量化框架、完整回测引擎、券商对接自动交易"}}]
            }
        },
        {
            "block_type": 4,
            "heading2": {
                "elements": [{"text_run": {"content": "3. Backtest Expert ⭐⭐⭐⭐"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "链接：https://clawhub.ai/veeramanikandanr48/backtest-expert"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "功能：专业回测方法论、压力测试、参数敏感性分析"}}]
            }
        },
        {
            "block_type": 4,
            "heading2": {
                "elements": [{"text_run": {"content": "4. Ptrade ⭐⭐⭐⭐"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "链接：https://clawhub.ai/coderwpf/ptrade"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "功能：A股实盘自动下单、融资融券支持"}}]
            }
        },
        {
            "block_type": 3,
            "heading1": {
                "elements": [{"text_run": {"content": "推荐组合"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "日常投资分析 → Stock Copilot Pro"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "量化策略开发 → FinLab"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "策略验证 → Backtest Expert"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "实盘交易 → Ptrade"}}]
            }
        },
        {
            "block_type": 3,
            "heading1": {
                "elements": [{"text_run": {"content": "重要提示"}}]
            }
        },
        {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": "⚠️ 不要让AI直接下单，回测不能代表未来，小资金验证优先"}}]
            }
        }
    ]
    
    for i, block_data in enumerate(blocks_data):
        data = {
            "children": [block_data],
            "index": i
        }
        try:
            resp = requests.post(url, headers=headers, json=data)
            print(f"块 {i+1}/{len(blocks_data)}: {resp.status_code}")
        except Exception as e:
            print(f"块 {i+1} 错误: {e}")

# 执行
token = get_token()
print(f"Token获取成功")
print(f"开始写入内容...")
write_doc_simple(token, DOC_ID)
print(f"完成！文档链接: https://feishu.cn/docx/{DOC_ID}")
