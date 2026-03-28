
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日价格监控脚本
美的550法式多门冰箱 - 三大平台价格查询
每天早晚运行一次
"""

from tavily import TavilyClient
import yaml
import os
import json
from datetime import datetime

# 配置
PRODUCT_NAME = "美的M60 MR-550WUFIPZE 550升法式多门制冰冰箱"
PRODUCT_MODEL = "MR-550WUFIPZE"
PRODUCT_SPEC = "法式多门 带制冰 双系统"

# 读取配置
config_path = os.path.expanduser('~/.openclaw/config.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

api_key = config['web']['tavily']['api_key']
tavily = TavilyClient(api_key=api_key)

# 搜索查询模板
SEARCH_QUERIES = [
    {
        "platform": "京东",
        "query": f"美的MR-550WUFIPZE 多少钱 价格"
    },
    {
        "platform": "淘宝",
        "query": f"淘宝 美的MR-550WUFIPZE 价格"
    },
    {
        "platform": "拼多多",
        "query": f"拼多多 美的MR-550WUFIPZE 价格"
    }
]

def search_price(query):
    """搜索单个平台的价格"""
    try:
        response = tavily.search(query, search_depth='advanced')
        results = []
        for r in response['results'][:3]:
            result = {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", "")[:500]
            }
            results.append(result)
        
        answer = response.get('answer', None)
        return {
            "success": True,
            "answer": answer,
            "results": results
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def extract_price_from_content(content):
    """从内容中提取价格数字"""
    import re
    # 多种价格匹配模式
    patterns = [
        r'(\d{3,4})(?:\s*元| yuan|RMB|￥)',  # 带单位
        r'[￥]\s*(\d{3,4})',  # 人民币符号在前
        r'(\d{3,4})\s*$',  # 行尾的数字，很可能是价格
        r'(\d{3,4})',  # 任何3-4位数字，过滤后面在合理区间
    ]
    prices = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        prices.extend([int(p) for p in matches])
    
    # 去重并过滤在合理价格区间
    prices = sorted(list(set([p for p in prices if 3000 <= p <= 8000])))
    return prices

def main():
    """主函数"""
    print(f"===== 价格监控 - {PRODUCT_NAME} =====")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_prices = []
    report = []
    report.append(f"# 冰箱价格监控日报\n")
    report.append(f"**商品:** {PRODUCT_NAME}")
    report.append(f"**型号:** {PRODUCT_MODEL}")
    report.append(f"**规格:** {PRODUCT_SPEC}")
    report.append(f"**查询时间:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    for item in SEARCH_QUERIES:
        print(f"正在搜索 {item['platform']}...")
        result = search_price(item['query'])
        platform = item['platform']
        
        if not result['success']:
            report.append(f"## [X] {platform} - 查询失败")
            report.append(f"错误: {result['error']}\n")
            continue
        
        # 提取价格
        all_prices_content = ""
        prices_found = []
        for r in result['results']:
            prices = extract_price_from_content(r['content'])
            prices_found.extend(prices)
            all_prices_content += r['content']
        
        prices_found = [p for p in prices_found if 3000 <= p <= 8000]  # 合理价格区间
        
        if prices_found:
            min_price = min(prices_found)
            max_price = max(prices_found)
            all_prices.append({
                "platform": platform,
                "min": min_price,
                "max": max_price,
                "found": len(prices_found)
            })
            report.append(f"## [OK] {platform}")
            report.append(f"**最低价:** `{min_price} 元`")
            report.append(f"**价格区间:** {min_price} - {max_price} 元")
            report.append(f"**找到价格数据:** {len(prices_found)} 条")
            # 添加前两个结果链接
            for i, r in enumerate(result['results'][:2]):
                if r.get("url"):
                    report.append(f"  - [链接 {i+1}]({r['url']})")
            report.append("")
        else:
            report.append(f"## [搜索中] {platform}")
            report.append(f"未找到明确价格数据\n")
    
    # 汇总最低价
    report.append("## 价格汇总")
    report.append("| 平台 | 最低价(元) |")
    report.append("|------|------------|")
    for p in sorted(all_prices, key=lambda x: x['min']):
        report.append(f"| {p['platform']} | {p['min']} |")
    
    if all_prices:
        overall_min = min(all_prices, key=lambda x: x['min'])
        report.append(f"\n**当前全网最低价: {overall_min['platform']} - {overall_min['min']} 元**")
        
        # 保存历史
        history_file = os.path.expanduser('~/.openclaw/workspace-my_robot_01/price_history.json')
        history = []
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        history.append({
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "prices": all_prices,
            "overall_min": overall_min
        })
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    # 输出报告
    full_report = "\n".join(report)
    print("\n" + full_report)
    
    # 保存报告到文件
    report_file = os.path.expanduser('~/.openclaw/workspace-my_robot_01/latest_price_report.md')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(full_report)
    
    print(f"\n报告已保存到: {report_file}")
    print("\n价格监控完成!")

if __name__ == "__main__":
    main()
