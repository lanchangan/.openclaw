# QQ Download Script
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "       QQ Downloader" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

$urls = @(
    "https://dldir1.qq.com/qqfile/qq/PCQQ9.9.16/QQ9.9.16.241023.exe",
    "https://dldir1.qq.com/qqfile/qq/PCQQ9.9.15/QQ9.9.15.27597.exe",
    "https://dldir1.qq.com/qqfile/qq/PCQQ9.9.12/QQ9.9.12.22771.exe"
)

$output = "$env:TEMP\QQ_Installer.exe"
$success = $false

foreach ($url in $urls) {
    Write-Host "Downloading: $url" -ForegroundColor Yellow
    try {
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing -TimeoutSec 30
        
        if ((Test-Path $output) -and ((Get-Item $output).Length -gt 1MB)) {
            $size = [math]::Round((Get-Item $output).Length/1MB, 2)
            Write-Host "Success! Size: $size MB" -ForegroundColor Green
            $success = $true
            break
        }
    } catch {
        Write-Host "Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

if ($success) {
    Write-Host "`nInstaller saved to: $output" -ForegroundColor Green
    Write-Host "Starting installer..." -ForegroundColor Yellow
    Start-Process -FilePath $output
} else {
    Write-Host "`nAll downloads failed." -ForegroundColor Red
    Write-Host "Visit: https://im.qq.com/pcqq/index.shtml" -ForegroundColor Yellow
}
