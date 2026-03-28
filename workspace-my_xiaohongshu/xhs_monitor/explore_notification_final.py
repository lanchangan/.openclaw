# -*- coding: utf-8 -*-
"""
探索小红书通知/消息页面 - 使用Edge浏览器
"""

import asyncio
import json
from pathlib import Path

async def explore_notification():
    """探索通知页面"""
    from playwright.async_api import async_playwright
    
    print("正在探索小红书通知页面（使用Edge浏览器）...")
    
    cookies_file = Path(__file__).parent / "cookies.json"
    screenshot_file = Path(__file__).parent / "logs" / "xhs_notification_final.png"
    
    playwright = await async_playwright().start()
    
    # 使用Edge浏览器
    browser = await playwright.chromium.launch(
        headless=False,
        channel="msedge",
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
        print("正在访问通知页面...")
        await page.goto("https://www.xiaohongshu.com/notification", timeout=30000)
        await page.wait_for_timeout(5000)
        
        print(f"当前URL: {page.url}")
        print(f"页面标题: {await page.title()}")
        
        # 保存cookies
        new_cookies = await context.cookies()
        with open(cookies_file, 'w', encoding='utf-8') as f:
            json.dump(new_cookies, f, ensure_ascii=False, indent=2)
        print(f"已保存 {len(new_cookies)} 个 cookies")
        
        # 截图
        await page.screenshot(path=str(screenshot_file), full_page=False)
        print(f"已截图保存到: {screenshot_file}")
        
        print("\n正在分析页面元素...")
        
        # 查找页面上的所有元素
        print("\n--- 所有链接 ---")
        links = await page.query_selector_all('a[href]')
        for i, link in enumerate(links[:40]):
            try:
                href = await link.get_attribute('href')
                text = await link.inner_text()
                if href:
                    print(f"  [{i}] {text[:50]} -> {href}")
            except:
                pass
        
        print("\n--- 查找可能的消息/聊天入口 ---")
        # 尝试查找有特定class的元素
        selectors = ['.message', '.chat', '.notification-item', '.conversation', '.dialog', '[class*="message"]']
        for sel in selectors:
            els = await page.query_selector_all(sel)
            if els:
                print(f"  {sel}: 找到 {len(els)} 个元素")
        
        print("\n你可以在浏览器中浏览页面，找到私信/聊天的具体内容后告诉我。")
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
        asyncio.run(explore_notification())
    except KeyboardInterrupt:
        print("\n已退出")
