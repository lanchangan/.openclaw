# SystemVerilog 语言标准要点

> 整理自 IEEE Std 1800-2023 SystemVerilog 标准

## 目录

1. [语言概述](#1-语言概述)
2. [数据类型系统](#2-数据类型系统)
3. [面向对象编程](#3-面向对象编程)
4. [并发编程](#4-并发编程)
5. [断言语言](#5-断言语言)
6. [功能覆盖](#6-功能覆盖)
7. [约束随机化](#7-约束随机化)

---

## 1. 语言概述

### 1.1 SystemVerilog 定位

SystemVerilog 是 IEEE 1800 标准定义的硬件描述和验证语言 (HDVL)，融合了：
- **设计描述**: Verilog-2001 的超集
- **验证功能**: 断言、覆盖、随机化
- **面向对象**: 类、继承、多态
- **形式化验证**: 假设、断言

### 1.2 标准演进

| 版本 | 年份 | 主要新增 |
|------|------|---------|
| 1800-2005 | 2005 | 基础 SV，断言 |
| 1800-2009 | 2009 | 与 Verilog 合并 |
| 1800-2012 | 2012 | 增强 OOP，UVM 支持 |
| 1800-2017 | 2017 | 稳定版 |
| 1800-2023 | 2023 | 最新版 |

### 1.3 语言子集

```
SystemVerilog
├── 设计子集
│   ├── 模块 (module)
│   ├── 接口 (interface)
│   ├── 程序 (program)
│   └── 包 (package)
├── 验证子集
│   ├── 类 (class)
│   ├── 随机化 (randomize)
│   ├── 覆盖 (covergroup)
│   └── 断言 (assert)
└── 断言子集
    ├── 立即断言
    ├── 并发断言
    └── 覆盖断言
```

---

## 2. 数据类型系统

### 2.1 类型分类

```
数据类型
├── 标量类型
│   ├── 2态类型: bit, int, byte, shortint, longint
│   ├── 4态类型: logic, reg, integer, time
│   └── 实数类型: real, shortreal
├── 向量类型
│   ├── packed array
│   └── unpacked array
├── 复合类型
│   ├── struct
│   ├── union
│   └── enum
├── 动态类型
│   ├── 动态数组 []
│   ├── 队列 [$]
│   └── 关联数组 [key_type]
└── 字符串类型
    └── string
```

### 2.2 类型兼容性规则

| 规则 | 描述 |
|------|------|
| 赋值兼容 | 2态可赋给4态，反之需显式转换 |
| 位宽匹配 | 高位截断或符号扩展 |
| 符号性 | 有符号和无符号混合运算 |

### 2.3 4态逻辑值

| 值 | 含义 | 用途 |
|---|------|------|
| 0 | 逻辑 0 | 低电平 |
| 1 | 逻辑 1 | 高电平 |
| X | 未知 | 未初始化、冲突 |
| Z | 高阻 | 三态 |

---

## 3. 面向对象编程

### 3.1 类定义规则

```systemverilog
class ClassName;
    // 属性
    rand data_type property_name;
    static data_type static_property;
    
    // 方法
    function return_type method_name(arguments);
        // 方法体
    endfunction
    
    // 约束
    constraint constraint_name {
        // 约束条件
    }
    
    // 覆盖组
    covergroup covergroup_name;
        // 覆盖点
    endcovergroup
endclass
```

### 3.2 继承规则

```systemverilog
// 父类
class BaseClass;
    virtual function void method();
        $display("Base method");
    endfunction
endclass

// 子类
class DerivedClass extends BaseClass;
    virtual function void method();
        $display("Derived method");
    endfunction
endclass

// 多态
BaseClass obj;
obj = DerivedClass::new();
obj.method();  // 调用 DerivedClass::method
```

### 3.3 工厂模式

```systemverilog
// 类型注册
`uvm_object_utils(MyClass)
`uvm_component_utils(MyComponent)

// 创建对象
obj = MyClass::type_id::create("obj");

// 类型覆盖
MyClass::type_id::set_type_override(MyExtendedClass::get_type());
```

---

## 4. 并发编程

### 4.1 进程类型

| 关键字 | 描述 | 用途 |
|--------|------|------|
| fork...join | 等待所有 | 并行执行 |
| fork...join_any | 等待任一 | 超时控制 |
| fork...join_none | 不等待 | 后台任务 |

### 4.2 进程控制

```systemverilog
// 禁用进程块
fork: block_name
    // 进程
join_any
disable block_name;

// 等待进程
fork
    begin: process1
        // ...
    end
    begin: process2
        // ...
    end
join
wait(process1.finished && process2.finished);
```

### 4.3 同步原语

| 类型 | 描述 | 操作 |
|------|------|------|
| event | 事件触发 | ->, @, wait() |
| semaphore | 计数信号量 | get(), put(), try_get() |
| mailbox | 消息队列 | put(), get(), peek(), try_get() |

---

## 5. 断言语言

### 5.1 断言类型

| 类型 | 关键字 | 执行时机 |
|------|--------|---------|
| 立即断言 | assert (expr) | 过程块执行时 |
| 并发断言 | assert property (prop) | 每个时钟沿 |
| 最终断言 | assert final (expr) | 仿真结束时 |

### 5.2 序列操作符

| 操作符 | 描述 | 示例 |
|--------|------|------|
| ##n | 延迟 | a ##2 b |
| ##[m:n] | 范围延迟 | a ##[1:5] b |
| [*n] | 连续重复 | a [*3] |
| [=n] | 非连续重复 | a [=3] |
| [->n] | 匹配重复 | a [->3] |

### 5.3 属性操作符

| 操作符 | 描述 | 示例 |
|--------|------|------|
| \-> | 交叠蕴含 | a -> b |
| => | 非交叠蕴含 | a => b |
| throughout | 贯穿 | a throughout b |
| within | 期间 | a within b |
| intersect | 交集 | a intersect b |

---

## 6. 功能覆盖

### 6.1 覆盖组定义

```systemverilog
covergroup cg_name @(posedge clk);
    // 覆盖点
    cp_name: coverpoint variable {
        bins bin_name = {values};
        bins range_bin = {[low:high]};
        bins trans_bin = (val1 => val2);
    }
    
    // 交叉覆盖
    cross_name: cross cp1, cp2;
endcovergroup
```

### 6.2 Bins 类型

| 类型 | 关键字 | 描述 |
|------|--------|------|
| 显式 bins | bins name = {} | 指定值 |
| 范围 bins | bins name = [a:b] | 值范围 |
| 转换 bins | bins name = (a=>b) | 状态转换 |
| 通配 bins | wildcard bins | 模式匹配 |
| 忽略 bins | ignore_bins | 不统计 |
| 非法 bins | illegal_bins | 报错 |

---

## 7. 约束随机化

### 7.1 约束定义

```systemverilog
class MyClass;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    rand bit [3:0]  burst;
    
    // 约束块
    constraint addr_c {
        addr inside {[32'h0000_1000:32'h0000_1FFF]};
        addr % 4 == 0;  // 4字节对齐
    }
    
    constraint burst_c {
        burst inside {1, 2, 4, 8, 16};
        burst * 4 <= 64;  // 最大64字节
    }
    
    // 条件约束
    constraint mode_c {
        (mode == READ) -> (burst <= 8);
        (mode == WRITE) -> (burst <= 16);
    }
endclass
```

### 7.2 分布约束

```systemverilog
constraint dist_c {
    // 加权分布
    burst dist {1 := 70, 2 := 20, 4 := 10};
    
    // 比例分布
    mode dist {READ := 1, WRITE := 1};
}
```

### 7.3 数组约束

```systemverilog
class ArrayClass;
    rand int arr[];
    
    constraint arr_size_c {
        arr.size inside {[4:16]};
    }
    
    constraint arr_sum_c {
        arr.sum() inside {[100:200]};
    }
    
    constraint arr_unique_c {
        unique {arr};
    }
endclass
```

### 7.4 随机化控制

```systemverilog
// 禁用随机化
obj.rand_mode(0);      // 所有变量
obj.addr.rand_mode(0); // 单个变量

// 禁用约束
obj.constraint_mode(0);        // 所有约束
obj.addr_c.constraint_mode(0); // 单个约束

// 内联约束
obj.randomize() with {addr == 32'h1000;};

// pre/post_randomize
function void pre_randomize();
    // 随机化前处理
endfunction

function void post_randomize();
    // 随机化后处理
endfunction
```

---

## 参考文档

- IEEE Std 1800-2023: SystemVerilog Language Reference Manual
- SystemVerilog for Verification 3rd Edition

---

*整理自协议&标准知识库*
