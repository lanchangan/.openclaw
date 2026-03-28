
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
response = tavily.search('美的 550法式多门冰箱 制冰 京东 最新价格', search_depth='advanced')

print('=== 自动摘要 ===')
print(response['answer'])
print('\n' + '='*60)
print('\n=== 搜索结果详情 ===')
for i, result in enumerate(response['results']):
    print(f'\n[{i+1}] {result["title"]}')
    print(f'URL: {result["url"]}')
    content_snippet = result.get("content", "")[:300]
    print(f'内容摘要: {content_snippet}...')
