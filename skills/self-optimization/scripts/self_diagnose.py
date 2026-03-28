#!/usr/bin/env python3
"""
自我诊断脚本：检查系统状态和工具可用性
"""
import os
import sys
import subprocess
import json
from datetime import datetime

REPORT_PATH = "~/.openclaw/workspace/memory/diagnose_report.json"

def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def check_tools():
    """检查常用工具是否可用"""
    tools = [
        {"name": "node", "cmd": "node --version", "description": "Node.js 运行环境"},
        {"name": "npm", "cmd": "npm --version", "description": "Node 包管理器"},
        {"name": "git", "cmd": "git --version", "description": "Git 版本控制"},
        {"name": "python", "cmd": "python --version || python3 --version", "description": "Python 运行环境"},
        {"name": "clawhub", "cmd": "clawhub --version", "description": "ClawHub 技能管理器"},
    ]
    
    results = []
    for tool in tools:
        print(f"检查 {tool['name']}...")
        result = run_command(tool["cmd"])
        results.append({
            "name": tool["name"],
            "description": tool["description"],
            "available": result["success"],
            "version": result["stdout"] if result["success"] else None,
            "error": result["stderr"] if not result["success"] else result.get("error")
        })
    
    return results

def check_files():
    """检查核心文件是否存在"""
    required_files = [
        "~/.openclaw/workspace/SOUL.md",
        "~/.openclaw/workspace/USER.md",
        "~/.openclaw/workspace/MEMORY.md",
        "~/.openclaw/workspace/AGENTS.md",
        "~/.openclaw/workspace/TOOLS.md",
    ]
    
    results = []
    for file_path in required_files:
        full_path = os.path.expanduser(file_path)
        exists = os.path.exists(full_path)
        results.append({
            "path": file_path,
            "exists": exists,
            "size": os.path.getsize(full_path) if exists else 0
        })
    
    return results

def check_permissions():
    """检查关键目录权限"""
    directories = [
        "~/.openclaw/workspace",
        "~/.openclaw/skills",
        "~/.openclaw/extensions",
        "/tmp/openclaw",
    ]
    
    results = []
    for dir_path in directories:
        full_path = os.path.expanduser(dir_path)
        exists = os.path.exists(full_path)
        writable = os.access(full_path, os.W_OK) if exists else False
        results.append({
            "path": dir_path,
            "exists": exists,
            "writable": writable
        })
    
    return results

def generate_report():
    """生成诊断报告"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "tools": check_tools(),
        "files": check_files(),
        "permissions": check_permissions(),
        "summary": {
            "total_issues": 0,
            "critical_issues": 0,
            "warning_issues": 0
        }
    }
    
    # 统计问题
    issues = []
    
    # 检查工具问题
    for tool in report["tools"]:
        if not tool["available"]:
            if tool["name"] in ["node", "python", "git"]:
                issues.append({"type": "critical", "message": f"核心工具 {tool['name']} 不可用"})
                report["summary"]["critical_issues"] += 1
            else:
                issues.append({"type": "warning", "message": f"工具 {tool['name']} 不可用"})
                report["summary"]["warning_issues"] += 1
    
    # 检查文件问题
    for file in report["files"]:
        if not file["exists"]:
            issues.append({"type": "warning", "message": f"核心文件 {file['path']} 不存在"})
            report["summary"]["warning_issues"] += 1
    
    # 检查权限问题
    for perm in report["permissions"]:
        if not perm["exists"]:
            issues.append({"type": "warning", "message": f"目录 {perm['path']} 不存在"})
            report["summary"]["warning_issues"] += 1
        elif not perm["writable"]:
            issues.append({"type": "critical", "message": f"目录 {perm['path']} 不可写"})
            report["summary"]["critical_issues"] += 1
    
    report["issues"] = issues
    report["summary"]["total_issues"] = len(issues)
    
    # 保存报告
    os.makedirs(os.path.dirname(os.path.expanduser(REPORT_PATH)), exist_ok=True)
    with open(os.path.expanduser(REPORT_PATH), 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    return report

def print_report(report):
    """打印诊断报告"""
    print("\n" + "="*50)
    print("🤖 自我诊断报告 " + report["timestamp"])
    print("="*50)
    
    print(f"\n📊 问题统计：")
    print(f"   总问题数：{report['summary']['total_issues']}")
    print(f"   严重问题：{report['summary']['critical_issues']}")
    print(f"   警告问题：{report['summary']['warning_issues']}")
    
    if report["issues"]:
        print("\n❌ 发现的问题：")
        for i, issue in enumerate(report["issues"], 1):
            icon = "🔴" if issue["type"] == "critical" else "🟡"
            print(f"   {i}. {icon} {issue['message']}")
    else:
        print("\n✅ 系统状态良好，未发现问题！")
    
    print("\n" + "="*50)

def main():
    """主函数"""
    print("开始自我诊断...")
    report = generate_report()
    print_report(report)
    
    # 如果有严重问题，返回非0退出码
    if report["summary"]["critical_issues"] > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
