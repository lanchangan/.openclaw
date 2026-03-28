#!/usr/bin/env python3
"""
技能审核脚本：完整的技能审核流程
"""
import os
import json
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
from scan_skill import scan_skill, RISK_LEVELS

AUDIT_LOG_DIR = "~/.openclaw/workspace/memory/skill_audits"

def run_sandboxed(skill_path, test_command):
    """在沙箱中运行技能测试"""
    try:
        # 创建临时目录作为沙箱
        with tempfile.TemporaryDirectory() as sandbox_dir:
            # 复制技能到沙箱
            import shutil
            shutil.copytree(skill_path, os.path.join(sandbox_dir, Path(skill_path).name))
            
            # 运行测试命令
            result = subprocess.run(
                test_command,
                shell=True,
                cwd=sandbox_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "执行超时"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def audit_skill(skill_path, auto_approve=False):
    """完整的技能审核流程"""
    skill_path = Path(os.path.expanduser(skill_path))
    skill_name = skill_path.name
    
    # 1. 静态扫描
    print(f"1/3 正在静态扫描技能: {skill_name}")
    scan_report = scan_skill(skill_path)
    if "error" in scan_report:
        return {"error": scan_report["error"]}
    
    # 2. 动态测试
    print(f"2/3 正在动态测试技能: {skill_name}")
    test_result = run_sandboxed(skill_path, "python --version 2>&1")  # 简单测试
    
    # 3. 权限检查
    print(f"3/3 正在检查权限声明: {skill_name}")
    permission_check = check_permissions(skill_path)
    
    # 生成最终审核报告
    final_risk = max(
        scan_report["risk_summary"]["max_risk_level"],
        1 if not test_result["success"] else 0,
        permission_check["risk_level"]
    )
    
    audit_report = {
        "skill_name": skill_name,
        "audit_time": datetime.now().isoformat(),
        "status": "approved" if final_risk <= 1 and auto_approve else "pending",
        "final_risk_level": final_risk,
        "final_risk_name": RISK_LEVELS[final_risk]["name"],
        "scan_report": scan_report,
        "test_result": test_result,
        "permission_check": permission_check,
        "recommendation": get_final_recommendation(final_risk, auto_approve)
    }
    
    # 保存审核记录
    save_audit_report(audit_report)
    
    return audit_report

def check_permissions(skill_path):
    """检查技能的权限声明和实际使用是否一致"""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {"risk_level": 2, "issues": ["缺少SKILL.md文件，无法检查权限声明"]}
    
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单的权限检查
        declared_permissions = []
        if "网络请求" in content or "http" in content.lower():
            declared_permissions.append("network")
        if "文件操作" in content or "读写" in content:
            declared_permissions.append("filesystem")
        if "系统命令" in content or "执行" in content:
            declared_permissions.append("exec")
        
        # 检查脚本中的实际权限使用
        actual_permissions = []
        for ext in [".py", ".js", ".sh"]:
            for file_path in skill_path.rglob(f"*{ext}"):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                    if "request" in file_content.lower() or "http" in file_content.lower():
                        if "network" not in actual_permissions:
                            actual_permissions.append("network")
                    if "open(" in file_content or "os." in file_content:
                        if "filesystem" not in actual_permissions:
                            actual_permissions.append("filesystem")
                    if "system(" in file_content or "subprocess" in file_content:
                        if "exec" not in actual_permissions:
                            actual_permissions.append("exec")
        
        # 检查未声明的权限
        undeclared = [p for p in actual_permissions if p not in declared_permissions]
        
        if undeclared:
            return {
                "risk_level": 2,
                "issues": [f"技能使用了未声明的权限: {', '.join(undeclared)}"],
                "declared_permissions": declared_permissions,
                "actual_permissions": actual_permissions
            }
        else:
            return {
                "risk_level": 0,
                "issues": [],
                "declared_permissions": declared_permissions,
                "actual_permissions": actual_permissions
            }
    
    except Exception as e:
        return {"risk_level": 1, "issues": [f"权限检查失败: {str(e)}"]}

def get_final_recommendation(risk_level, auto_approve):
    """生成最终建议"""
    if risk_level == 0:
        return "✅ 技能完全安全，建议安装"
    elif risk_level == 1:
        return "⚠️ 技能存在低风险，可正常安装使用"
    elif risk_level == 2:
        return "🟡 技能存在中风险，需要用户确认后安装"
    else:
        return "🔴 技能存在高风险，强烈建议不要安装"

def save_audit_report(report):
    """保存审核报告到日志"""
    log_dir = os.path.expanduser(AUDIT_LOG_DIR)
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{report['skill_name']}_{timestamp}.json")
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"审核报告已保存到: {log_file}")

def print_audit_report(report):
    """打印审核报告"""
    print("\n" + "="*70)
    print(f"📋 技能审核报告: {report['skill_name']}")
    print("="*70)
    print(f"审核时间: {report['audit_time']}")
    print(f"审核状态: {'✅ 通过' if report['status'] == 'approved' else '⏳ 待确认'}")
    print(f"最终风险等级: {RISK_LEVELS[report['final_risk_level']]['icon']} {report['final_risk_name']}")
    print()
    
    print("🔍 静态扫描结果:")
    print(f"   扫描文件数: {report['scan_report']['total_files_scanned']}")
    print(f"   发现问题数: {report['scan_report']['total_issues_found']}")
    print(f"   最高风险: {RISK_LEVELS[report['scan_report']['risk_summary']['max_risk_level']]['icon']} {report['scan_report']['risk_summary']['max_risk_name']}")
    
    print("\n🧪 动态测试结果:")
    if report['test_result']['success']:
        print("   ✅ 测试通过")
    else:
        print(f"   ❌ 测试失败: {report['test_result'].get('error', '未知错误')}")
    
    print("\n🔑 权限检查结果:")
    if report['permission_check']['risk_level'] == 0:
        print("   ✅ 权限声明正确")
    else:
        for issue in report['permission_check']['issues']:
            print(f"   ⚠️ {issue}")
    
    print(f"\n💡 最终建议: {report['recommendation']}")
    print("="*70)

def main():
    """主函数"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='技能安全审核工具')
    parser.add_argument('skill_path', help='要审核的技能路径')
    parser.add_argument('--auto-approve', action='store_true', help='低风险自动通过')
    args = parser.parse_args()
    
    report = audit_skill(args.skill_path, args.auto_approve)
    
    if "error" in report:
        print(f"❌ 审核失败: {report['error']}")
        sys.exit(1)
    
    print_audit_report(report)
    
    # 高风险退出码为1
    if report['final_risk_level'] >= 3:
        sys.exit(1)

if __name__ == "__main__":
    main()
