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
