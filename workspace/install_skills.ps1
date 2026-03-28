# 批量安装技能脚本
$Skills = @(
    "skill-creator",
    "model-usage", 
    "free-ride",
    "copywriting",
    "social-content",
    "product-marketing-context",
    "ui-ux-pro-max",
    "diagram-generator",
    "humanizer",
    "openai-whisper",
    "youtube-watcher",
    "slack",
    "api-gateway",
    "mcporter",
    "n8n",
    "playwright-scraper",
    "weather"
)

$Workspace = "$env:USERPROFILE\.openclaw\workspace"
$SkillsDir = "$Workspace\skills"

# 确保目录存在
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

# 安装每个技能
foreach ($Skill in $Skills) {
    Write-Host "Installing $Skill..." -ForegroundColor Yellow
    try {
        clawhub install $Skill
        Write-Host "✅ $Skill installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install $Skill : $_" -ForegroundColor Red
    }
}

Write-Host "Installation complete!" -ForegroundColor Cyan