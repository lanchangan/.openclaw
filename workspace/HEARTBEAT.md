# HEARTBEAT.md - 心跳任务配置

> 本文件配置 OpenClaw 的定期心跳任务
> 每小时系统会读取一次此文件，更新任务列表
>
> ⚠️ **重要更新 (2026-03-21):** 以下任务已迁移到 Cron 定时任务系统：
> - ✅ 每日天气推送 → Cron 任务
> - ✅ 每日新闻与市场早报 → Cron 任务  
> - ✅ 装修任务检查 → Cron 任务（周五/周一）
>
> 这些任务不再需要在 HEARTBEAT.md 中配置。

---

## 📋 当前通过 HEARTBEAT 管理的任务

> （暂无 - 所有定期任务已迁移至 Cron 系统）

---

## 📋 已迁移至 Cron 的任务（历史记录）

以下任务已成功转换为 Cron 定时任务，不再需要 HEARTBEAT 处理：

### 1. 🌤️ 每日天气推送 ✅ 已迁移
- **Cron 任务 ID:** `0f91aae7-beb8-4901-bb6e-0a6630d7e169`
- **触发时间:** 每天早上 7:30 (Asia/Shanghai)
- **状态:** ✅ 已启用

### 2. 📰 每日新闻与市场早报 ✅ 已迁移
- **Cron 任务 ID:** `8ecc8a2f-8c0c-47da-b813-78ecc92e2cd5`
- **触发时间:** 每天早上 7:00 (Asia/Shanghai)
- **状态:** ✅ 已启用

### 3. 📝 装修任务检查-周五 ✅ 已迁移
- **Cron 任务 ID:** `91f2a567-eeac-4a4c-bbf9-403f8b03c0d9`
- **触发时间:** 每周五 18:00 (Asia/Shanghai)
- **状态:** ✅ 已启用

### 4. 📝 装修任务检查-周一 ✅ 已迁移
- **Cron 任务 ID:** `cd6f41c7-41a3-4abf-865f-5f01e6beb397`
- **触发时间:** 每周一 08:00 (Asia/Shanghai)
- **状态:** ✅ 已启用

---

## ⚙️ 如何查看和管理 Cron 任务

### 查看所有任务
```bash
openclaw cron list
```

### 查看任务执行历史
```bash
openclaw cron runs <job-id>
```

### 手动运行任务（测试）
```bash
openclaw cron run <job-id>
```

### 禁用/启用任务
```bash
openclaw cron disable <job-id>
openclaw cron enable <job-id>
```

### 删除任务
```bash
openclaw cron rm <job-id>
```

---

## ⚙️ 配置说明（保留参考）

### 时间格式
- 固定时间: `HH:MM` (24小时制)
- 循环周期: `每X小时/天/周`
- 特定日期: `YYYY-MM-DD HH:MM`

### Cron 表达式
- `30 7 * * *` = 每天 7:30
- `0 7 * * *` = 每天 7:00
- `0 18 * * 5` = 每周五 18:00
- `0 8 * * 1` = 每周一 8:00

### 执行动作
- 发送消息: 通过配置的 channel (飞书/Telegram/等)
- 查询数据: 读取文件、API、网页
- 生成报告: 汇总信息并格式化
- 提醒通知: @用户或发送私信

---

*最后更新: 2026-03-21 21:15*
*状态: ✅ 所有任务已迁移至 Cron 系统*