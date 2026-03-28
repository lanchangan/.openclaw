# 创建技能目录
$skillDir = "$env:USERPROFILE\.openclaw\skills"
New-Item -ItemType Directory -Force -Path $skillDir | Out-Null

# 克隆仓库
$targetDir = "$skillDir\multi-search-engine"
if (Test-Path $targetDir) {
    Write-Host "技能已存在，正在更新..."
    Set-Location $targetDir
    git pull
} else {
    Write-Host "正在克隆 multi-search-engine 技能..."
    git clone https://github.com/openclaw-hub/multi-search-engine.git $targetDir
}

Write-Host "安装完成！"
