---
name: find-skills
description: ClawHub技能搜索和发现工具，支持搜索、筛选、发现适合的技能。支持按功能、分类、评分、下载量筛选，提供技能详情、使用说明、安装指引。当用户需要找某个功能的技能、探索新技能时使用。
---

# Find Skills 技能搜索工具

## 核心功能
- 🔍 **技能搜索**：按关键词搜索ClawHub上的所有公开技能
- 📊 **筛选功能**：按分类、评分、下载量、更新时间筛选技能
- 📝 **技能详情**：查看技能的完整描述、功能说明、使用方法
- ⭐ **评分系统**：查看其他用户对技能的评分和评价
- 📈 **热门推荐**：推荐热门、高评分、新上线的技能
- 📦 **一键安装**：直接安装选中的技能，自动解决依赖

## 搜索语法
- 普通关键词搜索：`find-skills "web search"`
- 按分类搜索：`find-skills category:productivity`
- 按评分筛选：`find-skills "AI" rating:>4.5`
- 按下载量筛选：`find-skills "git" downloads:>1000`
- 组合搜索：`find-skills "frontend" category:development rating:>4.0`

## 使用示例
```python
# 搜索技能
results = search_skills("tavily search", category="tools", rating_min=4.0)
for skill in results:
    print(f"{skill['name']} - {skill['description']}")
    print(f"评分: {skill['rating']} ⭐ 下载量: {skill['downloads']}")

# 安装技能
install_skill("tavily-search")
```

## 触发场景
- 用户需要查找具有特定功能的技能
- 想要探索新的技能，扩展功能
- 寻找热门、高评分的优质技能
- 需要了解某个技能的详细信息和使用方法
- 比较多个同类技能的优缺点，选择最合适的
