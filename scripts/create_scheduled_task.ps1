# 创建OpenClaw共享记忆同步定时任务
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File 'C:\Users\LWS\.openclaw\scripts\sync_shared_memory.ps1'"
$trigger = New-ScheduledTaskTrigger -AtStartup -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration ([timespan]::MaxValue)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable:$false
$principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "OpenClaw共享记忆自动同步" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "每5分钟同步主工作区MEMORY.md到所有Agent共享记忆" -Force

Write-Host "定时任务创建成功！将在系统启动后每5分钟自动运行一次同步脚本。"
