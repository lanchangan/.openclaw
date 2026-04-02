# 覆盖率技术

> 本文档整理自《SystemVerilog for Verification》《VMM》等书籍

## 目录

1. [覆盖率概述](#1-覆盖率概述)
2. [代码覆盖率](#2-代码覆盖率)
3. [功能覆盖率基础](#3-功能覆盖率基础)
4. [覆盖组 Covergroup](#4-覆盖组-covergroup)
5. [覆盖点 Coverpoint](#5-覆盖点-coverpoint)
6. [交叉覆盖 Cross Coverage](#6-交叉覆盖)
7. [覆盖率策略](#7-覆盖率策略)
8. [覆盖率分析](#8-覆盖率分析)

---

## 1. 覆盖率概述

### 1.1 为什么需要覆盖率

```
┌─────────────────────────────────────────────────────────────┐
│                    验证的完整性问题                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   "你什么时候算验证完成？"                                    │
│                                                             │
│   ✓ 跑了 10000 个测试用例？                                  │
│   ✓ 仿真了 100 小时？                                        │
│   ✓ 发现了 50 个 Bug？                                       │
│                                                             │
│   → 这些都不是可靠的衡量标准！                                │
│                                                             │
│   真正的问题是：你测试了多少设计功能？                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 覆盖率类型

```
┌─────────────────────────────────────────────────────────────┐
│                        覆盖率层次                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              功能覆盖率 (Functional)                 │   │
│  │  • 验证计划驱动                                      │   │
│  │  • 测量设计规格覆盖                                  │   │
│  │  • 需要人工定义                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ▲                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              断言覆盖率 (Assertion)                  │   │
│  │  • 协议检查                                          │   │
│  │  • 时序约束                                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ▲                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              代码覆盖率 (Code)                       │   │
│  │  • 行覆盖率                                          │   │
│  │  • 分支覆盖率                                        │   │
│  │  • 条件覆盖率                                        │   │
│  │  • FSM 覆盖率                                        │   │
│  │  • 翻转覆盖率                                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 覆盖率目标

| 覆盖率类型 | 目标值 | 说明 |
|------------|--------|------|
| 行覆盖率 | 100% | 每行代码都应执行 |
| 分支覆盖率 | 100% | 每个 if/else 分支 |
| 条件覆盖率 | 100% | 每个条件的真/假 |
| FSM 覆盖率 | 100% | 所有状态和转换 |
| 功能覆盖率 | 视规格 | 根据验证计划定义 |

---

## 2. 代码覆盖率

### 2.1 行覆盖率 (Line Coverage)

```systemverilog
// 示例：未被覆盖的代码
always @(posedge clk) begin
    if (condition_a)
        result = a + b;      // 已覆盖
    else
        result = a - b;      // 未覆盖 ← 需要测试
end
```

### 2.2 分支覆盖率 (Branch Coverage)

```systemverilog
// 分支覆盖检查每个 if/else 和 case 分支
always @(*) begin
    case (state)
        IDLE:   next = FETCH;   // 需要覆盖
        FETCH:  next = DECODE;  // 需要覆盖
        DECODE: next = EXEC;    // 需要覆盖
        default: next = IDLE;   // 需要覆盖
    endcase
end

// 分支覆盖率报告示例
// case 语句覆盖: 3/4 (75%)
// 未覆盖分支: default
```

### 2.3 条件覆盖率 (Condition Coverage)

```systemverilog
// 条件覆盖率检查每个子条件的真/假组合
if (a && b || c)  // 需要 2^3 = 8 种组合？实际需要 6 种
    result = 1;

// 条件组合分析
// a=0, b=X, c=0 → 结果 = 0 (需要测试)
// a=0, b=X, c=1 → 结果 = 1 (需要测试)
// a=1, b=0, c=0 → 结果 = 0 (需要测试)
// a=1, b=0, c=1 → 结果 = 1 (需要测试)
// a=1, b=1, c=X → 结果 = 1 (需要测试)
```

### 2.4 翻转覆盖率 (Toggle Coverage)

```systemverilog
// 翻转覆盖率检查信号的变化
// 每个信号位需要 0→1 和 1→0 的翻转

// 示例报告
// signal[31:0] 翻转覆盖率:
// bit 0:  0→1 ✓, 1→0 ✓  (100%)
// bit 15: 0→1 ✓, 1→0 ✗  (50%)
// bit 31: 0→1 ✗, 1→0 ✗  (0%)  ← 常数或未使用？
```

### 2.5 FSM 覆盖率

```systemverilog
// FSM 覆盖率检查
// 1. 状态覆盖率：是否访问了所有状态
// 2. 转换覆盖率：是否经历了所有状态转换

typedef enum {IDLE, FETCH, DECODE, EXEC} state_t;
state_t state, next_state;

// FSM 覆盖率报告示例
// 状态覆盖: 4/4 (100%)
// 转换覆盖: 5/8 (62.5%)
// 未覆盖转换:
//   IDLE → EXEC (非法转换？)
//   FETCH → IDLE (需要测试复位场景)
```

---

## 3. 功能覆盖率基础

### 3.1 功能覆盖率 vs 代码覆盖率

```
┌─────────────────────────────────────────────────────────────┐
│              功能覆盖率 vs 代码覆盖率                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  代码覆盖率回答："代码执行了吗？"                            │
│  功能覆盖率回答："功能测试了吗？"                            │
│                                                             │
│  示例：                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  // 代码覆盖率 100%，但功能可能未覆盖               │   │
│  │  if (addr < 100) begin                              │   │
│  │      // 测试了 addr=0, 50, 99                       │   │
│  │      // 但边界 100 呢？溢出情况呢？                  │   │
│  │  end                                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  功能覆盖率可以：                                           │
│  • 检查边界值是否测试                                       │
│  • 检查所有操作模式                                         │
│  • 检查异常情况                                             │
│  • 检查配置组合                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 功能覆盖率策略

```systemverilog
// 策略 1: 采样数据值
covergroup cg_data;
    cp_addr: coverpoint trans.addr;
    cp_data: coverpoint trans.data;
endcovergroup

// 策略 2: 采样控制流
covergroup cg_control;
    cp_state: coverpoint fsm.state;
    cp_event: coverpoint {interrupt, exception};
endcovergroup

// 策略 3: 采样配置组合
covergroup cg_config;
    cp_mode: coverpoint cfg.mode;
    cp_size: coverpoint cfg.size;
    cross_mode_size: cross cp_mode, cp_size;
endcovergroup
```

---

## 4. 覆盖组 Covergroup

### 4.1 定义覆盖组

```systemverilog
// 在类中定义
class Transaction;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    
    // 定义覆盖组
    covergroup cg_trans;
        cp_addr: coverpoint addr;
        cp_data: coverpoint data;
    endcovergroup
    
    function new();
        cg_trans = new();  // 实例化覆盖组
    endfunction
    
    function void sample();
        cg_trans.sample();  // 采样
    endfunction
endclass

// 独立定义覆盖组
covergroup cg_address #(parameter WIDTH=32);
    cp_addr: coverpoint addr[WIDTH-1:0];
endcovergroup
```

### 4.2 覆盖组采样方式

```systemverilog
// 方式 1: 显式调用 sample()
Transaction trans;
trans = new();
trans.randomize();
trans.sample();  // 手动采样

// 方式 2: 事件触发
covergroup cg_event @(posedge clk);
    cp_valid: coverpoint valid;
endcovergroup

// 方式 3: 序列触发
covergroup cg_sequence;
    cp_trans: coverpoint data;
endcovergroup

// 使用断言触发
always @(posedge clk) begin
    if (transaction_complete)
        cg.sample();
end

// 方式 4: 回调采样
class Driver;
    virtual function void sample_trans(Transaction trans);
        trans.cg_trans.sample();
    endfunction
endclass
```

### 4.3 覆盖组选项

```systemverilog
covergroup cg_options;
    // 覆盖率目标
    option.goal = 90;  // 目标 90%（默认 100%）
    
    // 注释
    option.comment = "Transaction coverage";
    
    // 实例覆盖
    option.per_instance = 1;  // 每个实例独立统计
    
    // 打印空 bin
    option.print_empty = 1;
    
    // 自动 bin 最大数量
    option.auto_bin_max = 64;
    
    // 权重
    option.weight = 2;  // 在总覆盖率中权重加倍
    
    cp_data: coverpoint data;
endcovergroup
```

---

## 5. 覆盖点 Coverpoint

### 5.1 基本覆盖点

```systemverilog
covergroup cg_basic;
    // 简单覆盖点
    cp_addr: coverpoint addr;
    
    // 表达式覆盖点
    cp_sum: coverpoint (a + b);
    
    // 位选择覆盖点
    cp_bit: coverpoint data[7:0];
endcovergroup
```

### 5.2 自动 Bins

```systemverilog
covergroup cg_auto_bins;
    // 自动创建 bins
    cp_data: coverpoint data;
    // 自动创建 64 个 bins（option.auto_bin_max 默认值）
    
    // 限制自动 bin 数量
    cp_addr: coverpoint addr {
        option.auto_bin_max = 16;  // 只创建 16 个 bins
    }
endcovergroup
```

### 5.3 显式 Bins

```systemverilog
covergroup cg_explicit_bins;
    cp_addr: coverpoint addr {
        // 单值 bin
        bins zero     = {0};
        bins one      = {1};
        
        // 范围 bin
        bins range_0_100   = {[0:100]};
        bins range_101_200 = {[101:200]};
        
        // 离散值 bin
        bins values   = {10, 20, 30, 40, 50};
        
        // 转换 bin
        bins trans_0_1 = (0 => 1);
        bins trans_1_0 = (1 => 0);
        
        // 通配符 bin
        wildcard bins pattern = {8'b1???_????};
        
        // 默认 bin（其他所有值）
        bins others = default;
    }
endcovergroup
```

### 5.4 条件 Bins

```systemverilog
covergroup cg_conditional_bins;
    cp_mode: coverpoint mode {
        // 忽略某些值
        ignore_bins unused = {[8:15]};
        
        // 非法值（遇到会报错）
        illegal_bins invalid = {16'hFFFF};
    }
    
    // 条件覆盖
    cp_valid_data: coverpoint data {
        bins valid = {[0:255]} iff (valid == 1);
        // 只在 valid=1 时采样
    }
endcovergroup
```

### 5.5 转换覆盖

```systemverilog
covergroup cg_transition;
    cp_state: coverpoint state {
        // 单步转换
        bins idle_to_fetch  = (IDLE => FETCH);
        bins fetch_to_decode = (FETCH => DECODE);
        
        // 转换序列
        bins sequence = (IDLE => FETCH => DECODE => EXEC);
        
        // 重复转换
        bins repeat_3 = (IDLE => IDLE => IDLE);
        
        // 范围转换
        bins any_to_idle = (default => IDLE);
    }
endcovergroup
```

### 5.6 枚举覆盖

```systemverilog
typedef enum {READ, WRITE, IDLE} mode_t;

covergroup cg_enum;
    cp_mode: coverpoint mode {
        // 自动为每个枚举值创建 bin
        bins modes = {READ, WRITE, IDLE};
    }
endcovergroup

// 等价于
covergroup cg_enum_auto;
    cp_mode: coverpoint mode;  // 自动创建 READ, WRITE, IDLE bins
endcovergroup
```

---

## 6. 交叉覆盖 Cross Coverage

### 6.1 基本交叉覆盖

```systemverilog
covergroup cg_cross;
    cp_mode: coverpoint mode {
        bins read  = {READ};
        bins write = {WRITE};
    }
    
    cp_size: coverpoint size {
        bins byte = {1};
        bins word = {4};
        bins dword = {8};
    }
    
    // 交叉覆盖：生成 2 × 3 = 6 个 cross bins
    cross_mode_size: cross cp_mode, cp_size;
endcovergroup

// 交叉 bin 列表
// read × byte
// read × word
// read × dword
// write × byte
// write × word
// write × dword
```

### 6.2 交叉覆盖排除

```systemverilog
covergroup cg_cross_exclude;
    cp_mode: coverpoint mode {
        bins read  = {READ};
        bins write = {WRITE};
        bins idle  = {IDLE};
    }
    
    cp_size: coverpoint size {
        bins byte = {1};
        bins word = {4};
    }
    
    cross_mode_size: cross cp_mode, cp_size {
        // 忽略特定组合
        ignore_bins ignore_idle = 
            binsof(cp_mode.idle);
        
        // 忽略 read × byte 组合
        ignore_bins ignore_read_byte = 
            binsof(cp_mode.read) && binsof(cp_size.byte);
        
        // 只保留特定组合
        bins valid_only = 
            binsof(cp_mode.write) && binsof(cp_size.word);
    }
endcovergroup
```

### 6.3 交叉覆盖示例

```systemverilog
// 总线事务交叉覆盖
covergroup cg_bus_trans;
    // 操作类型
    cp_cmd: coverpoint cmd {
        bins read  = {RD};
        bins write = {WR};
        bins rmw   = {RMW};
    }
    
    // 地址范围
    cp_addr: coverpoint addr {
        bins low    = {[32'h0000_0000:32'h0000_FFFF]};
        bins mid    = {[32'h0001_0000:32'hFFFF_0000]};
        bins high   = {[32'hFFFF_0001:32'hFFFF_FFFF]};
    }
    
    // 数据大小
    cp_size: coverpoint size {
        bins b1  = {1};
        bins b2  = {2};
        bins b4  = {4};
        bins b8  = {8};
    }
    
    // 三维交叉
    cross_cmd_addr_size: cross cp_cmd, cp_addr, cp_size {
        // 忽略无效组合
        ignore_bins ignore_rmw_b1 = 
            binsof(cp_cmd.rmw) && binsof(cp_size.b1);
    }
endcovergroup
```

---

## 7. 覆盖率策略

### 7.1 从验证计划到覆盖率模型

```
┌─────────────────────────────────────────────────────────────┐
│                    覆盖率开发流程                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  验证计划                                                   │
│      │                                                      │
│      ▼                                                      │
│  识别功能点                                                 │
│      │                                                      │
│      ▼                                                      │
│  定义覆盖组                                                 │
│      │                                                      │
│      ▼                                                      │
│  设计约束和随机化                                           │
│      │                                                      │
│      ▼                                                      │
│  运行仿真收集覆盖率                                         │
│      │                                                      │
│      ▼                                                      │
│  分析覆盖率报告                                             │
│      │                                                      │
│      ▼                                                      │
│  补充测试用例                                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 覆盖率分层

```systemverilog
// 第 1 层：事务级覆盖
covergroup cg_transaction;
    cp_cmd:  coverpoint trans.cmd;
    cp_addr: coverpoint trans.addr;
    cp_size: coverpoint trans.size;
endcovergroup

// 第 2 层：协议级覆盖
covergroup cg_protocol;
    cp_burst_type: coverpoint burst_type;
    cp_response:   coverpoint response;
    
    // 协议时序
    cp_latency: coverpoint latency {
        bins fast   = {[0:10]};
        bins medium = {[11:50]};
        bins slow   = {[51:100]};
    }
endcovergroup

// 第 3 层：系统级覆盖
covergroup cg_system;
    cp_concurrent_users: coverpoint active_users;
    cp_throughput: coverpoint throughput;
    
    // 系统状态组合
    cross_system_state: cross 
        cp_concurrent_users, cp_throughput;
endcovergroup
```

### 7.3 边界值覆盖

```systemverilog
covergroup cg_boundary;
    cp_addr: coverpoint addr {
        // 边界值
        bins min     = {32'h0000_0000};
        bins max     = {32'hFFFF_FFFF};
        bins min_1   = {32'h0000_0001};
        bins max_1   = {32'hFFFF_FFFE};
        
        // 对齐边界
        bins align_4   = {32'h0000_0004, 32'h0000_0008, ...};
        bins align_16  = {32'h0000_0010, 32'h0000_0020, ...};
        bins align_256 = {32'h0000_0100, 32'h0000_0200, ...};
        
        // 边界附近
        bins near_boundary = {
            [32'hFFFF_FFF0:32'hFFFF_FFFF],
            [32'h0000_0000:32'h0000_000F]
        };
    }
endcovergroup
```

### 7.4 异常覆盖

```systemverilog
covergroup cg_exception;
    // 错误类型
    cp_error: coverpoint error_type {
        bins no_error    = {0};
        bins parity_err  = {1};
        bins timeout_err = {2};
        bins crc_err     = {3};
    }
    
    // 错误注入时机
    cp_inject_time: coverpoint inject_time {
        bins during_header = {HEADER};
        bins during_data   = {DATA};
        bins during_crc    = {CRC};
    }
    
    // 错误恢复
    cp_recovery: coverpoint recovery_type {
        bins retry   = {RETRY};
        bins abort   = {ABORT};
        bins recover = {RECOVER};
    }
    
    // 错误场景交叉
    cross_error_scenario: cross cp_error, cp_inject_time, cp_recovery;
endcovergroup
```

---

## 8. 覆盖率分析

### 8.1 覆盖率报告

```systemverilog
// 获取覆盖率值
real coverage;
coverage = cg.get_coverage();  // 获取总覆盖率

// 获取覆盖点覆盖率
coverage = cg.cp_addr.get_coverage();

// 获取交叉覆盖率
coverage = cg.cross_mode_size.get_coverage();

// 打印覆盖率报告
initial begin
    #100000;  // 仿真结束
    $display("Overall Coverage: %.2f%%", cg.get_coverage());
    $display("Address Coverage: %.2f%%", cg.cp_addr.get_coverage());
end
```

### 8.2 覆盖率合并

```systemverilog
// 多实例覆盖率合并
covergroup cg_per_instance;
    option.per_instance = 1;  // 每个实例独立
    cp_data: coverpoint data;
endcovergroup

// 实例化多个
cg_per_instance cg_inst1 = new();
cg_per_instance cg_inst2 = new();

// 合并报告
// 工具会自动合并所有实例的覆盖率
```

### 8.3 覆盖率数据库

```systemverilog
// 保存覆盖率数据
initial begin
    $set_coverage_db_name("coverage.ucdb");  // 设置数据库名
    $load_coverage_db("coverage.ucdb");      // 加载已有数据
end

// 运行时查询
initial begin
    #100000;
    $display("Coverage database saved");
    $stop;  // 保存覆盖率数据
end
```

### 8.4 覆盖率缺口分析

```
┌─────────────────────────────────────────────────────────────┐
│                    覆盖率缺口分析流程                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 查看覆盖率报告                                          │
│     • 哪些 bins 未覆盖？                                    │
│     • 哪些组合未测试？                                      │
│                                                             │
│  2. 分析未覆盖原因                                          │
│     • 约束限制？→ 放宽约束                                  │
│     • 测试不足？→ 添加测试                                  │
│     • 功能未实现？→ 确认规格                                │
│     • 非法情况？→ 添加 ignore_bins                          │
│                                                             │
│  3. 补充测试                                                │
│     • 添加定向测试                                          │
│     • 修改随机约束                                          │
│     • 增加测试时间                                          │
│                                                             │
│  4. 回归验证                                                │
│     • 确认覆盖率提升                                        │
│     • 确认功能正确                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 参考书籍

- SystemVerilog for Verification 3rd Edition, Chris Spear & Greg Tumbush
- Verification Methodology Manual for SystemVerilog
- IEEE 1800 SystemVerilog LRM

---

*整理自验证知识库*
