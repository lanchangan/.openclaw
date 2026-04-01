# 覆盖率技术

> 本文档整理自《SystemVerilog for Verification》《VMM》等书籍

## 目录

1. [覆盖率概述](#1-覆盖率概述)
2. [代码覆盖率](#2-代码覆盖率)
3. [功能覆盖率](#3-功能覆盖率)
4. [覆盖组 (Covergroup)](#4-覆盖组-covergroup)
5. [交叉覆盖](#5-交叉覆盖)

---

## 1. 覆盖率概述

```
┌─────────────────────────────────────────┐
│           覆盖率类型                     │
├─────────────────────────────────────────┤
│  代码覆盖率                              │
│  ├── 行覆盖率                            │
│  ├── 分支覆盖率                          │
│  ├── 条件覆盖率                          │
│  ├── 翻转覆盖率                          │
│  └── FSM 覆盖率                          │
├─────────────────────────────────────────┤
│  功能覆盖率                              │
│  ├── 数据值覆盖                          │
│  ├── 控制流覆盖                          │
│  └── 边界条件覆盖                        │
└─────────────────────────────────────────┘
```

---

## 2. 代码覆盖率

| 类型 | 目标 | 说明 |
|------|------|------|
| 行覆盖率 | 100% | 所有代码行都应执行 |
| 分支覆盖率 | 100% | 所有 if/else 分支 |
| 条件覆盖率 | 100% | 所有条件的真/假 |
| 翻转覆盖率 | 100% | 信号 0→1 和 1→0 |

---

## 3. 功能覆盖率

```systemverilog
// 定义覆盖组
covergroup cg_transaction;
    cp_addr:  coverpoint tr.addr;
    cp_data:  coverpoint tr.data;
endcovergroup

// 实例化并采样
cg_transaction cg = new();

always @(posedge clk) begin
    if (valid)
        cg.sample();
end
```

---

## 4. 覆盖组 (Covergroup)

### 4.1 Bins 定义

```systemverilog
covergroup cg_bins;
    cp_data: coverpoint data {
        bins zero = {0};
        bins range_0_100 = {[0:100]};
        bins values = {10, 20, 30};
        bins others = default;
    }
endcovergroup
```

### 4.2 条件 Bins

```systemverilog
covergroup cg_conditional;
    cp_addr: coverpoint addr {
        ignore_bins invalid = {[32'hFFFF_FFFF]};
        illegal_bins illegal = {32'hDEAD_BEEF};
    }
endcovergroup
```

---

## 5. 交叉覆盖

```systemverilog
covergroup cg_cross;
    cp_mode: coverpoint mode {
        bins read  = {READ};
        bins write = {WRITE};
    }
    
    cp_size: coverpoint size {
        bins byte = {1};
        bins word = {4};
    }
    
    cross_mode_size: cross cp_mode, cp_size {
        ignore_bins ignore = 
            binsof(cp_mode.read) && binsof(cp_size.byte);
    }
endcovergroup
```

---

*整理自验证知识库*
