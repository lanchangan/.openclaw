# -*- coding: utf-8 -*-
import requests
import json
import sys
import io

class EmojiStripper(io.TextIOWrapper):
    def write(self, text):
        emoji_map = {
            '\U0001f308': '[彩虹]', '\U0001f50d': '[搜索]', '\u2705': '[OK]',
            '\u274c': '[X]', '\U0001f4e6': '[包裹]', '\U0001f4e9': '[信]',
            '\U0001f3eb': '[麦克风]', '\U0001f4ac': '[评论]', '\u2764': '[心]',
            '\U0001f49c': '[心]', '\u2b50': '[星]', '\U0001f31f': '[星]',
            '\U0001f525': '[火]', '\U0001f680': '[火箭]', '\U0001f4a1': '[灯泡]',
        }
        for emoji, replacement in emoji_map.items():
            text = text.replace(emoji, replacement)
        super().write(text)

sys.stdout = EmojiStripper(sys.stdout.buffer, encoding='utf-8')

def publish_note(title, content, images, tags=None):
    try:
        payload = {
            "title": title,
            "content": content,
            "images": images if isinstance(images, list) else [images]
        }
        if tags:
            payload["tags"] = tags if isinstance(tags, list) else [tags]
        
        print(f"Publishing note: {title}")
        print(f"Content length: {len(content)} chars")
        print(f"Images: {len(images)} image(s)")
        
        resp = requests.post(
            "http://localhost:18060/api/v1/publish",
            json=payload,
            timeout=120
        )
        data = resp.json()
        
        print(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if data.get("success"):
            post_id = data.get("data", {}).get("post_id", "Unknown")
            print(f"[OK] Published successfully! Post ID: {post_id}")
            return {"success": True, "post_id": post_id}
        else:
            print(f"[X] Publish failed: {data.get('error')}")
            return {"success": False, "error": data.get('error')}
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # 标题 (需在30字以内)
    title = "西安边家村 | 教室出租，配套齐全"
    
    # 正文
    content = """📍 边家村 · 教室共享

我们是一间教育工作室，现有两间教室因业务调整，对外开放共享啦！

🏠 场地详情：

大教室（15-20人）：中小型会议、团队培训、讲座沙龙、自习室
小教室（6-7人）：一对一辅导、小班教学、商务洽谈、兴趣小组

📍 位置：边家村（地铁口附近）

✨ 配套齐全：
一体机（可投屏/展示）、白板、空调暖气、安静独立空间

💰 价格：根据使用时长和频率灵活计费，欢迎私信了解～

⚠️ 免责声明：本场地仅提供空间使用，不涉及任何课程辅导、培训等服务。"""
    
    # 图片路径 - 使用用户提供的图片
    images = [
        "C:/Users/LWS/.openclaw/media/inbound/86e7fdef-11fe-4d1c-acfd-b918d34e59d3.jpg",
        "C:/Users/LWS/.openclaw/media/inbound/95ff5eb9-530a-45d6-b6a6-a28902c6be0a.jpg"
    ]
    
    # 标签
    tags = ["西安教室出租", "西安共享空间", "边家村", "自习室", "会议室出租", "西安创业", "副业", "场地共享"]
    
    result = publish_note(title, content, images, tags)
    
    # 保存结果
    with open("publish_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
