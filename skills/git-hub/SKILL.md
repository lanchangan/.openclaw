---
name: git-hub
description: GitHub集成工具，支持仓库管理、Issue处理、PR审查、发布管理、通知监控等功能。帮助开发者更高效地使用GitHub进行协作开发。当需要操作GitHub仓库、处理Issue、PR时使用。
---

# GitHub 集成技能

## 核心功能
### 📁 仓库管理
- **仓库操作**：创建、删除、 Fork、Star仓库
- **分支管理**：创建、删除、合并分支，查看分支列表
- **标签管理**：创建、删除标签，管理版本发布
- **权限管理**：管理仓库协作者和权限设置

### 🐛 Issue处理
- **Issue创建**：创建新的Issue，支持模板和标签
- **Issue管理**：编辑、关闭、分配Issue，添加标签和里程碑
- **Issue搜索**：按条件搜索和筛选Issue
- **评论管理**：添加、编辑、删除Issue评论

### 🔄 PR审查
- **PR创建**：创建Pull Request，支持模板
- **代码审查**：查看PR变更，添加行评论和全局评论
- **PR管理**：合并、关闭、重新打开PR，添加审查者
- **CI状态**：查看CI运行状态和测试结果

### 🚀 发布管理
- **版本发布**：创建新版本发布，上传附件
- **变更日志**：自动生成变更日志
- **预发布**：管理预发布版本和草稿版本
- **下载统计**：查看版本下载量和统计数据

### 🔔 通知监控
- **通知管理**：查看和标记通知为已读
- **活动监控**：监控仓库的活动和事件
- **Webhook**：管理仓库Webhook配置
- **告警设置**：自定义通知规则和告警方式

## 使用示例
### 创建Issue
```python
github.create_issue(
    repo="owner/repo",
    title="Bug: 登录页面崩溃",
    body="### 问题描述\n登录时点击提交按钮页面崩溃",
    labels=["bug", "priority:high"],
    assignee="username"
)
```

### 审查PR
```python
pr = github.get_pr("owner/repo", 123)
print(f"PR标题: {pr.title}")
print(f"变更文件数: {pr.changed_files}")
print(f"新增代码: {pr.additions} 行")

# 添加评论
github.add_pr_comment("owner/repo", 123, "这里逻辑有问题，需要修改")

# 合并PR
github.merge_pr("owner/repo", 123, merge_method="squash")
```

### 创建发布
```python
github.create_release(
    repo="owner/repo",
    tag_name="v1.0.0",
    name="Version 1.0.0",
    body="## 新功能\n- 支持用户登录\n- 新增数据导出功能",
    prerelease=False,
    draft=False
)
```

## 配置方法
在配置文件中添加GitHub Token：
```yaml
github:
  token: "your-github-personal-access-token"
  username: "your-github-username"
  default_org: "your-org-name"
```

## 触发场景
- 需要操作GitHub仓库（创建、Fork、Star等）
- 处理Issue（创建、分配、关闭等）
- 审查和合并Pull Request
- 管理版本发布和变更日志
- 监控GitHub通知和活动
