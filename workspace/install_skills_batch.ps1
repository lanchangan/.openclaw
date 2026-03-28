# 智能批量安装技能脚本
# 自动处理 ClawHub API 速率限制

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

$Success = @()
$Failed = @()
$RateLimited = @()

foreach ($Skill in $Skills) {
    Write-Host "`n[$($Success.Count + $Failed.Count + 1)/$($Skills.Count)] Installing $Skill..." -ForegroundColor Cyan
    
    try {
        $Output = clawhub install $Skill 2>&1
        $ExitCode = $LASTEXITCODE
        
        if ($Output -match "Rate limit exceeded") {
            Write-Host "  ⚠️ Rate limited. Waiting 30 seconds..." -ForegroundColor Yellow
            $RateLimited += $Skill
            Start-Sleep -Seconds 30
            
            # 重试一次
            $Output = clawhub install $Skill 2>&1
            if ($Output -match "Installed|already installed") {
                Write-Host "  ✅ Retry successful!" -ForegroundColor Green
                $Success += $Skill
            } else {
                $Failed += $Skill
            }
        }
        elseif ($Output -match "Installed|already installed") {
            Write-Host "  ✅ Success!" -ForegroundColor Green
            $Success += $Skill
        }
        else {
            Write-Host "  ❌ Failed: $Output" -ForegroundColor Red
            $Failed += $Skill
        }
    }
    catch {
        Write-Host "  ❌ Error: $_" -ForegroundColor Red
        $Failed += $Skill
    }
    
    # 每次安装后短暂延时，避免触发限制
    Start-Sleep -Seconds 2
}

# 输出总结
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "安装完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ 成功: $($Success.Count)" -ForegroundColor Green
$Success | ForEach-Object { Write-Host "   - $_" }

if ($Failed.Count -gt 0) {
    Write-Host "`n❌ 失败: $($Failed.Count)" -ForegroundColor Red
    $Failed | ForEach-Object { Write-Host "   - $_" }
}

if ($RateLimited.Count -gt 0) {
    Write-Host "`n⚠️ 曾触发速率限制: $($RateLimited.Count)" -ForegroundColor Yellow
    $RateLimited | ForEach-Object { Write-Host "   - $_" }
}

Write-Host "`n========================================" -ForegroundColor Cyan