# Multi-Agent shared memory sync script
# Sync content from main workspace MEMORY.md to global shared memory

$source_path = "C:\Users\LWS\.openclaw\workspace\MEMORY.md"
$target_path = "C:\Users\LWS\.openclaw\memory\shared_global_memory.md"

# Read source content
$content = Get-Content $source_path -Raw

# Write to target (hard links auto sync to all agent workspaces)
Set-Content $target_path -Value $content -Encoding UTF8

Write-Host "[$(Get-Date)] Shared memory synced successfully"
