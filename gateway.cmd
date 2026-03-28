@echo off
rem OpenClaw Gateway (v2026.3.24)
set "TAVILY_API_KEY=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"
set "TMPDIR=C:\Users\LWS\AppData\Local\Temp"
set "OPENCLAW_GATEWAY_PORT=18789"
set "OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service"
set "OPENCLAW_WINDOWS_TASK_NAME=OpenClaw Gateway"
set "OPENCLAW_SERVICE_MARKER=openclaw"
set "OPENCLAW_SERVICE_KIND=gateway"
set "OPENCLAW_SERVICE_VERSION=2026.3.24"
D:\intall\Node\node.exe C:\Users\LWS\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789
