# -*- coding: utf-8 -*-
"""
首次登录 - 直接打开浏览器让用户手动登录，然后保存Cookies
"""

import asyncio
import json
from pathlib import Path

async def first_login():
    """首次登录"""
    from playwright.async_api import async_playwright
    
    print("=" * 50)
    print("小红书首次登录引导")
    print("=" * 50)
    print("\n步骤：")
    print("1. 浏览器会自动打开")
    print("2. 请在浏览器中登录你的小红书账号")
    print("3. 登录成功后，访问通知页面确认")
    print("4. 回到这里按回车键保存登录状态\n")
    
    cookies_file = Path(__file__).parent / "cookies.json"
    screenshot_file = Path(__file__).parent / "logs" / "after_login.png"
    
    playwright = await async_playwright().start()
    
    # 使用Edge浏览器，不加载之前的cookies
    browser = await playwright.chromium.launch(
        headless=False,
        channel="msedge",
        args=['--disable-blink-features=AutomationControlled']
    )
    
    context = await browser.new_context(
        viewport={'width': 1280, 'height': 720},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    
    page = await context.new_page()
    
    try:
        print("正在打开小红书首页...")
        await page.goto("https://www.xiaohongshu.com", timeout=30000)
        
        print("\n浏览器已打开！请登录你的小红书账号。")
        print("登录成功后，可以访问通知页面确认，然后回到这里按回车键继续...")
        input("\n登录完成后，按回车键保存登录状态...")
        
        # 保存cookies
        print("\n正在保存登录状态...")
        cookies = await context.cookies()
        with open(cookies_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print(f"已保存 {len(cookies)} 个 cookies 到 {cookies_file}")
        
        # 尝试访问通知页面
        print("\n正在测试访问通知页面...")
        await page.goto("https://www.xiaohongshu.com/notification", timeout=30000)
        await page.wait_for_timeout(3000)
        
        print(f"当前URL: {page.url}")
        print(f"页面标题: {await page.title()}")
        
        # 截图
        await page.screenshot(path=str(screenshot_file), full_page=False)
        print(f"已截图保存到: {screenshot_file}")
        
        if "/login" in page.url:
            print("\n⚠️  看起来还在登录页面，请确保已成功登录！")
        else:
            print("\n✅ 登录状态保存成功！")
        
        print("\n你可以继续在浏览器中浏览页面，找到私信/聊天入口后告诉我。")
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
        asyncio.run(first_login())
    except KeyboardInterrupt:
        print("\n已退出")
