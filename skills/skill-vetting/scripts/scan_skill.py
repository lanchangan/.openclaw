#!/usr/bin/env python3
"""
技能安全扫描脚本：扫描指定技能的安全风险
"""
import os
import re
import json
from pathlib import Path
from datetime import datetime

# 恶意代码特征库
MALICIOUS_PATTERNS = [
    # 网络请求相关
    r'requests\.post\s*\(\s*["\']https?://',
    r'urllib\.request\.urlopen',
    r'socket\.connect',
    # 文件操作相关
    r'open\s*\(\s*["\']/etc/passwd',
    r'open\s*\(\s*["\']/etc/shadow',
    r'os\.remove\s*\(\s*["\']/\.',
    r'shutil\.rmtree',
    # 系统命令相关
    r'os\.system\s*\(',
    r'subprocess\.call\s*\(',
    r'subprocess\.Popen\s*\(',
    r'exec\s*\(',
    r'eval\s*\(',
    # 敏感信息相关
    r'password\s*=\s*["\'][^"\']+["\']',
    r'api_key\s*=\s*["\'][^"\']+["\']',
    r'token\s*=\s*["\'][^"\']+["\']',
    r'secret\s*=\s*["\'][^"\']+["\']',
    # 恶意行为
    r'fork\s*\(',
    r'daemon\s*\(',
    r'cryptocurrency|miner|bitcoin',
    r'ransomware|encrypt',
]

# 风险等级定义
RISK_LEVELS = {
    0: {"name": "安全", "color": "green", "icon": "✅"},
    1: {"name": "低风险", "color": "yellow", "icon": "⚠️"},
    2: {"name": "中风险", "color": "orange", "icon": "🟡"},
    3: {"name": "高风险", "color": "red", "icon": "🔴"},
}

def scan_file(file_path):
    """扫描单个文件的恶意代码"""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        for pattern in MALICIOUS_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content.count('\n', 0, match.start()) + 1
                issues.append({
                    "file": str(file_path),
                    "line": line_num,
                    "pattern": pattern,
                    "match": match.group(),
                    "risk_level": 2 if "system" in pattern or "subprocess" in pattern or "eval" in pattern else 1
                })
        
        return issues
    except Exception as e:
        return [{"file": str(file_path), "error": f"无法读取文件: {str(e)}", "risk_level": 1}]

def scan_skill(skill_path):
    """扫描整个技能目录"""
    skill_path = Path(os.path.expanduser(skill_path))
    if not skill_path.exists():
        return {"error": "技能目录不存在"}
    
    # 检查SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {"error": "无效的技能：缺少SKILL.md文件"}
    
    # 扫描所有文件
    all_issues = []
    total_files = 0
    
    for ext in [".py", ".js", ".sh", ".bash", ".cmd", ".bat", ".ps1"]:
        for file_path in skill_path.rglob(f"*{ext}"):
            total_files += 1
            issues = scan_file(file_path)
            all_issues.extend(issues)
    
    # 计算风险等级
    max_risk = 0
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0
    
    for issue in all_issues:
        risk_level = issue.get("risk_level", 0)
        if risk_level > max_risk:
            max_risk = risk_level
        if risk_level == 3:
            high_risk_count += 1
        elif risk_level == 2:
            medium_risk_count += 1
        elif risk_level == 1:
            low_risk_count += 1
    
    # 生成报告
    report = {
        "skill_name": skill_path.name,
        "scan_time": datetime.now().isoformat(),
        "total_files_scanned": total_files,
        "total_issues_found": len(all_issues),
        "risk_summary": {
            "max_risk_level": max_risk,
            "max_risk_name": RISK_LEVELS[max_risk]["name"],
            "high_risk_count": high_risk_count,
            "medium_risk_count": medium_risk_count,
            "low_risk_count": low_risk_count,
        },
        "issues": all_issues,
        "recommendation": get_recommendation(max_risk, len(all_issues))
    }
    
    return report

def get_recommendation(risk_level, issue_count):
    """根据风险等级给出建议"""
    if risk_level == 0:
        return "✅ 技能安全，可以正常安装使用"
    elif risk_level == 1:
        return "⚠️ 存在低风险问题，建议检查后安装"
    elif risk_level == 2:
        return "🟡 存在中风险问题，需要确认后再安装"
    else:
        return "🔴 存在高风险问题，建议不要安装"

def print_report(report):
    """打印扫描报告"""
    print("\n" + "="*70)
    print(f"🔍 技能安全扫描报告: {report['skill_name']}")
    print("="*70)
    print(f"扫描时间: {report['scan_time']}")
    print(f"扫描文件数: {report['total_files_scanned']}")
    print(f"发现问题数: {report['total_issues_found']}")
    print()
    
    summary = report['risk_summary']
    print(f"最高风险等级: {RISK_LEVELS[summary['max_risk_level']]['icon']} {summary['max_risk_name']}")
    print(f"高风险问题: {summary['high_risk_count']} 个")
    print(f"中风险问题: {summary['medium_risk_count']} 个")
    print(f"低风险问题: {summary['low_risk_count']} 个")
    print()
    
    if report['issues']:
        print("发现的问题:")
        for i, issue in enumerate(report['issues'], 1):
            risk_icon = RISK_LEVELS[issue.get('risk_level', 1)]['icon']
            print(f"\n{i}. {risk_icon} 文件: {issue.get('file', '未知')}")
            if 'line' in issue:
                print(f"   行号: {issue['line']}")
            if 'match' in issue:
                print(f"   匹配: {issue['match'][:50]}...")
            if 'error' in issue:
                print(f"   错误: {issue['error']}")
    
    print(f"\n💡 建议: {report['recommendation']}")
    print("="*70)

def main():
    """主函数"""
    import sys
    if len(sys.argv) != 2:
        print("用法: python scan_skill.py <技能路径>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    report = scan_skill(skill_path)
    
    if "error" in report:
        print(f"❌ 扫描失败: {report['error']}")
        sys.exit(1)
    
    print_report(report)
    
    # 高风险退出码为1
    if report['risk_summary']['max_risk_level'] >= 3:
        sys.exit(1)

if __name__ == "__main__":
    main()
