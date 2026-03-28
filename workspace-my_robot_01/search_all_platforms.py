
from tavily import TavilyClient
import yaml
import os

# Expand home directory
config_path = os.path.expanduser('~/.openclaw/config.yaml')

# 读取配置
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    
api_key = config['web']['tavily']['api_key']
tavily = TavilyClient(api_key=api_key)

# 搜索三个平台
product_name = "美的机皇550法式多门冰箱 制冰 MR-550WUFIPZE"

platforms = [
    f"美的550法式多门冰箱 制冰 京东官方旗舰店 最新价格",
    f"美的550法式多门冰箱 制冰 淘宝官方旗舰店 最新价格", 
    f"美的550法式多门冰箱 制冰 拼多多官方旗舰店 最新价格"
]

print("=" * 70)
print(f"商品：{product_name}")
print("搜索三大平台价格...")
print("=" * 70 + "\n")

all_results = []
for query in platforms:
    print(f"\n【{query.split(' ')[2]}】")
    print("-" * 50)
    response = tavily.search(query, search_depth='advanced')
    if response.get('answer'):
        print(f"摘要: {response['answer']}")
    else:
        print("摘要: 无自动摘要")
    print()
    for i, result in enumerate(response['results'][:2]):
        title = result.get("title", "无标题")
        url = result["url"]
        content = result.get("content", "")[:250]
        print(f"  {i+1}. {title}")
        print(f"     链接: {url}")
        print(f"     摘要: {content}...")
    all_results.append({
        'platform': query.split(' ')[2],
        'response': response
    })
    print()

print("\n" + "=" * 70)
print("搜索完成")
