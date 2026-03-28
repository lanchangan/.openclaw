@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo   小红书私信自动回复监控
echo ========================================
echo.
echo 启动中...
python xhs_monitor.py
pause
