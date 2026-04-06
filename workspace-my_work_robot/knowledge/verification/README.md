# 验证知识库

本知识库整理自 D:\飞书\验证书籍 目录下的所有验证相关书籍。

## 知识库结构

```
verification/
├── README.md                    # 本文件 - 知识库索引
├── raw/                         # 原始提取内容（PDF转文本）
│
├── 01_systemverilog_basics.md   # SystemVerilog 基础 ✅
├── 02_uvm_framework.md          # UVM 验证框架 ✅
├── 03_testbench_architecture.md # 测试平台架构 ✅
├── 04_assertions.md             # 断言技术 ✅
├── 05_coverage.md               # 覆盖率技术 ✅
├── 06_randomization.md          # 随机化技术 ✅
├── 07_verification_methodology.md # 验证方法论 ✅
├── 08_advanced_topics.md        # 进阶主题 ✅
└── 09_practical_cases.md        # 实战案例 ✅
```

## 书籍来源清单

共提取 **19 个 PDF**，总计 **6000+ 页** 内容。

| 书籍名称 | 页数 | 主要内容 | 对应章节 |
|---------|------|----------|---------|
| SystemVerilog for Verification 3rd Ed. | 500 | SV验证语言特性 | 01, 03, 05, 06 |
| UVM实战（张强） | 836 | UVM框架详解 | 02 |
| UVM1.1应用指南及源码解析 | 636 | UVM源码分析 | 02 |
| VMM (Verification Methodology Manual) | 528 | VMM方法论 | 07 |
| SystemVerilog功能验证 | 221 | SV功能验证 | 01, 03 |
| 101个Verilog和SystemVerilog陷阱 | 98 | 常见陷阱 | 08 |
| Verilog Digital System Design | 402 | 数字系统设计 | 01 |
| Fundamentals of Digital Logic with Verilog | 864 | Verilog基础 | 01 |
| 深度学习笔记（1-3册） | 1226 | 深度学习应用 | 09 |
| 基于SystemVerilog+UVM建立SOC/ASIC RTL验证 | 50 | 验证平台搭建 | 03 |
| 用System Verilog建立RTL验证平台 | 26 | 验证平台 | 03 |

## 文档概要

### 01_systemverilog_basics.md
- 数据类型：logic、bit、数组、队列、关联数组
- 过程语句：任务、函数、控制流
- OOP 基础：类、继承、句柄
- 接口连接：Interface、Clocking Block、Program

### 02_uvm_framework.md
- UVM 类层次结构
- 工厂机制：注册、创建、覆盖
- UVM 组件：Driver、Monitor、Sequencer、Agent、Scoreboard
- Phase 机制：build、connect、run、report
- Sequence 机制：Sequence Item、Virtual Sequence
- Config DB：配置传递
- TLM 通信：Analysis Port、FIFO

### 03_testbench_architecture.md
- 分层测试平台：信号层、命令层、功能层、场景层、测试层
- 接口设计：Interface、Virtual Interface
- 事务级建模：Transaction 定义、队列
- 组件设计模式：Driver、Monitor、Scoreboard

### 04_assertions.md
- 立即断言：assert
- 并发断言：assert property
- 序列：Sequence 定义、操作符
- 属性：Property 定义、蕴含、重复
- 覆盖属性：cover property
- 实战案例：总线协议、FIFO、状态机断言

### 05_coverage.md
- 代码覆盖率：行、分支、条件、翻转、FSM
- 功能覆盖率：Covergroup、Coverpoint
- Bins 定义：单值、范围、翻转、通配符
- 交叉覆盖：Cross Coverage
- 实战案例：总线、FIFO、状态机覆盖组

### 06_randomization.md
- Rand 与 Randc
- 约束：Constraint、表达式、分布
- 约束块：集合、条件、循环、数组
- 随机化方法：randomize、pre/post_randomize
- 随机化控制：rand_mode、constraint_mode

### 07_verification_methodology.md
- 验证计划：规划、功能分解
- 验证策略：方法选择、验证层次
- 验证环境：架构、组件复用
- 回归测试：策略、管理
- 验证管理：缺陷管理、进度追踪
- 最佳实践：代码规范、调试技巧

### 08_advanced_topics.md
- 常见陷阱：竞争条件、静态变量、数组越界
- 性能优化：仿真、内存、日志
- 调试技巧：波形、日志、断点
- 高级 UVM：Callback、Factory、自定义 Phase
- 形式验证：等价性检查、模型检查

### 09_practical_cases.md
- APB 总线验证完整案例
- FIFO 验证案例
- 状态机验证案例
- UART 验证案例
- 多通道验证案例

## 快速导航

### 初学者路径
1. [SystemVerilog 基础](01_systemverilog_basics.md) → 数据类型、过程语句、OOP
2. [测试平台架构](03_testbench_architecture.md) → 接口、Program、Clocking
3. [UVM 框架](02_uvm_framework.md) → 组件、Phase、Sequence

### 进阶路径
1. [断言技术](04_assertions.md) → SVA、时序断言
2. [覆盖率技术](05_coverage.md) → 代码覆盖、功能覆盖
3. [随机化技术](06_randomization.md) → 约束、分布

### 专家路径
1. [验证方法论](07_verification_methodology.md) → VMM/UVM方法论
2. [进阶主题](08_advanced_topics.md) → 高级技巧、陷阱规避
3. [实战案例](09_practical_cases.md) → 项目实践

---

*生成时间: 2026-04-01*
*来源: D:\飞书\验证书籍*
*原始文件: knowledge/verification/raw/ 目录*
