# -*- coding: utf-8 -*-
import requests
import json
import sys

# Force UTF-8 output
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def search_notes(keyword):
    try:
        payload = {
            "keyword": keyword,
            "filters": {
                "sort_by": "综合",
                "note_type": "不限",
                "publish_time": "不限"
            }
        }
        resp = requests.post(
            "http://localhost:18060/api/v1/feeds/search",
            json=payload,
            timeout=60
        )
        data = resp.json()
        
        if data.get("success"):
            feeds = data.get("data", {}).get("feeds", [])
            print(f"Found {len(feeds)} notes:")
            
            results = []
            for i, feed in enumerate(feeds[:10], 1):
                note_card = feed.get("noteCard", {})
                user = note_card.get("user", {})
                interact = note_card.get("interactInfo", {})
                
                title = note_card.get('displayTitle', 'No title')
                author = user.get('nickname', 'Unknown')
                likes = interact.get('likedCount', '0')
                feed_id = feed.get('id')
                
                results.append({
                    'index': i,
                    'title': title,
                    'author': author,
                    'likes': likes,
                    'feed_id': feed_id
                })
            
            # Output as JSON for easy parsing
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"error": data.get('error')}))
        
        return data
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    search_notes("西安教室出租")
