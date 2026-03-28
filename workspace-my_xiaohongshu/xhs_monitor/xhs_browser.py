# -*- coding: utf-8 -*-
"""
小红书私信监控 - 浏览器自动化部分
使用 Playwright 实现浏览器控制
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# 导入消息分类和回复生成
sys.path.insert(0, str(Path(__file__).parent))
from xhs_monitor import classify_message, generate_reply

# ============ Cookie管理 ============

async def save_cookies(context, cookies_file: Path):
    """保存cookies"""
    cookies = await context.cookies()
    with open(cookies_file, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    logger.info(f"已保存 cookies 到 {cookies_file}")

async def load_cookies(context, cookies_file: Path):
    """加载cookies"""
    if cookies_file.exists():
        try:
            with open(cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            logger.info(f"已加载 cookies 从 {cookies_file}")
            return True
        except Exception as e:
            logger.warning(f"加载 cookies 失败: {e}")
    return False

# ============ 登录引导 ============

async def first_time_login_guide():
    """首次登录引导（显示浏览器让用户手动登录）"""
    from playwright.async_api import async_playwright
    
    logger.info("=" * 50)
    logger.info("首次使用 - 请先登录小红书")
    logger.info("=" * 50)
    logger.info("1. 浏览器窗口会自动打开")
    logger.info("2. 请在浏览器中登录小红书账号")
    logger.info("3. 登录成功后，回到这里按回车键继续")
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,  # 显示浏览器
        args=['--disable-blink-features=AutomationControlled']
    )
    context = await browser.new_context(
        viewport={'width': 1280, 'height': 720},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    
    page = await context.new_page()
    await page.goto("https://www.xiaohongshu.com")
    
    # 等待用户登录
    logger.info("浏览器已打开，请登录小红书...")
    input("登录完成后，按回车键继续...")
    
    # 保存cookies
    cookies_file = Path(__file__).parent / "cookies.json"
    await save_cookies(context, cookies_file)
    
    await browser.close()
    await playwright.stop()
    
    logger.info("登录信息已保存！")
    return True

# ============ 监控循环 ============

async def monitor_loop():
    """主监控循环"""
    from playwright.async_api import async_playwright
    
    config_file = Path(__file__).parent / "config.json"
    cookies_file = Path(__file__).parent / "cookies.json"
    
    # 加载配置
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {"poll_interval": 30, "auto_reply": True}
    
    poll_interval = config.get("poll_interval", 30)
    auto_reply = config.get("auto_reply", True)
    
    # 检查是否首次使用
    if not cookies_file.exists():
        await first_time_login_guide()
    
    # 启动浏览器
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,
        args=['--disable-blink-features=AutomationControlled']
    )
    context = await browser.new_context(
        viewport={'width': 1280, 'height': 720},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    
    # 加载cookies
    await load_cookies(context, cookies_file)
    
    logger.info("=" * 50)
    logger.info("监控已启动")
    logger.info(f"轮询间隔: {poll_interval}秒")
    logger.info(f"自动回复: {'开启' if auto_reply else '关闭'}")
    logger.info("=" * 50)
    
    # 记录已处理的消息，避免重复回复
    processed_messages = set()
    
    try:
        while True:
            try:
                # 访问小红书主页检查登录状态
                page = await context.new_page()
                try:
                    await page.goto("https://www.xiaohongshu.com", timeout=30000)
                    await page.wait_for_timeout(2000)
                    
                    # 检查是否还在登录状态
                    title = await page.title()
                    logger.debug(f"当前页面: {page.url}, 标题: {title}")
                    
                    # 这里需要根据小红书实际页面结构来实现消息检查
                    # 暂时只输出日志，后续根据实际页面完善
                    logger.debug("检查消息中...")
                    
                except Exception as e:
                    logger.warning(f"访问页面出错: {e}")
                finally:
                    await page.close()
                
                # 定期保存cookies
                await save_cookies(context, cookies_file)
                
            except Exception as e:
                logger.error(f"监控出错: {e}")
            
            await asyncio.sleep(poll_interval)
            
    except asyncio.CancelledError:
        logger.info("监控已取消")
    except KeyboardInterrupt:
        logger.info("收到停止信号")
    finally:
        # 退出前保存cookies
        try:
            await save_cookies(context, cookies_file)
        except:
            pass
        await browser.close()
        await playwright.stop()
        logger.info("监控已停止")

def run_monitor():
    """运行监控（同步入口）"""
    try:
        asyncio.run(monitor_loop())
    except KeyboardInterrupt:
        logger.info("程序已退出")

if __name__ == "__main__":
    run_monitor()
