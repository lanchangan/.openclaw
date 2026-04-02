# 断言技术

> 本文档整理自《SystemVerilog for Verification》《VMM》等书籍

## 目录

1. [断言概述](#1-断言概述)
2. [立即断言](#2-立即断言)
3. [并发断言](#3-并发断言)
4. [序列 (Sequence)](#4-序列-sequence)
5. [属性 (Property)]#5-属性-property)
6. [断言实战技巧](#6-断言实战技巧)
7. [断言覆盖](#7-断言覆盖)
8. [断言调试](#8-断言调试)

---

## 1. 断言概述

### 1.1 什么是断言

断言（Assertion）是用于检查设计行为的描述性语句。它们：
- 自动检查设计是否符合规范
- 提高调试效率
- 作为文档记录设计意图
- 可用于形式验证

### 1.2 断言类型

| 类型 | 关键字 | 执行方式 | 用途 |
|------|--------|----------|------|
| 立即断言 | assert | 立即执行 | 组合逻辑检查 |
| 并发断言 | assert property | 周期性评估 | 时序检查 |
| 覆盖断言 | cover property | 统计计数 | 功能覆盖 |
| 假设断言 | assume property | 约束求解器 | 形式验证 |

### 1.3 断言位置

```systemverilog
// 模块内部断言
module my_module (...);
    // 内部信号断言
    assert property (req |-> ##2 ack);
endmodule

// 接口断言
interface my_interface (...);
    // 协议检查
    assert property (valid |-> ##[1:5] ready);
endinterface

// 程序块断言（验证环境）
program testbench;
    // 测试行为断言
endprogram

// 检查器模块（可重用）
module checker #(parameter WIDTH=8) (...);
    // 参数化断言
endmodule
```

---

## 2. 立即断言

### 2.1 基本语法

```systemverilog
// 基本形式
assert (expression);

// 带动作块
assert (expression)
    $display("PASS: assertion passed");
else
    $error("FAIL: assertion failed");

// 完整形式
assert (expression)
begin
    // 成功时执行
    $display("PASS at time %0t", $time);
end
else
begin
    // 失败时执行
    $error("FAIL: expected %b, got %b", expected, actual);
end
```

### 2.2 常见应用场景

```systemverilog
// One-hot 检查
always @(*) begin
    assert ($onehot(select)) 
        else $error("Select not one-hot: %b", select);
end

// 互斥检查
always @(*) begin
    assert (!(read_en && write_en)) 
        else $error("Read and Write both enabled!");
end

// 范围检查
always @(*) begin
    assert (addr < MAX_ADDR) 
        else $error("Address out of range: %h", addr);
end

// 指针非空检查
always @(*) begin
    assert (ptr != null) 
        else $error("Null pointer dereference");
end

// 状态机合法状态检查
always @(*) begin
    assert (state inside {IDLE, FETCH, DECODE, EXEC, WRITEBACK})
        else $error("Invalid state: %b", state);
end
```

### 2.3 立即断言与并发断言对比

```
┌─────────────────────────────────────────────────────────────────┐
│                    立即断言 vs 并发断言                          │
├─────────────────────────────────────────────────────────────────┤
│  特性          │  立即断言        │  并发断言                   │
├────────────────┼──────────────────┼─────────────────────────────┤
│  执行时机      │  过程块执行时    │  每个时钟边沿               │
│  时钟依赖      │  无              │  需要时钟                   │
│  时序检查      │  不支持          │  支持                       │
│  适用场景      │  组合逻辑        │  时序逻辑                   │
│  性能影响      │  较小            │  较大（周期性评估）         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. 并发断言

### 3.1 基本结构

```systemverilog
// 默认时钟声明
default clocking cb @(posedge clk);
endclocking

// 默认复位条件
default disable iff (!rst_n);

// 简单并发断言
assert property (req |-> ##2 ack);

// 带标签的断言
AP_REQ_ACK: assert property (req |-> ##2 ack)
    else $error("No ACK for REQ");
```

### 3.2 断言块结构

```systemverilog
// 并发断言的完整结构
assert property (
    @(posedge clk)      // 时钟事件
    disable iff (!rst_n) // 复位条件
    property_expression  // 属性表达式
)
else begin
    $error("Assertion failed at time %0t", $time);
end
```

### 3.3 并发断言的四种形式

```systemverilog
// 1. assert property - 检查属性是否成立
assert property (req |-> ack);

// 2. cover property - 统计属性成立次数
cover property (req ##1 ack);

// 3. assume property - 假设属性成立（形式验证）
assume property (rst_n |-> !req);

// 4. expect property - 等待属性成立（类似 wait）
expect (req |-> ##[1:5] ack);
```

---

## 4. 序列 (Sequence)

### 4.1 基本序列

```systemverilog
// 简单序列
sequence s_simple;
    a ##1 b;  // a 后 1 周期 b
endsequence

// 带延迟的序列
sequence s_delay;
    a ##[1:5] b;  // a 后 1-5 周期内 b
endsequence

// 固定重复
sequence s_repeat;
    a ##1 b[*3];  // b 连续 3 周期
endsequence

// 范围重复
sequence s_repeat_range;
    a ##1 b[*2:5];  // b 连续 2-5 周期
endsequence
```

### 4.2 序列运算符

```systemverilog
// 延迟操作符
##n      // 固定延迟 n 周期
##[m:n]  // 范围延迟 m 到 n 周期
##[*]    // 无限延迟（0 到无穷）
##[+]    // 至少 1 周期延迟

// 重复操作符
s[*n]    // 连续重复 n 次
s[*m:n]  // 连续重复 m 到 n 次
s[=n]    // 非连续重复，恰好 n 次
s[->n]   // 非连续重复，最后一次匹配后继续

// 逻辑运算符
s1 and s2   // 两序列同时开始，同时结束
s1 or s2    // 两序列任一匹配
s1 intersect s2  // 两序列长度相同
s1 within s2     // s1 在 s2 期间发生
s1 throughout s2 // s1 在整个 s2 期间保持
!s          // 序列不发生

// 条件运算符
s if (expr)  // 条件满足时匹配
```

### 4.3 序列方法

```systemverilog
// 信号变化检测
$rose(sig)      // 信号上升（从 0 变 1）
$fell(sig)      // 信号下降（从 1 变 0）
$stable(sig)    // 信号稳定（值不变）
$changed(sig)   // 信号改变

// 历史值
$past(sig)      // 上一周期的值
$past(sig, n)   // 前 n 周期的值

// 计数
$countones(sig) // 1 的个数
$onehot(sig)    // 是否 one-hot
$onehot0(sig)   // 是否 one-hot 或全 0

// 位操作
$isunknown(sig) // 是否包含 X 或 Z
```

### 4.4 序列示例

```systemverilog
// 请求-响应序列
sequence s_req_resp;
    req ##[1:10] ack ##1 data_valid;
endsequence

// 写事务序列
sequence s_write;
    write_en && addr_valid ##[1:2] 
    data_ready ##0 write_done;
endsequence

// 突发传输序列
sequence s_burst;
    start ##1 data[*4] ##1 stop;
endsequence

// 带条件的序列
sequence s_conditional;
    req ##1 (ack && !error);
endsequence

// 使用序列方法
sequence s_methods;
    $rose(valid) ##1 $stable(data) ##1 $fell(busy);
endsequence
```

---

## 5. 属性 (Property)

### 5.1 属性定义

```systemverilog
// 内联属性
assert property (req |-> ack);

// 命名属性
property p_req_ack;
    req |-> ##[1:3] ack;
endproperty

assert property (p_req_ack);

// 带参数的属性
property p_handshake(req, ack, delay);
    req |-> ##[1:delay] ack;
endproperty

assert property (p_handshake(read_req, read_ack, 5));
```

### 5.2 蕴含操作符

```systemverilog
// 交叠蕴含 |-> (同周期)
// 如果前提成立，结论在同周期必须成立
property p_overlap;
    req |-> gnt;  // req 和 gnt 同周期
endproperty

// 非交叠蕴含 |=> (下一周期)
// 如果前提成立，结论在下一周期必须成立
property p_next_cycle;
    req |=> gnt;  // req 后下一周期 gnt
endproperty

// 蕴含的 truth table
// 前提为假 → 空成功（vacuous success）
// 前提为真 → 检查结论

// 示例
property p_vacuous;
    req |-> ack;
    // 如果 req=0，断言空成功
    // 如果 req=1，检查 ack
endproperty
```

### 5.3 属性中的逻辑运算

```systemverilog
// 与运算
property p_and;
    req |-> (ack && ready);
endproperty

// 或运算
property p_or;
    req |-> (ack || retry);
endproperty

// 非运算
property p_not;
    not (req ##1 !ack);
endproperty

// if-else
property p_if_else;
    if (mode == READ)
        read_req |-> read_ack
    else
        write_req |-> write_ack;
endproperty
```

### 5.4 属性中的变量

```systemverilog
// 局部变量
property p_local_var;
    int count;
    (req, count = 0) ##1 
    (ack && (count < 10), count++)[*1:$] ##1 
    (count == 10);
endproperty

// 匹配变量
property p_match;
    bit [31:0] saved_addr;
    (req && addr == saved_addr) |-> ##[1:10] 
    (ack && data == $past(saved_data));
endproperty
```

---

## 6. 断言实战技巧

### 6.1 FIFO 断言

```systemverilog
module fifo_assertions #(
    parameter DEPTH = 16
)(
    input logic clk, rst_n,
    input logic wr_en, rd_en,
    input logic full, empty,
    input logic [$clog2(DEPTH):0] count
);
    default clocking cb @(posedge clk);
    endclocking
    default disable iff (!rst_n);
    
    // 满时不写
    AP_NO_WR_WHEN_FULL: assert property (
        full |-> !wr_en
    ) else $error("Write when FIFO full!");
    
    // 空时不读
    AP_NO_RD_WHEN_EMPTY: assert property (
        empty |-> !rd_en
    ) else $error("Read when FIFO empty!");
    
    // 满和空互斥
    AP_FULL_EMPTY_MUTEX: assert property (
        !(full && empty)
    ) else $error("FIFO both full and empty!");
    
    // 写入时计数增加
    AP_WR_INCR: assert property (
        (wr_en && !rd_en && !full) |=> 
        count == $past(count) + 1
    );
    
    // 读取时计数减少
    AP_RD_DECR: assert property (
        (rd_en && !wr_en && !empty) |=> 
        count == $past(count) - 1
    );
    
    // 同时读写时计数不变
    AP_WR_RD_SAME: assert property (
        (wr_en && rd_en && !full && !empty) |=> 
        count == $past(count)
    );
endmodule
```

### 6.2 状态机断言

```systemverilog
typedef enum logic [2:0] {
    IDLE    = 3'b000,
    FETCH   = 3'b001,
    DECODE  = 3'b010,
    EXEC    = 3'b011,
    WRITE   = 3'b100
} state_t;

module fsm_assertions (
    input logic clk, rst_n,
    input state_t state, next_state,
    input logic start, done
);
    default clocking cb @(posedge clk);
    endclocking
    default disable iff (!rst_n);
    
    // 复位后进入 IDLE
    AP_RESET_IDLE: assert property (
        $fell(rst_n) |=> state == IDLE
    );
    
    // 从 IDLE 开始需要 start 信号
    AP_IDLE_TRANS: assert property (
        state == IDLE |-> (start |=> state == FETCH)
    );
    
    // 状态转换合法
    AP_LEGAL_TRANS: assert property (
        state == IDLE   |=> next_state inside {IDLE, FETCH}   and
        state == FETCH  |=> next_state inside {DECODE, IDLE}  and
        state == DECODE |=> next_state inside {EXEC, IDLE}    and
        state == EXEC   |=> next_state inside {WRITE, IDLE}   and
        state == WRITE  |=> next_state inside {IDLE}
    );
    
    // 最终回到 IDLE
    AP_BACK_TO_IDLE: assert property (
        start |-> ##[1:100] state == IDLE
    ) else $error("FSM stuck!");
    
    // 覆盖所有状态
    CP_ALL_STATES: cover property (
        state == IDLE   ##1 
        state == FETCH  ##1 
        state == DECODE ##1 
        state == EXEC   ##1 
        state == WRITE  ##1 
        state == IDLE
    );
endmodule
```

### 6.3 总线协议断言

```systemverilog
// APB 总线断言示例
module apb_assertions (
    input logic pclk, preset_n,
    input logic psel, penable, pwrite,
    input logic [31:0] paddr, pwdata, prdata,
    input logic pready
);
    default clocking cb @(posedge pclk);
    endclocking
    default disable iff (!preset_n);
    
    // SETUP → ACCESS 状态转换
    AP_SETUP_ACCESS: assert property (
        psel && !penable |=> psel && penable
    );
    
    // ACCESS 结束后回到 IDLE 或 SETUP
    AP_ACCESS_END: assert property (
        psel && penable && pready |=> 
        (!psel || (psel && !penable))
    );
    
    // 写操作时 pwrite 保持
    AP_WRITE_STABLE: assert property (
        psel && penable && pwrite |-> $stable(pwrite)
    );
    
    // 地址在传输期间稳定
    AP_ADDR_STABLE: assert property (
        psel |-> $stable(paddr) throughout 
        (psel ##1 (psel && penable))
    );
endmodule
```

### 6.4 仲裁器断言

```systemverilog
module arbiter_assertions #(
    parameter NUM_REQ = 4
)(
    input logic clk, rst_n,
    input logic [NUM_REQ-1:0] req,
    input logic [NUM_REQ-1:0] gnt
);
    default clocking cb @(posedge clk);
    endclocking
    default disable iff (!rst_n);
    
    // One-hot grant
    AP_ONEHOT_GNT: assert property (
        |gnt |-> $onehot(gnt)
    ) else $error("Grant not one-hot!");
    
    // 只授权有请求的
    AP_GNT_HAS_REQ: assert property (
        gnt[0] |-> req[0] and
        gnt[1] |-> req[1] and
        gnt[2] |-> req[2] and
        gnt[3] |-> req[3]
    );
    
    // 请求最终会被授权
    AP_NO_STARVATION: assert property (
        req[0] |-> ##[1:100] gnt[0]
    ) else $error("Request 0 starved!");
    
    // 公平仲裁覆盖
    CP_FAIRNESS: cover property (
        gnt[0] ##[1:10] gnt[1] ##[1:10] gnt[2] ##[1:10] gnt[3]
    );
endmodule
```

---

## 7. 断言覆盖

### 7.1 覆盖属性

```systemverilog
// 统计事件发生次数
cover property (req ##1 ack);

// 带标签的覆盖
CP_HANDSHAKE: cover property (req |-> ##[1:5] ack);

// 覆盖所有状态转换
cover property (state == IDLE ##1 state == FETCH);
cover property (state == FETCH ##1 state == DECODE);
```

### 7.2 覆盖序列

```systemverilog
// 覆盖特定序列
sequence s_burst;
    start ##1 data[*4] ##1 stop;
endsequence

cover property (s_burst);

// 覆盖带参数的序列
cover property (
    req && (addr inside {[0:255]})
);
```

---

## 8. 断言调试

### 8.1 断言控制

```systemverilog
// 禁用特定断言
initial begin
    $assertoff(0, top.dut.ap_check);  // 暂停
    $asserton(0, top.dut.ap_check);   // 恢复
    $assertkill(0, top.dut.ap_check); // 终止
end

// 运行时控制
initial begin
    // 禁用所有断言
    $assertoff();
    
    // 仿真稳定后启用
    #100;
    $asserton();
end
```

### 8.2 断言消息

```systemverilog
// 自定义消息
AP_CHECK: assert property (req |-> ack)
    $display("PASS at %0t", $time);
else
    $error("FAIL: req=%b, ack=%b at time %0t", 
           $past(req), ack, $time);

// 使用 $info 和 $warning
AP_WARN: assert property (timeout < MAX_TIMEOUT)
    $info("Timeout within limit");
else
    $warning("Timeout exceeded limit");
```

### 8.3 断言密度控制

```systemverilog
// 只在关键时刻检查
assert property (
    enable_check |-> (data == expected)
);

// 控制检查使能
logic enable_check;
initial enable_check = 0;

// 仿真稳定后启用
initial begin
    #1000;
    enable_check = 1;
end
```

---

## 参考书籍

- SystemVerilog for Verification 3rd Edition, Chris Spear & Greg Tumbush
- Verification Methodology Manual for SystemVerilog
- IEEE 1800 SystemVerilog LRM

---

*整理自验证知识库*
