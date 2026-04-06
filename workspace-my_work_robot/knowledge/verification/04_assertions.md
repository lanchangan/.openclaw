# 断言技术

> 本文档整理自《SystemVerilog for Verification》《VMM》等书籍

## 目录

1. [断言概述](#1-断言概述)
2. [立即断言](#2-立即断言)
3. [并发断言](#3-并发断言)
4. [序列 (Sequence)](#4-序列-sequence)
5. [属性 (Property)](#5-属性-property)
6. [断言实战技巧](#6-断言实战技巧)

---

## 1. 断言概述

| 类型 | 关键字 | 用途 |
|------|--------|------|
| 立即断言 | assert | 组合逻辑检查，立即执行 |
| 并发断言 | assert property | 时序检查，周期性评估 |
| 覆盖断言 | cover property | 统计事件发生次数 |

---

## 2. 立即断言

```systemverilog
always @(posedge clk) begin
    assert (req || !gnt) 
        $display("PASS");
    else 
        $error("FAIL: Grant without request");
end

// One-hot 检查
assert ($onehot(select)) else $error("Select not one-hot");

// 互斥检查
assert (!(read_en && write_en)) else $error("RW conflict");
```

---

## 3. 并发断言

```systemverilog
// 默认时钟
default clocking cb @(posedge clk);
endclocking

default disable iff (rst_n == 0);

// 并发断言
assert property (req |-> ##[1:3] ack)
else $error("No acknowledgment received");
```

---

## 4. 序列 (Sequence)

### 4.1 序列操作符

```systemverilog
// ##n - 延迟 n 个周期
sequence s1;
    a ##2 b;
endsequence

// ##[m:n] - 延迟范围
sequence s2;
    a ##[1:5] b;
endsequence

// 序列运算
sequence s_and;
    (a ##1 b) and (c ##1 d);
endsequence

sequence s_or;
    (a ##1 b) or (c ##1 d);
endsequence
```

### 4.2 序列方法

```systemverilog
$rose(sig)    // 信号上升
$fell(sig)    // 信号下降
$stable(sig)  // 信号稳定
$past(sig, 2) // 2 周期前的值
$onehot(sig)  // one-hot 检查
```

---

## 5. 属性 (Property)

### 5.1 蕴含操作符

```systemverilog
// |-> 交叠蕴含 (同周期)
property p_overlap;
    req |-> gnt;
endproperty

// |=> 非交叠蕴含 (下一周期)
property p_next_cycle;
    req |=> gnt;
endproperty
```

### 5.2 重复操作符

```systemverilog
// 连续重复 [*n]
property p_consecutive;
    a |-> b[*3];  // b 连续 3 周期
endproperty

// 非连续重复 [=n]
property p_non_consecutive;
    a |-> b[=3];  // b 出现 3 次
endproperty
```

---

## 6. 断言实战技巧

### 6.1 FIFO 断言

```systemverilog
module fifo_assertions (
    input logic clk, rst_n,
    input logic wr_en, rd_en,
    input logic full, empty
);
    default clocking cb @(posedge clk);
    endclocking
    default disable iff (!rst_n);
    
    // 满时不写
    assert property (full |-> !wr_en);
    
    // 空时不读
    assert property (empty |-> !rd_en);
    
    // 满和空互斥
    assert property (!(full && empty));
endmodule
```

### 6.2 状态机断言

```systemverilog
typedef enum {IDLE, FETCH, DECODE, EXECUTE} state_t;

module fsm_assertions (
    input logic clk, rst_n,
    input state_t state
);
    // 从 IDLE 开始
    assert property (@(posedge clk) $rose(rst_n) |=> state == IDLE);
    
    // 最终回到 IDLE
    assert property (@(posedge clk) start |-> ##[1:50] state == IDLE);
endmodule
```

---

*整理自验证知识库*
