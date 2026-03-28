# -*- coding: utf-8 -*-
"""
探索小红书页面结构，找到消息入口
"""

import asyncio
import json
from pathlib import Path

async def explore_page():
    """探索页面"""
    from playwright.async_api import async_playwright
    
    print("正在探索小红书页面结构...")
    
    cookies_file = Path(__file__).parent / "cookies.json"
    screenshot_file = Path(__file__).parent / "logs" / "xhs_page.png"
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )
    context = await browser.new_context(
        viewport={'width': 1280, 'height': 720},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    
    # 加载cookies
    if cookies_file.exists():
        with open(cookies_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)
        print(f"已加载 {len(cookies)} 个 cookies")
    
    page = await context.new_page()
    
    try:
        print("正在访问小红书...")
        await page.goto("https://www.xiaohongshu.com", timeout=30000)
        await page.wait_for_timeout(3000)
        
        print(f"当前URL: {page.url}")
        print(f"页面标题: {await page.title()}")
        
        # 截图
        await page.screenshot(path=str(screenshot_file), full_page=False)
        print(f"已截图保存到: {screenshot_file}")
        
        # 查找所有可见元素
        print("\n正在分析页面元素...")
        
        # 查找可能的消息/聊天入口
        selectors_to_check = [
            'a[href*="message"]',
            'a[href*="chat"]',
            'a[href*="notification"]',
            '.message',
            '.chat',
            '.notification',
            '[class*="message"]',
            '[class*="chat"]',
            '[class*="notification"]',
            'button',
            'a[href]'
        ]
        
        for selector in selectors_to_check[:5]:
            elements = await page.query_selector_all(selector)
            if elements:
                print(f"\n找到 {len(elements)} 个元素匹配: {selector}")
                for i, el in enumerate(elements[:3]):
                    try:
                        text = await el.inner_text()
                        href = await el.get_attribute('href') if selector.startswith('a') else None
                        class_name = await el.get_attribute('class')
                        print(f"  [{i}] text: {text[:50] if text else 'None'}, href: {href}, class: {class_name[:50] if class_name else 'None'}")
                    except:
                        pass
        
        print("\n页面分析完成！")
        print("你可以在浏览器中查看页面，找到消息入口后告诉我。")
        print("按 Ctrl+C 退出...")
        
        while True:
            await asyncio.sleep(1)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    try:
        asyncio.run(explore_page())
    except KeyboardInterrupt:
        print("\n已退出")
