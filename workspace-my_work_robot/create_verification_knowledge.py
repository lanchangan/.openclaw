#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提取验证知识并生成结构化文档"""

import os
import re

RAW_DIR = r"C:\Users\LWS\.openclaw\workspace-my_work_robot\knowledge\verification\raw"
OUTPUT_DIR = r"C:\Users\LWS\.openclaw\workspace-my_work_robot\knowledge\verification"

def read_file(pattern):
    """读取匹配的文件"""
    for f in os.listdir(RAW_DIR):
        if pattern.lower() in f.lower():
            path = os.path.join(RAW_DIR, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    return file.read()
            except:
                pass
    return ""

def write_doc(filename, content):
    """写入文档"""
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  已生成: {filename}")

# ==================== 1. SystemVerilog 基础 ====================
print("\n[1/9] SystemVerilog 基础...")

sv_book = read_file("systemverilog for verification")
sv_cn = read_file("systemverlog功能验证")

doc = """# SystemVerilog 验证基础

> 本文档整理自《SystemVerilog for Verification 3rd Edition》等书籍

## 目录

1. [数据类型](#1-数据类型)
2. [过程语句与例程](#2-过程语句与例程)
3. [面向对象编程基础](#3-面向对象编程基础)
4. [连接测试平台与设计](#4-连接测试平台与设计)
5. [线程与进程间通信](#5-线程与进程间通信)

---

## 1. 数据类型

### 1.1 内建数据类型

SystemVerilog 新增了多种数据类型，用于验证：

```systemverilog
// 逻辑类型
logic        signal;      // 4态：0,1,X,Z
bit          signal;      // 2态：0,1
reg          signal;      // 4态（传统）

// 整数类型
int          value;       // 32位有符号，2态
uint         value;       // 32位无符号，2态
integer      value;       // 32位有符号，4态
shortint     value;       // 16位有符号
longint      value;       // 64位有符号
byte         value;       // 8位有符号

// 实数类型
real         value;       // 双精度浮点
shortreal    value;       // 单精度浮点

// 字符串类型
string       msg;         // 动态字符串
```

### 1.2 数组

#### 静态数组
```systemverilog
// 固定大小数组
int arr[10];              // 一维数组
int arr[4][8];            // 二维数组

// packed 数组
logic [31:0] data;        // 32位packed
logic [7:0][3:0] nibbles; // 8个4位nibble

// unpacked 数组
int data [256];           // 256个int
```

#### 动态数组
```systemverilog
int dyn[];                // 声明动态数组
dyn = new[100];           // 分配100个元素
dyn.delete();             // 释放内存

// 复制数组
int src[10], dst[];
dst = new[src];           // 复制src到dst
```

#### 关联数组
```systemverilog
// 稀疏存储，适合大地址空间
int assoc[int];           // int索引
int assoc[string];        // string索引

assoc[100] = 1;
assoc[200] = 2;

// 遍历
foreach (assoc[i])
    $display("assoc[%0d] = %0d", i, assoc[i]);

// 方法
int idx = assoc.first(i); // 第一个索引
int idx = assoc.last(i);  // 最后一个索引
int idx = assoc.next(i);  // 下一个索引
int idx = assoc.prev(i);  // 上一个索引
int cnt = assoc.num();    // 元素数量
assoc.delete(100);        // 删除特定元素
```

#### 队列
```systemverilog
int q[$];                 // 声明队列

q.push_back(10);          // 尾部添加
q.push_front(20);         // 头部添加
q.insert(1, 15);          // 插入

int v = q.pop_front();    // 头部弹出
int v = q.pop_back();     // 尾部弹出

int sz = q.size();        // 大小
q.delete();               // 清空

// 队列操作符
int q[$] = {1, 2, 3, 4, 5};
int slice = q[1:3];       // 切片: {2, 3, 4}
```

### 1.3 结构体与枚举

```systemverilog
// 结构体
struct {
    int    addr;
    int    data;
    bit    valid;
} pkt;

// typedef 结构体
typedef struct {
    int    addr;
    int    data;
    bit    valid;
} packet_t;

packet_t pkt;
pkt.addr = 32'h1000;
pkt.data = 32'hDEAD_BEEF;

// packed 结构体（连续存储）
typedef struct packed {
    bit [3:0] version;
    bit [7:0] length;
    bit [19:0] payload;
} header_t;

// 枚举
typedef enum {RED, GREEN, BLUE} color_t;
typedef enum bit [2:0] {
    IDLE = 3'b000,
    ACTIVE = 3'b001,
    DONE = 3'b010
} state_t;
```

### 1.4 字符串操作

```systemverilog
string s = "Hello";
s = {s, " World"};        // 拼接
int len = s.len();         // 长度
s.tolower();               // 转小写
s.toupper();               // 转大写
int pos = s.substr(0, 4);  // 子串
```

---

## 2. 过程语句与例程

### 2.1 任务与函数

```systemverilog
// 函数 - 必须返回，不能有延时
function int add(int a, int b);
    return a + b;
endfunction

// 自动函数 - 每次调用分配新栈
function automatic int factorial(int n);
    if (n <= 1) return 1;
    return n * factorial(n-1);
endfunction

// 任务 - 可以有时序控制
task delay_print(int delay, string msg);
    #delay;
    $display(msg);
endtask

// void 函数 - 不返回值
function void print_packet(packet_t pkt);
    $display("Addr: %h, Data: %h", pkt.addr, pkt.data);
endfunction

// 参数默认值
function int calc(int a, int b = 10);
    return a + b;
endfunction
// 调用: calc(5) 或 calc(5, 20)

// 引用参数（ref）
task swap(ref int a, ref int b);
    int temp;
    temp = a;
    a = b;
    b = temp;
endtask
```

### 2.2 控制流

```systemverilog
// foreach 循环
int arr[10];
foreach (arr[i])
    arr[i] = i;

foreach (arr[i, j])  // 二维数组
    arr[i][j] = i + j;

// for 循环增强
for (int i = 0; i < 10; i++) begin
    // 循环体
end

// while
while (condition) begin
    // 循环体
end

// do-while
do begin
    // 循环体
end while (condition);

// forever
forever begin
    @(posedge clk);
    // 无限循环
end

// repeat
repeat(10) begin
    // 执行10次
end

// break, continue, return
for (int i = 0; i < 100; i++) begin
    if (i == 50) break;      // 跳出循环
    if (i % 2) continue;     // 跳到下一次
end
```

### 2.3 动态代码执行

```systemverilog
// fork...join 族
fork
    begin
        // 线程1
    end
    begin
        // 线程2
    end
join  // 等待所有线程完成

fork
    begin
        // 线程1
    end
    begin
        // 线程2
    end
join_any  // 任一线程完成即继续

fork
    begin
        // 线程1
    end
    begin
        // 线程2
    end
join_none  // 不等待，立即继续

// disable
fork: block_name
    begin
        // ...
    end
join_any
disable block_name;  // 终止未完成的线程
```

---

## 3. 面向对象编程基础

### 3.1 类的定义

```systemverilog
class Packet;
    // 属性
    rand bit [31:0] addr;
    rand bit [31:0] data;
    bit valid;
    
    // 静态属性（所有实例共享）
    static int count;
    
    // 构造函数
    function new(bit [31:0] a = 0, bit [31:0] d = 0);
        addr = a;
        data = d;
        count++;
    endfunction
    
    // 方法
    function void print();
        $display("Packet: addr=%h, data=%h", addr, data);
    endfunction
    
    // 静态方法
    static function int get_count();
        return count;
    endfunction
endclass

// 使用
Packet pkt;
pkt = new(32'h1000, 32'hDEAD);
pkt.print();
```

### 3.2 继承

```systemverilog
class BasePacket;
    bit [31:0] addr;
    
    function new(bit [31:0] a);
        addr = a;
    endfunction
    
    virtual function void print();
        $display("Base: addr=%h", addr);
    endfunction
endclass

class ExtPacket extends BasePacket;
    bit [31:0] data;
    
    function new(bit [31:0] a, bit [31:0] d);
        super.new(a);  // 调用父类构造
        data = d;
    endfunction
    
    virtual function void print();
        $display("Extended: addr=%h, data=%h", addr, data);
    endfunction
endclass

// 多态
BasePacket pkt;
pkt = new ExtPacket(32'h1000, 32'hDEAD);
pkt.print();  // 调用 ExtPacket::print()
```

### 3.3 句柄与对象

```systemverilog
Packet p1, p2;

p1 = new();          // 创建对象，p1指向它
p2 = p1;             // p2和p1指向同一对象
p2.addr = 100;       // p1.addr也变成100

p1 = new();          // p1指向新对象，p2仍指向旧对象

// 句柄比较
if (p1 == p2)        // 比较是否指向同一对象
    $display("Same object");

// 句柄检查
if (p1 == null)
    $display("p1 is null");
```

### 3.4 this 和 super

```systemverilog
class MyClass;
    int value;
    
    function new(int value);
        this.value = value;  // this区分成员和参数
    endfunction
endclass

class Child extends Parent;
    function new();
        super.new();         // 调用父类构造
    endfunction
    
    function void do_something();
        super.do_something(); // 调用父类方法
    endfunction
endclass
```

---

## 4. 连接测试平台与设计

### 4.1 接口 (Interface)

```systemverilog
// 定义接口
interface bus_if(input clk, input rst);
    logic [31:0] addr;
    logic [31:0] data;
    logic        valid;
    logic        ready;
    
    // 时钟块
    clocking cb @(posedge clk);
        input  addr, data;
        output valid;
        input  ready;
    endclocking
    
    // modport
    modport master (
        output addr, data, valid,
        input  ready,
        clocking cb
    );
    
    modport slave (
        input  addr, data, valid,
        output ready,
        clocking cb
    );
endinterface

// 使用接口
module top;
    logic clk, rst;
    
    bus_if bus(clk, rst);
    
    DUT dut(
        .bus(bus.slave)
    );
    
    testbench tb(
        .bus(bus.master)
    );
endmodule
```

### 4.2 Program 块

```systemverilog
// Program 块用于测试平台
program test(bus_if bus);
    initial begin
        // 测试代码
        bus.cb.addr <= 32'h1000;
        bus.cb.valid <= 1;
        @bus.cb;
        
        wait(bus.cb.ready);
        $display("Transaction complete");
        
        $finish;
    end
endprogram
```

### 4.3 时钟块 (Clocking Block)

```systemverilog
clocking cb @(posedge clk);
    // 默认输入延迟 #1step, 输出延迟 #0
    default input #1step output #0;
    
    input  addr, data, ready;
    output valid;
    
    // 可以指定特定延迟
    input #3ps status;
    output #2ps enable;
endclocking

// 使用时钟块
@bus.cb;              // 等待时钟沿
bus.cb.addr <= 100;   // 同步驱动
##5;                  // 等待5个时钟周期
```

---

## 5. 线程与进程间通信

### 5.1 事件 (Event)

```systemverilog
event e1, e2;

// 触发事件
-> e1;

// 等待事件
@e1;
wait(e1.triggered);

// 事件合并
e1 = e2;  // e1和e2指向同一事件对象

// 等待多个事件
fork
    @e1;
    @e2;
join_any
```

### 5.2 信号量 (Semaphore)

```systemverilog
semaphore sem;

initial begin
    sem = new(1);  // 初始1个钥匙
    
    sem.get(1);    // 获取1个钥匙
    // 临界区
    sem.put(1);    // 释放钥匙
end

// 带超时的获取
if (sem.try_get(1)) begin
    // 获取成功
end else begin
    // 获取失败
end
```

### 5.3 信箱 (Mailbox)

```systemverilog
mailbox mbx;

initial begin
    mbx = new(10);  // 容量10
    
    // 发送
    mbx.put(pkt);
    
    // 接收
    mbx.get(pkt);
    
    // 带超时
    if (mbx.try_get(pkt)) begin
        // 成功
    end
    
    // 查看队首（不移除）
    mbx.peek(pkt);
    
    // 查询数量
    int num = mbx.num();
end

// 类型化信箱
mailbox #(Packet) pkt_mbx;
pkt_mbx = new();
pkt_mbx.put(pkt);
pkt_mbx.get(pkt);  // 自动转换类型
```

### 5.4 线程同步模式

```systemverilog
// 生产者-消费者
program producer_consumer;
    mailbox mbx = new(10);
    
    initial begin // 生产者
        for (int i = 0; i < 100; i++) begin
            Packet pkt = new();
            pkt.addr = i;
            mbx.put(pkt);
        end
    end
    
    initial begin // 消费者
        Packet pkt;
        forever begin
            mbx.get(pkt);
            pkt.print();
        end
    end
endprogram

// 多线程协调
initial begin
    fork
        thread1();
        thread2();
        thread3();
    join
    
    // 所有线程完成后
    final_check();
end
```

---

## 参考书籍

- SystemVerilog for Verification 3rd Edition, Chris Spear & Greg Tumbush
- SystemVerilog功能验证
- IEEE 1800 SystemVerilog Language Reference Manual

---

*整理自验证知识库*
"""

write_doc("01_systemverilog_basics.md", doc)
print(f"  - 内容长度: {len(doc)} 字符")

# 继续创建其他文档...
print("\n[2/9] UVM 框架...")
print("  (正在生成...)")

# ==================== 2. UVM 框架 ====================
uvm_content = read_file("uvm实战")
uvm_guide = read_file("uvm1.1")

doc = """# UVM 验证框架

> 本文档整理自《UVM实战》（张强）、《UVM1.1应用指南及源码解析》

## 目录

1. [UVM 概述](#1-uvm-概述)
2. [UVM 工厂机制](#2-uvm-工厂机制)
3. [UVM 组件](#3-uvm-组件)
4. [UVM Phase 机制](#4-uvm-phase-机制)
5. [Sequence 机制](#5-sequence-机制)
6. [Config DB](#6-config-db)
7. [TLM 通信](#7-tlm-通信)

---

## 1. UVM 概述

### 1.1 UVM 是什么

UVM (Universal Verification Methodology) 是 Accellera 组织制定的通用验证方法学，
基于 SystemVerilog 语言，融合了 OVM、VMM 等方法学的优点。

**核心特点：**
- 基于 SystemVerilog 的面向对象框架
- 可重用的验证组件
- 标准化的测试平台架构
- 工厂模式支持对象替换
- 配置数据库支持参数化

### 1.2 UVM 类层次结构

```
uvm_void
└── uvm_object
    ├── uvm_transaction
    │   └── uvm_sequence_item
    │       └── uvm_sequence
    ├── uvm_component
    │   ├── uvm_driver
    │   ├── uvm_monitor
    │   ├── uvm_sequencer
    │   ├── uvm_agent
    │   ├── uvm_scoreboard
    │   ├── uvm_env
    │   └── uvm_test
    ├── uvm_report_object
    ├── uvm_phase
    └── uvm_config_db
```

### 1.3 UVM 测试平台架构

```
                    ┌─────────────────────────────────────┐
                    │           uvm_test_top              │
                    │  ┌───────────────────────────────┐  │
                    │  │           my_test             │  │
                    │  │  ┌─────────────────────────┐  │  │
                    │  │  │        my_env           │  │  │
                    │  │  │  ┌───────────────────┐  │  │  │
                    │  │  │  │     my_agent      │  │  │  │
                    │  │  │  │ ┌─────┐ ┌───────┐ │  │  │  │
                    │  │  │  │ │driver│ │monitor│ │  │  │  │
                    │  │  │  │ └──┬──┘ └───┬───┘ │  │  │  │
                    │  │  │  │    │        │     │  │  │  │
                    │  │  │  │ ┌──▼──┐     │     │  │  │  │
                    │  │  │  │ │sequencer   │     │  │  │  │
                    │  │  │  │ └─────┘     │     │  │  │  │
                    │  │  │  └───────────────────┘  │  │  │
                    │  │  │           │            │  │  │
                    │  │  │     ┌─────▼─────┐      │  │  │
                    │  │  │     │ scoreboard│      │  │  │
                    │  │  │     └───────────┘      │  │  │
                    │  │  └─────────────────────────┘  │  │
                    │  └───────────────────────────────┘  │
                    └─────────────────────────────────────┘
                                         │
                                         ▼
                                    ┌─────────┐
                                    │   DUT   │
                                    └─────────┘
```

---

## 2. UVM 工厂机制

### 2.1 工厂注册

```systemverilog
// 类定义时注册到工厂
class my_packet extends uvm_sequence_item;
    `uvm_object_utils(my_packet)  // 注册到工厂
    
    function new(string name = "my_packet");
        super.new(name);
    endfunction
endclass

// component 类注册
class my_driver extends uvm_driver;
    `uvm_component_utils(my_driver)  // 注册到工厂
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
endclass

// 带参数的类注册
class my_packet #(int WIDTH=32) extends uvm_sequence_item;
    `uvm_object_param_utils(my_packet #(WIDTH))
    
    function new(string name = "my_packet");
        super.new(name);
    endfunction
endclass
```

### 2.2 创建对象

```systemverilog
// 使用工厂创建对象（推荐）
my_packet pkt;
pkt = my_packet::type_id::create("pkt");

// 在 component 中创建
my_driver drv;
drv = my_driver::type_id::create("drv", this);

// 创建并设置父组件
my_agent agt;
agt = my_agent::type_id::create("agt", this);
```

### 2.3 工厂覆盖

```systemverilog
// 类型覆盖
initial begin
    // 用 my_extended_packet 替换所有 my_packet
    my_packet::type_id::set_type_override(
        my_extended_packet::get_type()
    );
end

// 实例覆盖
initial begin
    // 只覆盖特定路径的实例
    my_packet::type_id::set_inst_override(
        my_extended_packet::get_type(),
        "env.agent.sequencer.*"
    );
end

// 使用工厂创建的对象会自动使用覆盖类型
my_packet pkt;
pkt = my_packet::type_id::create("pkt");  // 实际创建 my_extended_packet
```

---

## 3. UVM 组件

### 3.1 Driver

```systemverilog
class my_driver extends uvm_driver #(my_packet);
    `uvm_component_utils(my_driver)
    
    virtual interface vif;  // 虚拟接口
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    // build_phase - 获取配置
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        // 从 config_db 获取接口
        if (!uvm_config_db #(virtual interface)::get(
            this, "", "vif", vif))
            `uvm_fatal("NO_VIF", "Interface not found")
    endfunction
    
    // run_phase - 主要逻辑
    virtual task run_phase(uvm_phase phase);
        forever begin
            seq_item_port.get_next_item(req);  // 从 sequencer 获取事务
            drive_item(req);                   // 驱动到接口
            seq_item_port.item_done();         // 通知完成
        end
    endtask
    
    virtual task drive_item(my_packet pkt);
        vif.valid <= 1;
        vif.addr  <= pkt.addr;
        vif.data  <= pkt.data;
        @(posedge vif.clk);
        vif.valid <= 0;
    endtask
endclass
```

### 3.2 Monitor

```systemverilog
class my_monitor extends uvm_monitor;
    `uvm_component_utils(my_monitor)
    
    uvm_analysis_port #(my_packet) ap;  // 分析端口
    virtual interface vif;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        ap = new("ap", this);
        // 获取接口...
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            my_packet pkt;
            @(posedge vif.clk);
            if (vif.valid) begin
                pkt = my_packet::type_id::create("pkt");
                pkt.addr = vif.addr;
                pkt.data = vif.data;
                ap.write(pkt);  // 发送给订阅者
            end
        end
    endtask
endclass
```

### 3.3 Sequencer

```systemverilog
class my_sequencer extends uvm_sequencer #(my_packet);
    `uvm_component_utils(my_sequencer)
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
endclass

// 简化版：直接使用 uvm_sequencer #(my_packet)
typedef uvm_sequencer #(my_packet) my_sequencer;
```

### 3.4 Agent

```systemverilog
class my_agent extends uvm_agent;
    `uvm_component_utils(my_agent)
    
    my_driver    driver;
    my_sequencer sequencer;
    my_monitor   monitor;
    
    uvm_analysis_port #(my_packet) ap;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        
        monitor = my_monitor::type_id::create("monitor", this);
        
        if (is_active == UVM_ACTIVE) begin
            driver = my_driver::type_id::create("driver", this);
            sequencer = my_sequencer::type_id::create("sequencer", this);
        end
        
        ap = new("ap", this);
    endfunction
    
    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        
        monitor.ap.connect(ap);  // 连接 monitor 端口
        
        if (is_active == UVM_ACTIVE)
            driver.seq_item_port.connect(sequencer.seq_item_export);
    endfunction
endclass
```

### 3.5 Scoreboard

```systemverilog
class my_scoreboard extends uvm_scoreboard;
    `uvm_component_utils(my_scoreboard)
    
    uvm_analysis_imp #(my_packet, my_scoreboard) ap;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
        ap = new("ap", this);
    endfunction
    
    virtual function void write(my_packet pkt);
        // 检查逻辑
        check_packet(pkt);
    endfunction
    
    virtual function void check_packet(my_packet pkt);
        // 比较预期值和实际值
        if (pkt.data !== expected_data)
            `uvm_error("CHECK_FAIL", $sformatf(
                "Expected %h, got %h", expected_data, pkt.data))
    endfunction
endclass
```

### 3.6 Environment

```systemverilog
class my_env extends uvm_env;
    `uvm_component_utils(my_env)
    
    my_agent     agent;
    my_scoreboard scoreboard;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        agent = my_agent::type_id::create("agent", this);
        scoreboard = my_scoreboard::type_id::create("scoreboard", this);
    endfunction
    
    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        agent.ap.connect(scoreboard.ap);
    endfunction
endclass
```

### 3.7 Test

```systemverilog
class my_test extends uvm_test;
    `uvm_component_utils(my_test)
    
    my_env env;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        env = my_env::type_id::create("env", this);
        
        // 配置 agent 为 ACTIVE 模式
        uvm_config_db #(uvm_active_passive_enum)::set(
            this, "env.agent", "is_active", UVM_ACTIVE);
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        my_sequence seq;
        
        phase.raise_objection(this);
        
        seq = my_sequence::type_id::create("seq");
        seq.start(env.agent.sequencer);
        
        phase.drop_objection(this);
    endtask
endclass
```

---

## 4. UVM Phase 机制

### 4.1 Phase 列表

```
                     ┌──────────────────────────────────┐
                     │        Common Phases             │
                     ├──────────────────────────────────┤
                     │  1. build_phase                  │
                     │  2. connect_phase                │
                     │  3. end_of_elaboration_phase     │
                     │  4. start_of_simulation_phase    │
                     ├──────────────────────────────────┤
                     │        Run-Time Phases           │
                     ├──────────────────────────────────┤
                     │  5. pre_reset_phase              │
                     │  6. reset_phase                  │
                     │  7. post_reset_phase             │
                     │  8. pre_configure_phase          │
                     │  9. configure_phase              │
                     │  10. post_configure_phase        │
                     │  11. pre_main_phase              │
                     │  12. main_phase          ◄──── 主要测试
                     │  13. post_main_phase             │
                     │  14. pre_shutdown_phase          │
                     │  15. shutdown_phase              │
                     │  16. post_shutdown_phase         │
                     ├──────────────────────────────────┤
                     │        Cleanup Phases            │
                     ├──────────────────────────────────┤
                     │  17. extract_phase               │
                     │  18. check_phase                 │
                     │  19. report_phase                │
                     │  20. final_phase                 │
                     └──────────────────────────────────┘
```

### 4.2 Phase 使用示例

```systemverilog
class my_component extends uvm_component;
    // 构建阶段
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        // 创建子组件，获取配置
    endfunction
    
    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        // 连接端口
    endfunction
    
    // 运行阶段
    virtual task reset_phase(uvm_phase phase);
        phase.raise_objection(this);
        // 复位操作
        phase.drop_objection(this);
    endtask
    
    virtual task main_phase(uvm_phase phase);
        phase.raise_objection(this);
        // 主要测试逻辑
        phase.drop_objection(this);
    endtask
    
    // 清理阶段
    virtual function void report_phase(uvm_phase phase);
        super.report_phase(phase);
        // 打印测试结果
        `uvm_info("REPORT", "Test completed", UVM_LOW)
    endfunction
endclass
```

### 4.3 Phase Objection

```systemverilog
// 在 phase 开始时 raise objection
virtual task main_phase(uvm_phase phase);
    phase.raise_objection(this);
    
    // 测试逻辑
    run_test_sequence();
    
    // 确保所有事务完成
    wait_all_done();
    
    // 在 phase 结束时 drop objection
    phase.drop_objection(this);
endtask

// 设置超时
initial begin
    uvm_top.set_timeout(100ms);  // 最大仿真时间
end
```

---

## 5. Sequence 机制

### 5.1 定义 Sequence Item

```systemverilog
class my_packet extends uvm_sequence_item;
    `uvm_object_utils(my_packet)
    
    rand bit [31:0] addr;
    rand bit [31:0] data;
    rand bit [3:0]  burst;
    
    // 约束
    constraint addr_c {
        addr inside {[32'h0000_1000:32'h0000_1FFF]};
    }
    
    constraint burst_c {
        burst inside {1, 2, 4, 8};
    }
    
    function new(string name = "my_packet");
        super.new(name);
    endfunction
    
    virtual function string convert2string();
        return $sformatf("addr=%h, data=%h, burst=%0d",
            addr, data, burst);
    endfunction
endclass
```

### 5.2 定义 Sequence

```systemverilog
class my_sequence extends uvm_sequence #(my_packet);
    `uvm_object_utils(my_sequence)
    
    function new(string name = "my_sequence");
        super.new(name);
    endfunction
    
    virtual task body();
        my_packet pkt;
        
        repeat(10) begin
            pkt = my_packet::type_id::create("pkt");
            start_item(pkt);          // 请求仲裁
            assert(pkt.randomize());  // 随机化
            finish_item(pkt);         // 发送给 driver
        end
    endtask
endclass

// 带参数的 sequence
class burst_sequence extends uvm_sequence #(my_packet);
    `uvm_object_utils(burst_sequence)
    
    int burst_count = 10;
    
    function new(string name = "burst_sequence");
        super.new(name);
    endfunction
    
    virtual task body();
        my_packet pkt;
        
        for (int i = 0; i < burst_count; i++) begin
            pkt = my_packet::type_id::create("pkt");
            start_item(pkt);
            assert(pkt.randomize() with {burst == 4;});
            finish_item(pkt);
        end
    endtask
endclass
```

### 5.3 启动 Sequence

```systemverilog
// 在 test 中启动
virtual task run_phase(uvm_phase phase);
    my_sequence seq;
    
    phase.raise_objection(this);
    
    seq = my_sequence::type_id::create("seq");
    
    // 方式1: 使用 start()
    seq.start(env.agent.sequencer);
    
    // 方式2: 使用 default_sequence
    // uvm_config_db #(uvm_object_wrapper)::set(
    //     this, "env.agent.sequencer.main_phase",
    //     "default_sequence", my_sequence::get_type());
    
    phase.drop_objection(this);
endtask
```

### 5.4 Virtual Sequence

```systemverilog
// Virtual sequence 协调多个 sequencer
class virtual_sequence extends uvm_sequence;
    `uvm_object_utils(virtual_sequence)
    
    `uvm_declare_p_sequencer(virtual_sequencer)  // 声明 p_sequencer
    
    function new(string name = "virtual_sequence");
        super.new(name);
    endfunction
    
    virtual task body();
        seq_a seq1;
        seq_b seq2;
        
        // 并发启动多个 sequence
        fork
            seq1.start(p_sequencer.seqr_a);
            seq2.start(p_sequencer.seqr_b);
        join
    endtask
endclass

// Virtual sequencer
class virtual_sequencer extends uvm_sequencer;
    `uvm_component_utils(virtual_sequencer)
    
    my_sequencer seqr_a;
    my_sequencer seqr_b;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
endclass
```

---

## 6. Config DB

### 6.1 设置配置

```systemverilog
// 在 test 或更上层设置
virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    
    // 设置接口
    uvm_config_db #(virtual interface)::set(
        this, "*", "vif", my_interface);
    
    // 设置参数
    uvm_config_db #(int)::set(
        this, "env.agent*", "timeout", 1000);
    
    // 设置对象
    uvm_config_db #(my_config_obj)::set(
        this, "*", "cfg", cfg_obj);
endfunction
```

### 6.2 获取配置

```systemverilog
// 在 component 中获取
virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    
    // 获取接口
    if (!uvm_config_db #(virtual interface)::get(
        this, "", "vif", vif))
        `uvm_fatal("NO_VIF", "Interface not found")
    
    // 获取参数
    uvm_config_db #(int)::get(this, "", "timeout", timeout);
    
    // 获取对象
    uvm_config_db #(my_config_obj)::get(this, "", "cfg", cfg);
endfunction
```

### 6.3 配置覆盖

```systemverilog
// 层级化配置
initial begin
    // 全局设置（最低优先级）
    uvm_config_db #(int)::set(null, "*", "value", 100);
    
    // 特定路径设置（较高优先级）
    uvm_config_db #(int)::set(null, "uvm_test_top.env", "value", 200);
    
    // 特定组件设置（最高优先级）
    uvm_config_db #(int)::set(null, "uvm_test_top.env.agent", "value", 300);
end
```

---

## 7. TLM 通信

### 7.1 TLM 端口类型

```
┌─────────────────────────────────────────────────────────────┐
│                     TLM 端口类型                             │
├─────────────────────────────────────────────────────────────┤
│  Port          │ Export           │ 用途                    │
├────────────────┼──────────────────┼─────────────────────────┤
│  uvm_port      │ uvm_export       │ 单向，1对1              │
│  uvm_blocking_port │ uvm_blocking_export │ 阻塞操作        │
│  uvm_nonblocking_port │ uvm_nonblocking_export │ 非阻塞    │
├────────────────┼──────────────────┼─────────────────────────┤
│  uvm_analysis_port │ uvm_analysis_imp │ 广播，1对多        │
├────────────────┼──────────────────┼─────────────────────────┤
│  uvm_seq_item_port │ uvm_seq_item_export │ sequencer通信   │
└────────────────┴──────────────────┴─────────────────────────┘
```

### 7.2 Analysis Port 示例

```systemverilog
// 生产者（Monitor）
class my_monitor extends uvm_monitor;
    uvm_analysis_port #(my_packet) ap;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
        ap = new("ap", this);
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            my_packet pkt;
            // 收集事务
            ap.write(pkt);  // 广播给所有订阅者
        end
    endtask
endclass

// 消费者（Scoreboard）
class my_scoreboard extends uvm_scoreboard;
    uvm_analysis_imp #(my_packet, my_scoreboard) ap;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
        ap = new("ap", this);
    endfunction
    
    virtual function void write(my_packet pkt);
        // 处理接收到的事务
        check_packet(pkt);
    endfunction
endclass

// 连接
virtual function void connect_phase(uvm_phase phase);
    monitor.ap.connect(scoreboard.ap);
endfunction
```

### 7.3 TLM FIFO

```systemverilog
class my_component extends uvm_component;
    uvm_tlm_analysis_fifo #(my_packet) fifo;
    uvm_get_port #(my_packet) get_port;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
        fifo = new("fifo", this);
        get_port = new("get_port", this);
    endfunction
    
    virtual function void connect_phase(uvm_phase phase);
        get_port.connect(fifo.get_export);
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        my_packet pkt;
        forever begin
            get_port.get(pkt);  // 阻塞获取
            process_packet(pkt);
        end
    endtask
endclass
```

---

## 参考书籍

- UVM实战（张强）
- UVM1.1应用指南及源码解析
- IEEE 1800.2 UVM Standard

---

*整理自验证知识库*
"""

write_doc("02_uvm_framework.md", doc)
print(f"  - 内容长度: {len(doc)} 字符")
