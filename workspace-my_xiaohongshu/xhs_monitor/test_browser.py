# -*- coding: utf-8 -*-
"""
测试浏览器是否能正常启动
"""

import asyncio
import sys
from pathlib import Path

async def test_browser():
    """测试浏览器"""
    print("正在启动浏览器测试...")
    
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("错误: 未安装 playwright")
        print("请运行: pip install playwright")
        return False
    
    playwright = None
    browser = None
    
    try:
        playwright = await async_playwright().start()
        print("Playwright 初始化成功")
        
        # 启动浏览器（显示窗口）
        browser = await playwright.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        print("浏览器启动成功")
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        print("正在访问小红书...")
        
        await page.goto("https://www.xiaohongshu.com", timeout=30000)
        print(f"页面加载成功: {page.url}")
        print(f"页面标题: {await page.title()}")
        
        # 保存cookies（如果有的话）
        cookies_file = Path(__file__).parent / "cookies.json"
        cookies = await context.cookies()
        if cookies:
            import json
            with open(cookies_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            print(f"已保存 {len(cookies)} 个 cookies 到 {cookies_file}")
        
        print("\n浏览器窗口已打开，请查看。")
        print("你可以在浏览器中登录小红书，登录后按 Ctrl+C 退出...")
        
        # 保持浏览器打开
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n正在退出...")
        
        return True
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()
        print("浏览器已关闭")

if __name__ == "__main__":
    try:
        success = asyncio.run(test_browser())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n已取消")
        sys.exit(0)
