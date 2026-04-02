# 验证知识库

本知识库整理自 D:\飞书\验证书籍 和 D:\飞书\协议&标准 目录下的验证相关内容。

**状态**: ✅ 已完成

---

## 知识库结构

```
verification/
├── README.md                    # 本文件 - 索引
├── raw/                         # 原始提取内容（验证书籍，7.3MB）
├── protocols_raw/               # 协议原始提取（验证相关，14MB）
│
├── 01_systemverilog_basics.md   # SystemVerilog 基础 (6KB)
├── 02_uvm_framework.md          # UVM 验证框架 (7KB)
├── 03_testbench_architecture.md # 测试平台架构 (6KB)
├── 04_assertions.md             # 断言技术 (12KB)
├── 05_coverage.md               # 覆盖率技术 (18KB)
├── 06_randomization.md          # 随机化技术 (14KB)
├── 07_verification_methodology.md # 验证方法论 (20KB)
├── 08_advanced_topics.md        # 进阶主题 (13KB)
├── 09_practical_cases.md        # 实战案例 (13KB)
├── 10_systemverilog_standard.md # SV 语言标准 (6KB)
└── ai_verification.md           # AI 时代验证策略 (5KB)
```

**总计**: 约 110KB 结构化知识文档 + 21MB 原始内容

---

## 来源文档

### 验证书籍 (D:\飞书\验证书籍)

| 书籍名称 | 页数 | 主要内容 |
|---------|------|----------|
| SystemVerilog for Verification 3rd Ed. | 500 | SV验证语言特性 |
| UVM实战（张强） | 836 | UVM框架详解 |
| UVM1.1应用指南及源码解析 | 636 | UVM源码分析 |
| VMM (Verification Methodology Manual) | 528 | VMM方法论 |
| SystemVerilog功能验证 | 221 | SV功能验证 |
| 101个Verilog和SystemVerilog陷阱 | 98 | 常见陷阱 |
| Verilog Digital System Design | 402 | 数字系统设计 |
| Fundamentals of Digital Logic with Verilog | 864 | Verilog基础 |
| 深度学习笔记（1-3册） | 1226 | 深度学习应用 |

### 协议标准 (D:\飞书\协议&标准)

| 文档名称 | 页数 | 主要内容 |
|---------|------|----------|
| IEEE Std 1800-2023 | 1918 | SystemVerilog 标准 |
| IEEE 18002-2020-UVM | 580 | UVM 标准 |
| UVM Users Guide 1.1 | 198 | UVM 用户指南 |
| UVM Cookbook 2021 | 547 | UVM 实践指南 |
| VCS MX User Guide | 1000 | VCS 工具指南 |

---

## 知识点索引

### 1. SystemVerilog 基础
- 数据类型（logic, bit, int, string, enum, struct）
- 数组（静态、动态、关联、队列）
- 过程语句（task, function, fork-join）
- 面向对象编程（class, inheritance, polymorphism）
- 线程与进程间通信（event, semaphore, mailbox）

### 2. UVM 框架
- 工厂机制（factory, create, override）
- 组件层次（driver, monitor, agent, env, test）
- Phase 机制（build, connect, run, report）
- Sequence 机制（sequence_item, sequence, virtual sequence）
- Config DB（set, get, 配置传递）
- TLM 通信（port, export, imp, fifo）

### 3. 测试平台架构
- 分层测试平台（signal, command, functional, scenario, test）
- 接口设计（interface, clocking block, modport）
- 虚拟接口（virtual interface）
- 事务级建模（transaction, sequence item）
- 验证组件设计模式

### 4. 断言技术
- 立即断言（immediate assertion）
- 并发断言（concurrent assertion）
- 序列（sequence）操作符
- 属性（property）定义
- 蕴含操作符（->, =>）
- 断言实战案例（FIFO, FSM, 总线协议）

### 5. 覆盖率技术
- 代码覆盖率（line, branch, condition, toggle, FSM）
- 功能覆盖率（covergroup, coverpoint, bins）
- 交叉覆盖率（cross coverage）
- 覆盖率策略（边界值、异常场景）
- 覆盖率分析与缺口填补

### 6. 随机化技术
- 约束定义（constraint block）
- 分布控制（dist, weight）
- 条件约束（if-else, implication）
- 数组约束（foreach, sum）
- 随机化控制（rand_mode, constraint_mode）
- pre_randomize/post_randomize

### 7. 验证方法论
- 验证计划制定
- 测试平台架构设计
- 验证组件开发
- 回归测试策略
- 覆盖率驱动验证

### 8. 进阶主题
- 常见陷阱与规避
- 性能优化技巧
- 调试方法
- 代码规范

### 9. 实战案例
- 完整验证环境示例
- 项目实践经验
- 深度学习在验证中的应用

---

## 快速导航

### 初学者路径
```
01_systemverilog_basics.md → 数据类型、OOP
03_testbench_architecture.md → 接口、测试平台
02_uvm_framework.md → UVM 组件、Phase
```

### 进阶路径
```
04_assertions.md → SVA 断言技术
05_coverage.md → 功能覆盖率
06_randomization.md → 约束随机化
```

### 专家路径
```
07_verification_methodology.md → 方法论
10_systemverilog_standard.md → 语言标准
raw/ 目录 → 原始书籍深入阅读
```

---

*生成时间: 2026-04-01*
*来源: D:\飞书\验证书籍 + D:\飞书\协议&标准*
