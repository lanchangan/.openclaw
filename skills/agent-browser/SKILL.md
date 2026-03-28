---
name: agent-browser
description: AI智能浏览器控制工具，支持自动访问网页、提取内容、填写表单、点击交互、截图等功能。帮助AI自动化完成网页操作、信息收集、数据爬取等任务。当需要访问网页、获取网页内容、进行网页交互时使用。
---

# Agent Browser 智能浏览器技能

## 核心功能
### 🌐 网页访问
- **自动导航**：自动访问指定URL，支持cookie、代理、自定义请求头
- **动态渲染**：支持JavaScript渲染的单页应用(SPA)
- **等待机制**：智能等待页面加载完成，支持按元素、超时等待
- **会话管理**：支持多会话隔离，保存登录状态和Cookie

### 📝 内容提取
- **智能提取**：自动提取网页的标题、正文、链接、图片等内容
- **结构化数据**：提取表格、列表、商品信息等结构化数据
- **全文搜索**：在网页内容中搜索指定关键词
- **截图功能**：支持全屏截图、元素截图、长截图

### 🖱️ 交互操作
- **点击操作**：智能识别可点击元素（按钮、链接、菜单等）并点击
- **表单填写**：自动填写表单、输入框、下拉选择框
- **键盘操作**：支持按键输入、快捷键、组合键操作
- **滚动操作**：页面滚动、滚动到指定元素、无限滚动加载

### 🔍 元素定位
- **智能定位**：支持按文本、CSS选择器、XPath、ID等多种定位方式
- **模糊匹配**：支持部分文本匹配、正则表达式匹配
- **动态识别**：自动识别页面变化后的元素位置
- **防检测**：模拟人类操作行为，避免被反爬系统检测

### 🛡️ 反爬规避
- **行为模拟**：模拟人类的点击间隔、移动轨迹、滚动速度
- **指纹保护**：随机User-Agent、浏览器指纹、屏幕分辨率
- **代理支持**：支持HTTP/HTTPS/SOCKS5代理
- **验证码识别**：集成验证码识别服务，自动处理验证码

## 使用示例
### 基本网页访问
```python
# 打开浏览器并访问网页
browser = AgentBrowser(headless=True)
browser.goto("https://www.example.com")

# 获取网页内容
title = browser.get_title()
content = browser.get_content()
links = browser.get_links()

# 截图
browser.screenshot("/tmp/screenshot.png")

# 关闭浏览器
browser.close()
```

### 自动搜索
```python
browser.goto("https://www.google.com")
browser.fill('input[name="q"]', "OpenClaw AI助手")
browser.press("Enter")
browser.wait_for_load()

# 提取搜索结果
results = browser.extract_search_results()
for result in results:
    print(f"标题: {result['title']}")
    print(f"链接: {result['url']}")
    print(f"摘要: {result['snippet']}\n")
```

### 表单提交
```python
browser.goto("https://example.com/login")
browser.fill('#username', 'your-username')
browser.fill('#password', 'your-password')
browser.click('button[type="submit"]')
browser.wait_for_navigation()

# 验证是否登录成功
if "Dashboard" in browser.get_title():
    print("登录成功！")
```

## 配置选项
```yaml
agent_browser:
  # 浏览器类型：chrome/firefox/edge
  browser_type: "chrome"
  # 是否无头模式
  headless: true
  # 窗口大小
  viewport: {"width": 1920, "height": 1080}
  # 用户代理
  user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  # 操作延迟（毫秒）
  delay: 1000
  # 超时时间（秒）
  timeout: 30
  # 代理设置
  proxy: ""
```

## 触发场景
- 需要访问网页获取最新内容
- 自动进行网页交互（填写表单、提交数据等）
- 抓取网站数据、提取结构化信息
- 自动化测试网页功能
- 监控网页变化和更新
- 模拟用户操作完成复杂的网页任务
