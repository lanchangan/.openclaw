# -*- coding: utf-8 -*-
import requests
import json
import sys
import io

# Create a custom writer that replaces emojis with text
class EmojiStripper(io.TextIOWrapper):
    def write(self, text):
        # Replace common emojis with text markers
        emoji_map = {
            '\U0001f308': '[彩虹]',
            '\U0001f50d': '[搜索]',
            '\u2705': '[OK]',
            '\u274c': '[X]',
            '\U0001f4e6': '[包裹]',
            '\U0001f4e9': '[信]',
            '\U0001f3eb': '[麦克风]',
            '\U0001f4ac': '[评论]',
            '\u2764': '[心]',
            '\U0001f49c': '[心]',
            '\u2b50': '[星]',
            '\U0001f31f': '[星]',
            '\U0001f525': '[火]',
            '\U0001f680': '[火箭]',
            '\U0001f4a1': '[灯泡]',
            '\U0001f4cb': '[剪贴板]',
            '\U0001f4d6': '[书]',
            '\U0001f3e0': '[家]',
            '\U0001f3af': '[靶心]',
            '\U0001f517': '[链接]',
            '\U0001f534': '[蓝圆]',
            '\U0001f535': '[蓝圆]',
            '\u25b6': '[播放]',
            '\U0001f539': '[紫星]',
            '\U0001f536': '[绿星]',
            '\U0001f537': '[橙星]',
            '\U0001f538': '[黄星]',
            '\U0001f539': '[粉星]',
        }
        for emoji, replacement in emoji_map.items():
            text = text.replace(emoji, replacement)
        super().write(text)

# Redirect stdout
sys.stdout = EmojiStripper(sys.stdout.buffer, encoding='utf-8')

def search_and_save(keyword, sort_by="综合", output_file="search_results.json"):
    try:
        payload = {
            "keyword": keyword,
            "filters": {
                "sort_by": sort_by,
                "note_type": "不限",
                "publish_time": "不限"
            }
        }
        resp = requests.post(
            "http://localhost:18060/api/v1/feeds/search",
            json=payload,
            timeout=90
        )
        data = resp.json()
        
        if data.get("success"):
            feeds = data.get("data", {}).get("feeds", [])
            print(f"Found {len(feeds)} notes for keyword: {keyword}")
            
            results = []
            for i, feed in enumerate(feeds, 1):
                note_card = feed.get("noteCard", {})
                user = note_card.get("user", {})
                interact = note_card.get("interactInfo", {})
                
                results.append({
                    'index': i,
                    'title': note_card.get('displayTitle', ''),
                    'author': user.get('nickname', ''),
                    'likes': interact.get('likedCount', ''),
                    'feed_id': feed.get('id'),
                    'xsec_token': feed.get('xsecToken', ''),
                    'type': note_card.get('type', ''),
                    'cover_url': note_card.get('cover', {}).get('urlDefault', '')
                })
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'keyword': keyword,
                    'count': len(results),
                    'notes': results
                }, f, ensure_ascii=False, indent=2)
            
            print(f"Results saved to {output_file}")
            return results
        else:
            print(f"Search failed: {data.get('error')}")
            return []
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "西安教室出租"
    search_and_save(keyword)
