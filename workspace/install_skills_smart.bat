@echo off
chcp 65001 >nul
echo ========================================
echo Smart Skill Installation
echo ClawHub API Rate Limit Handler
echo ========================================
echo.

set SKILLS=skill-creator model-usage free-ride copywriting social-content product-marketing-context ui-ux-pro-max diagram-generator humanizer openai-whisper youtube-watcher slack api-gateway mcporter n8n playwright-scraper weather

set DELAY=3
set RETRY_DELAY=30
set COUNT=0

for %%S in (%SKILLS%) do (
    set /a COUNT+=1
    echo.
    echo [%COUNT%/17] Installing: %%S
    echo ----------------------------------------
    
    clawhub install %%S
    
    if %ERRORLEVEL% equ 0 (
        echo [OK] %%S installed successfully
    ) else (
        echo [RATE LIMIT] Waiting %RETRY_DELAY% seconds...
        timeout /t %RETRY_DELAY% /nobreak >nul
        
        clawhub install %%S
        if %ERRORLEVEL% equ 0 (
            echo [OK] %%S installed on retry
        ) else (
            echo [FAIL] %%S installation failed
        )
    )
    
    echo Waiting %DELAY% seconds before next...
    timeout /t %DELAY% /nobreak >nul
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
pause