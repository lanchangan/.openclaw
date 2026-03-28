# 设置目录
$Workspace = "$env:USERPROFILE\.openclaw\workspace"
$SkillsDir = "$Workspace\skills"
$TargetDir = "$SkillsDir\multi-search-engine"

# 清理旧版本
if (Test-Path $TargetDir) {
    Remove-Item -Recurse -Force $TargetDir
    Write-Host "已清除旧版本"
}

# 确保目录存在
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

# 克隆仓库
Set-Location $SkillsDir
git clone https://github.com/openclaw-hub/multi-search-engine.git

if (Test-Path $TargetDir\SKILL.md) {
    Write-Host "安装成功！"
    Get-ChildItem $TargetDir
} else {
    Write-Host "安装失败"
}