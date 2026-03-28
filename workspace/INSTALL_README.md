# Skill Installation Guide

## Current Status

### ✅ Already Installed (2/19)
1. `multi-search-engine` - Multi-engine web search
2. `web-search-exa` - Neural web search by Exa

### ⏳ Pending Installation (17 skills)
- skill-creator
- model-usage
- free-ride
- copywriting
- social-content
- product-marketing-context
- ui-ux-pro-max
- diagram-generator
- humanizer
- openai-whisper
- youtube-watcher
- slack
- api-gateway
- mcporter
- n8n
- playwright-scraper
- weather

## Installation Options

### Option 1: Automatic Retry (Recommended)
Run the smart installer that handles rate limits automatically:
```batch
install_skills_smart.bat
```

### Option 2: Manual Installation
Wait 2-3 minutes for rate limit to reset, then:
```bash
# Install one by one with delays
clawhub install skill-creator
# wait 5 seconds
clawhub install model-usage
# ... continue
```

### Option 3: Off-Peak Installation
Install during off-peak hours when API usage is lower:
- Late night (11 PM - 6 AM)
- Early morning weekdays

## Rate Limit Information

- **Limit**: 120 requests per minute
- **Current Issue**: Rate limit exceeded
- **Reset Time**: Usually 1-2 minutes
- **Strategy**: Batch with delays

## Troubleshooting

### If installation keeps failing:
1. Check internet connection
2. Verify GitHub access: `ping github.com`
3. Try using VPN if in restricted region
4. Check Windows Defender/Firewall settings

### If rate limit persists:
1. Wait 5 minutes and retry
2. Install in smaller batches (3-5 at a time)
3. Use `--force` flag if needed: `clawhub install skill-name --force`

## Contact & Support

- ClawHub Issues: https://github.com/openclaw/clawhub/issues
- OpenClaw Discord: https://discord.com/invite/clawd
- Documentation: https://docs.openclaw.ai

---
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")