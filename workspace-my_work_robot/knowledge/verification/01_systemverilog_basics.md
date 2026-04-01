# SystemVerilog 验证基础

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

SystemVerilog 新增了多种数据类型用于验证：

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
```

#### 关联数组
```systemverilog
// 稀疏存储，适合大地址空间
int assoc[int];           // int索引
int assoc[string];        // string索引

assoc[100] = 1;

// 遍历
foreach (assoc[i])
    $display("assoc[%0d] = %0d", i, assoc[i]);
```

#### 队列
```systemverilog
int q[$];                 // 声明队列

q.push_back(10);          // 尾部添加
q.push_front(20);         // 头部添加
int v = q.pop_front();    // 头部弹出

int sz = q.size();        // 大小
q.delete();               // 清空
```

### 1.3 结构体与枚举

```systemverilog
// 结构体
typedef struct {
    int    addr;
    int    data;
    bit    valid;
} packet_t;

packet_t pkt;
pkt.addr = 32'h1000;

// 枚举
typedef enum {RED, GREEN, BLUE} color_t;
typedef enum bit [2:0] {
    IDLE = 3'b000,
    ACTIVE = 3'b001,
    DONE = 3'b010
} state_t;
```

---

## 2. 过程语句与例程

### 2.1 任务与函数

```systemverilog
// 函数 - 必须返回，不能有延时
function int add(int a, int b);
    return a + b;
endfunction

// 任务 - 可以有时序控制
task delay_print(int delay, string msg);
    #delay;
    $display(msg);
endtask

// void 函数
function void print_packet(packet_t pkt);
    $display("Addr: %h, Data: %h", pkt.addr, pkt.data);
endfunction

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
    // ...
join_any  // 任一线程完成即继续

fork
    // ...
join_none  // 不等待，立即继续
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
    
    // 静态属性
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
    
    virtual function void print();
        $display("Base: addr=%h", addr);
    endfunction
endclass

class ExtPacket extends BasePacket;
    bit [31:0] data;
    
    virtual function void print();
        $display("Extended: addr=%h, data=%h", addr, data);
    endfunction
endclass

// 多态
BasePacket pkt;
pkt = new ExtPacket(32'h1000, 32'hDEAD);
pkt.print();  // 调用 ExtPacket::print()
```

---

## 4. 连接测试平台与设计

### 4.1 接口 (Interface)

```systemverilog
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
        output ready
    );
endinterface
```

### 4.2 时钟块 (Clocking Block)

```systemverilog
clocking cb @(posedge clk);
    default input #1step output #0;
    
    input  addr, data, ready;
    output valid;
endclocking

// 使用
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
```

### 5.2 信号量 (Semaphore)

```systemverilog
semaphore sem;

initial begin
    sem = new(1);  // 初始1个钥匙
    
    sem.get(1);    // 获取钥匙
    // 临界区
    sem.put(1);    // 释放钥匙
end
```

### 5.3 信箱 (Mailbox)

```systemverilog
mailbox mbx;

initial begin
    mbx = new(10);  // 容量10
    
    mbx.put(pkt);   // 发送
    mbx.get(pkt);   // 接收
    mbx.peek(pkt);  // 查看（不移除）
end
```

---

*整理自验证知识库*
