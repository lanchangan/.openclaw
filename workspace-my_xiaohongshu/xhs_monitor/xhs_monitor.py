# -*- coding: utf-8 -*-
"""
小红书私信自动回复监控脚本
功能：
1. 监控小红书私信
2. 关键词匹配：咨询商品/价格 -> 回复产品信息；咨询教室 -> 引导加联系方式
3. 其他消息 -> AI自动回复
"""

import json
import time
import logging
import sys
from pathlib import Path

# Setup logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "xhs_monitor.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============ 配置 ============
CONFIG_FILE = Path(__file__).parent / "config.json"

# 商品信息（用于回复商品咨询）
PRODUCT_INFO = """西安边家村教室出租

位置：边家村（地铁口附近）

场地详情：
- 大教室：可容纳15-20人，适合会议、培训、讲座、自习
- 小教室：可容纳6-7人，适合一对一辅导、小班教学

配套：一机（可投屏）、白板、空调暖气、安静独立空间

价格：根据使用时长和频率灵活计费，私信详聊"""

# 教室租赁关键词
CLASSROOM_KEYWORDS = ['教室', '租', '场地', '空间', '会议', '培训', '上课', '辅导', '自习']

# 引导加联系方式的回复（避免直接说微信）
WECHAT_REPLY = """您好！咨询教室租赁的话，方便加我详聊吗？备注"小红书教室"，我的号是：lzab0502"""

def load_config():
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "wechat_id": "lzab0502",
        "poll_interval": 30,
        "auto_reply": True
    }

def save_config(config):
    """保存配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def classify_message(message):
    """分类消息类型"""
    msg_lower = message.lower()
    
    # 检查是否咨询教室/场地
    for keyword in CLASSROOM_KEYWORDS:
        if keyword in msg_lower:
            return "classroom"
    
    # 检查是否咨询商品/价格
    price_keywords = ['价格', '多少钱', '价', '费用', '收费', '便宜', '优惠']
    for keyword in price_keywords:
        if keyword in msg_lower:
            return "product"
    
    # 检查是否只是打招呼
    greeting_keywords = ['你好', '您好', '在吗', 'hi', 'hello', '嗨', '在']
    for keyword in greeting_keywords:
        if keyword in msg_lower and len(message) < 10:
            return "greeting"
    
    return "other"

def generate_reply(message_type, original_message=""):
    """根据消息类型生成回复"""
    if message_type == "classroom":
        return WECHAT_REPLY
    elif message_type == "product":
        return PRODUCT_INFO
    elif message_type == "greeting":
        return "您好！有什么可以帮您的吗？"
    else:
        return "感谢您的消息！您的问题已收到，我会尽快回复。如需了解教室租赁详情，欢迎加我详聊~"

def check_new_messages():
    """检查新消息（实际逻辑在xhs_browser.py中）"""
    return []

def send_reply(user_id, message):
    """发送回复（实际逻辑在xhs_browser.py中）"""
    logger.info(f"向用户 {user_id} 发送回复: {message[:50]}...")
    return True

def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("小红书私信自动回复监控启动")
    logger.info("=" * 50)
    
    config = load_config()
    logger.info(f"配置加载完成")
    
    poll_interval = config.get("poll_interval", 30)
    auto_reply = config.get("auto_reply", True)
    
    logger.info(f"轮询间隔: {poll_interval}秒")
    logger.info(f"自动回复: {'开启' if auto_reply else '关闭'}")
    
    try:
        # 导入并运行浏览器监控
        from xhs_browser import run_monitor
        run_monitor()
            
    except KeyboardInterrupt:
        logger.info("监控已停止")
    except Exception as e:
        logger.error(f"发生错误: {e}")
        raise

if __name__ == "__main__":
    main()
