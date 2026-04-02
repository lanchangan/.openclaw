# SystemVerilog 验证基础（完整版）

> 本文档整理自《SystemVerilog for Verification 3rd Edition》IEEE 1800-2023 标准

## 目录

1. [数据类型详解](#1-数据类型详解)
2. [过程语句与例程](#2-过程语句与例程)
3. [面向对象编程](#3-面向对象编程)
4. [连接测试平台与设计](#4-连接测试平台与设计)
5. [线程与进程间通信](#5-线程与进程间通信)
6. [高级特性](#6-高级特性)

---

## 1. 数据类型详解

### 1.1 类型系统概述

```
SystemVerilog 数据类型层次
├── 标量类型
│   ├── 2态类型 (无 X/Z)
│   │   ├── bit      - 1位无符号
│   │   ├── byte     - 8位有符号
│   │   ├── shortint - 16位有符号
│   │   ├── int      - 32位有符号
│   │   ├── longint  - 64位有符号
│   │   └── uint     - 32位无符号
│   ├── 4态类型 (含 X/Z)
│   │   ├── logic    - 1位四态
│   │   ├── reg      - 传统四态
│   │   ├── integer  - 32位四态
│   │   └── time     - 64位无符号
│   └── 实数类型
│       ├── real      - 64位双精度
│       └── shortreal - 32位单精度
├── 向量类型
│   ├── packed array   - 连续存储
│   └── unpacked array - 分散存储
├── 动态类型
│   ├── 动态数组   []
│   ├── 队列       [$]
│   └── 关联数组   [key_type]
├── 复合类型
│   ├── struct
│   ├── union
│   └── enum
└── 字符串类型
    └── string
```

### 1.2 2态 vs 4态类型

| 特性 | 2态类型 | 4态类型 |
|------|---------|---------|
| 值域 | {0, 1} | {0, 1, X, Z} |
| 初始值 | 0 | X |
| 用途 | 验证环境 | RTL 设计 |
| 性能 | 更快 | 较慢 |

**类型转换规则**:
```systemverilog
// 4态 → 2态: X/Z 变为 0
logic [3:0] four_state = 4'b10XZ;
bit [3:0] two_state = bit'(four_state);  // 结果: 4'b1000

// 2态 → 4态: 自动转换
int two = 5;
integer four = two;  // 结果: 5
```

### 1.3 数组类型详解

#### 1.3.1 静态数组 (Static Array)

```systemverilog
// 固定大小数组
int arr[10];              // 声明10个元素
int arr[0:9];             // 等价写法

// 多维数组
int arr[4][8];            // 4行8列
int arr[0:3][0:7];        // 等价写法

// Packed 数组（连续存储，适合位操作）
logic [31:0] data;        // 32位 packed
logic [7:0][3:0] nibbles; // 8个4位 nibble

// Unpacked 数组（分散存储）
int data [256];           // 256个 int

// Packed vs Unpacked
// Packed:   [MSB:LSB] 连续存储，可整体赋值
// Unpacked: [size] 分散存储，每个元素独立
```

#### 1.3.2 动态数组 (Dynamic Array)

```systemverilog
// 声明
int dyn[];                // 大小未知

// 分配
dyn = new[100];           // 分配100个元素

// 调整大小
dyn = new[200](dyn);      // 扩展到200，保留原值

// 复制
int src[] = '{1,2,3,4,5};
int dst[];
dst = new[src.size()](src);  // 复制

// 删除
dyn.delete();             // 释放内存
```

#### 1.3.3 队列 (Queue)

```systemverilog
int q[$];                 // 声明队列
int q[$] = '{1, 2, 3};    // 初始化

// 添加元素
q.push_back(4);           // 尾部添加: {1,2,3,4}
q.push_front(0);          // 头部添加: {0,1,2,3,4}
q.insert(2, 99);          // 插入: {0,1,99,2,3,4}

// 删除元素
int v = q.pop_front();    // 头部弹出: v=0
int v = q.pop_back();     // 尾部弹出: v=4
q.delete(2);              // 删除索引2

// 查询
int sz = q.size();        // 大小
q.delete();               // 清空

// 切片
int slice[$] = q[1:3];    // 提取索引1-3
int first = q[0];         // 第一个
int last = q[$];          // 最后一个
```

#### 1.3.4 关联数组 (Associative Array)

```systemverilog
// 声明（键类型可以是任意类型）
int assoc[int];           // int 键
int assoc[string];        // string 键
int assoc[bit[31:0]];     // bit vector 键

// 赋值
assoc[100] = 1;
assoc[200] = 2;
assoc["name"] = 3;

// 遍历
foreach (assoc[i])
    $display("assoc[%0d] = %0d", i, assoc[i]);

// 方法
if (assoc.exists(100))    // 检查存在
    $display("Key 100 exists");

int first_key, last_key;
assoc.first(first_key);   // 第一个键
assoc.last(last_key);     // 最后一个键

int next_key, prev_key;
assoc.next(next_key);     // 下一个键
assoc.prev(prev_key);     // 上一个键

int cnt = assoc.num();    // 元素数量
assoc.delete(100);        // 删除特定键
assoc.delete();           // 清空
```

### 1.4 枚举类型

```systemverilog
// 基本定义
typedef enum {RED, GREEN, BLUE} color_t;
color_t my_color = GREEN;

// 显式赋值
typedef enum {A=0, B=10, C=20} val_t;

// 指定类型
typedef enum bit [2:0] {
    IDLE   = 3'b000,
    ACTIVE = 3'b001,
    DONE   = 3'b010,
    ERROR  = 3'b100
} state_t;

// 枚举方法
state_t s = IDLE;
s = s.next();             // 下一个值
s = s.prev();             // 上一个值
s = s.first();            // 第一个
s = s.last();             // 最后一个
int n = s.num();          // 元素数量
string name = s.name();   // 名称字符串
```

### 1.5 结构体与联合体

```systemverilog
// 结构体定义
typedef struct {
    bit [31:0] addr;
    bit [31:0] data;
    bit        valid;
    bit        ready;
} bus_trans_t;

// Packed 结构体
typedef struct packed {
    bit [3:0] version;
    bit [7:0] length;
    bit [19:0] payload;
} header_t;

// 使用
bus_trans_t trans;
trans.addr = 32'h1000;
trans.data = 32'hDEAD_BEEF;
trans.valid = 1;

// 结构体数组
bus_trans_t trans_queue[$];

// 联合体
typedef union {
    int   i;
    bit [31:0] b;
    real r;
} data_t;

data_t d;
d.i = 42;
$display("Bits: %b", d.b);  // 同一存储
```

### 1.6 字符串类型

```systemverilog
string s1 = "Hello";
string s2;

// 操作
s2 = {s1, " World"};      // 拼接
int len = s1.len();       // 长度

s1.tolower();             // 转小写
s1.toupper();             // 转大写

string sub = s1.substr(0, 3);  // 子串 "Hell"

int pos = s1.atoi();      // 字符串转整数
string s = pos.itoa();    // 整数转字符串

// 比较
if (s1 == s2) ...
if (s1.compare(s2) == 0) ...

// 查找
int idx = s1.substr("ll");  // 查找子串
```

---

## 2. 过程语句与例程

### 2.1 任务与函数详解

```systemverilog
// 函数 - 必须返回，不能有时序控制
function int add(int a, int b);
    return a + b;
endfunction

// void 函数 - 不返回值
function void print(string msg);
    $display("[%0t] %s", $time, msg);
endfunction

// 自动函数 - 每次调用分配新栈
function automatic int factorial(int n);
    if (n <= 1) return 1;
    return n * factorial(n-1);
endfunction

// 任务 - 可以有时序控制
task send_packet(bus_trans_t trans);
    @(posedge clk);
    vif.cb.addr <= trans.addr;
    vif.cb.data <= trans.data;
    vif.cb.valid <= 1;
    wait(vif.cb.ready);
    vif.cb.valid <= 0;
endtask
```

### 2.2 参数传递

```systemverilog
// 默认参数值
function int calc(int a, int b = 10, int c = 20);
    return a + b + c;
endfunction

// 调用方式
int r1 = calc(5);           // a=5, b=10, c=20
int r2 = calc(5, 15);       // a=5, b=15, c=20
int r3 = calc(5, .c(30));   // a=5, b=10, c=30 (按名传递)

// 引用参数 (ref) - 避免复制，可修改
task swap(ref int a, ref int b);
    int temp = a;
    a = b;
    b = temp;
endtask

// 常量引用 (const ref) - 避免复制，不可修改
function void print_array(const ref int arr[]);
    foreach (arr[i])
        $display("arr[%0d] = %0d", i, arr[i]);
endfunction

// 输出参数 (output)
function void divide(input int a, b, output int q, r);
    q = a / b;
    r = a % b;
endfunction
```

### 2.3 控制流语句

```systemverilog
// foreach 循环
int arr[10];
foreach (arr[i])
    arr[i] = i;

// 多维数组
int matrix[4][8];
foreach (matrix[i, j])
    matrix[i][j] = i * 8 + j;

// for 循环
for (int i = 0; i < 10; i++) begin
    // ...
end

// while 循环
int i = 0;
while (i < 10) begin
    i++;
end

// do-while 循环
do begin
    // 至少执行一次
end while (condition);

// forever 循环
forever begin
    @(posedge clk);
    // 无限循环
end

// repeat 循环
repeat(10) begin
    // 执行10次
end

// 跳转语句
for (int i = 0; i < 100; i++) begin
    if (i == 50) break;      // 跳出循环
    if (i % 2) continue;     // 跳到下一次迭代
    // ...
end

return value;  // 从函数返回
```

### 2.4 fork-join 并发控制

```systemverilog
// fork...join - 等待所有线程
fork
    begin
        // 线程1
        #10 $display("Thread 1");
    end
    begin
        // 线程2
        #5 $display("Thread 2");
    end
join
// 两个线程都完成才继续

// fork...join_any - 等待任一线程
fork
    begin
        #10 $display("Thread 1");
    end
    begin
        #5 $display("Thread 2");  // 先完成
    end
join_any
// 任一线程完成就继续，其他线程继续运行

// fork...join_none - 不等待
fork
    begin
        #10 $display("Thread 1");
    end
    begin
        #5 $display("Thread 2");
    end
join_none
// 立即继续，所有线程后台运行

// 等待所有子线程
fork
    // ...
join_none
// ... 其他代码 ...
wait fork;  // 等待所有子线程完成

// 禁用线程块
fork: my_block
    begin
        #100 $display("Timeout!");
    end
    begin
        // 主逻辑
        wait(done);
        disable my_block;  // 禁用整个块
    end
join_any
```

---

## 3. 面向对象编程

### 3.1 类的定义与使用

```systemverilog
class Packet;
    // 属性（成员变量）
    rand bit [31:0] addr;
    rand bit [31:0] data;
    rand bit [3:0]  burst;
    bit             valid;
    
    // 静态属性（所有实例共享）
    static int      count;
    const static int MAX_BURST = 16;
    
    // 构造函数
    function new(bit [31:0] a = 0, bit [31:0] d = 0);
        addr = a;
        data = d;
        burst = 1;
        count++;
    endfunction
    
    // 方法（成员函数）
    function void print();
        $display("Packet: addr=%h, data=%h, burst=%0d",
                 addr, data, burst);
    endfunction
    
    // 静态方法
    static function int get_count();
        return count;
    endfunction
    
    // 约束块
    constraint addr_c {
        addr inside {[32'h0000_1000:32'h0000_1FFF]};
    }
    
    constraint burst_c {
        burst inside {1, 2, 4, 8, 16};
    }
endclass

// 使用类
Packet pkt;
pkt = new();              // 创建对象
pkt.randomize();          // 随机化
pkt.print();              // 调用方法
pkt = new(32'h1000, 32'hDEAD);  // 带参数创建

// 句柄操作
Packet p1, p2;
p1 = new();
p2 = p1;                  // p2 指向 p1 的对象
p2.addr = 100;            // p1.addr 也变成 100

p1 = new();               // p1 指向新对象，p2 仍指向旧对象
```

### 3.2 继承与多态

```systemverilog
// 基类
class BasePacket;
    bit [31:0] addr;
    bit [31:0] data;
    
    function new(bit [31:0] a = 0, bit [31:0] d = 0);
        addr = a;
        data = d;
    endfunction
    
    // 虚方法（可重写）
    virtual function void print();
        $display("Base: addr=%h, data=%h", addr, data);
    endfunction
    
    // 纯虚方法（抽象方法，子类必须实现）
    // pure virtual function void process();
endclass

// 派生类
class ExtPacket extends BasePacket;
    bit [31:0] crc;
    bit [3:0]  burst;
    
    function new(bit [31:0] a = 0, bit [31:0] d = 0);
        super.new(a, d);     // 调用父类构造函数
        crc = calc_crc();
        burst = 1;
    endfunction
    
    // 重写虚方法
    virtual function void print();
        $display("Extended: addr=%h, data=%h, crc=%h, burst=%0d",
                 addr, data, crc, burst);
    endfunction
    
    function bit [31:0] calc_crc();
        // CRC 计算
        return ~addr ^ ~data;
    endfunction
endclass

// 多态
BasePacket pkt;            // 基类句柄
pkt = new ExtPacket();     // 指向派生类对象
pkt.print();               // 调用 ExtPacket::print()

// 类型转换
BasePacket base;
ExtPacket ext;
ext = new();
base = ext;                // 向上转型（隐式）
$cast(ext, base);          // 向下转型（显式，需检查）
```

### 3.3 this 和 super

```systemverilog
class MyClass;
    int value;
    
    function new(int value);
        this.value = value;    // this 区分成员和参数
    endfunction
    
    function void set(int v);
        this.value = v;
    endfunction
endclass

class Child extends Parent;
    int value;
    
    function new(int v);
        super.new(v);          // 调用父类构造
        this.value = v;
    endfunction
    
    function void reset();
        super.reset();         // 调用父类方法
        this.value = 0;
    endfunction
endclass
```

### 3.4 抽象类与接口类

```systemverilog
// 抽象类（不能实例化）
virtual class BaseDriver;
    pure virtual function void drive(Packet pkt);
    pure virtual task run();
endclass

// 具体类实现
class AxiDriver extends BaseDriver;
    virtual function void drive(Packet pkt);
        // 实现驱动逻辑
    endfunction
    
    virtual task run();
        // 实现运行逻辑
    endfunction
endclass

// 接口类（SystemVerilog 1800-2012+）
interface class IComparator;
    pure virtual function bit compare(input Packet a, b);
endinterface class

class Scoreboard implements IComparator;
    virtual function bit compare(input Packet a, b);
        return a.data == b.data;
    endfunction
endclass
```

### 3.5 参数化类

```systemverilog
// 参数化类（泛型）
class Stack #(type T = int, int DEPTH = 16);
    T storage[DEPTH];
    int top = 0;
    
    function void push(T item);
        if (top < DEPTH)
            storage[top++] = item;
    endfunction
    
    function T pop();
        if (top > 0)
            return storage[--top];
        return T'(0);
    endfunction
    
    function bit is_full();
        return top == DEPTH;
    endfunction
    
    function bit is_empty();
        return top == 0;
    endfunction
endclass

// 使用
Stack #(int) int_stack;           // int 类型，默认深度
Stack #(bit[31:0], 32) addr_stack; // bit[31:0] 类型，深度32
Stack #(string) str_stack;        // string 类型
```

---

## 4. 连接测试平台与设计

### 4.1 接口详解

```systemverilog
// 基本接口定义
interface bus_if(input logic clk, input logic rst_n);
    // 信号声明
    logic [31:0] addr;
    logic [31:0] wdata;
    logic [31:0] rdata;
    logic        valid;
    logic        ready;
    logic        write;
    
    // 时钟块（同步采样/驱动）
    clocking cb @(posedge clk);
        // 默认输入延迟 #1step，输出延迟 #0
        default input #1step output #0;
        
        // 输入信号（采样）
        input  addr, rdata, ready;
        
        // 输出信号（驱动）
        output wdata, valid, write;
        
        // 可以指定特定延迟
        input #2step rdata;
        output #1 valid;
    endclocking
    
    // modport（定义方向和访问权限）
    modport master (
        clocking cb,           // 使用时钟块
        output addr,           // 异步输出
        input  rst_n
    );
    
    modport slave (
        input  clk, rst_n,
        input  addr, wdata, valid, write,
        output rdata, ready
    );
    
    modport monitor (
        input  clk, rst_n, addr, wdata, rdata, valid, ready, write
    );
    
    // 接口内部任务和函数
    task wait_for_ready();
        wait(ready);
    endtask
    
    function bit is_idle();
        return (!valid && !ready);
    endfunction
endinterface
```

### 4.2 虚拟接口

```systemverilog
// 虚拟接口声明
virtual interface bus_if vif;

// 在类中使用虚拟接口
class Driver;
    virtual bus_if vif;     // 虚拟接口句柄
    
    function new(virtual bus_if vif);
        this.vif = vif;
    endfunction
    
    task drive_transaction(Packet pkt);
        @vif.cb;                    // 等待时钟沿
        vif.cb.addr <= pkt.addr;    // 同步驱动
        vif.cb.wdata <= pkt.data;
        vif.cb.write <= 1;
        vif.cb.valid <= 1;
        
        vif.wait_for_ready();       // 调用接口任务
        
        vif.cb.valid <= 0;
    endtask
endclass

// 顶层连接
module top;
    logic clk, rst_n;
    
    // 实例化接口
    bus_if bus(clk, rst_n);
    
    // 实例化 DUT
    DUT dut (
        .clk(clk),
        .rst_n(rst_n),
        .bus(bus.slave)    // 使用 modport 连接
    );
    
    // 测试程序
    initial begin
        // 传递接口到验证环境
        uvm_config_db#(virtual bus_if)::set(null, "*", "vif", bus);
        run_test();
    end
endmodule
```

### 4.3 Program 块

```systemverilog
// Program 块用于测试平台，避免竞争
program test(bus_if bus);
    initial begin
        // 初始化
        bus.cb.valid <= 0;
        
        // 发送事务
        for (int i = 0; i < 100; i++) begin
            Packet pkt = new();
            assert(pkt.randomize());
            drive(pkt);
        end
        
        $finish;
    endtask
    
    task drive(Packet pkt);
        @bus.cb;
        bus.cb.addr <= pkt.addr;
        bus.cb.valid <= 1;
        wait(bus.cb.ready);
        @bus.cb;
        bus.cb.valid <= 0;
    endtask
endprogram

// Program vs Module
// Program:
//   - 执行在 Reactive 区域（RTL 之后）
//   - 避免与 DUT 的竞争
//   - 用于测试平台代码
// Module:
//   - 执行在 Active 区域（RTL 区域）
//   - 用于设计和时钟生成
```

---

## 5. 线程与进程间通信

### 5.1 事件 (Event)

```systemverilog
event e1, e2;

// 触发事件
-> e1;                    // 立即触发

// 等待事件
@e1;                      // 边沿触发（只触发一次）
wait(e1.triggered);       // 电平触发（可多次）

// 事件合并
e2 = e1;                  // e2 和 e1 指向同一事件对象

// 等待多个事件
fork
    @e1;
    @e2;
join_any                  // 任一触发就继续

// 使用事件计数同步多个线程
int done_count = 0;
event all_done;

task wait_for_all(int N);
    fork
        begin
            wait(done_count == N);
            -> all_done;
        end
    join_none
endtask
```

### 5.2 信号量 (Semaphore)

```systemverilog
semaphore sem;

initial begin
    sem = new(1);          // 初始 1 个钥匙
    
    // 获取钥匙
    sem.get(1);            // 阻塞获取 1 个
    
    // 临界区
    access_shared_resource();
    
    // 释放钥匙
    sem.put(1);            // 释放 1 个
end

// 多钥匙信号量
semaphore multi_sem;
initial begin
    multi_sem = new(4);    // 4 个钥匙
    
    multi_sem.get(2);      // 获取 2 个
    // 使用资源
    multi_sem.put(2);      // 释放 2 个
end

// 非阻塞获取
if (sem.try_get(1)) begin
    // 获取成功
end else begin
    // 获取失败
end
```

### 5.3 信箱 (Mailbox)

```systemverilog
// 基本信箱
mailbox mbx;
mbx = new();               // 无限容量

// 发送
mbx.put(item);             // 阻塞发送
mbx.try_put(item);         // 非阻塞发送

// 接收
mbx.get(item);             // 阻塞接收
mbx.try_get(item);         // 非阻塞接收
mbx.peek(item);            // 查看（不移除）
mbx.try_peek(item);        // 非阻塞查看

// 有界信箱
mailbox bounded_mbx;
bounded_mbx = new(10);     // 容量 10

// 类型化信箱（SystemVerilog 2012+）
mailbox #(Packet) pkt_mbx;
pkt_mbx = new();
pkt_mbx.put(pkt);          // 只能放 Packet
Packet p;
pkt_mbx.get(p);            // 自动转换类型

// 查询
int n = mbx.num();         // 当前数量
```

### 5.4 生产者-消费者模式

```systemverilog
class Producer;
    mailbox #(Packet) out_mbx;
    
    task run();
        forever begin
            Packet pkt = new();
            assert(pkt.randomize());
            out_mbx.put(pkt);
            $display("Produced: %h", pkt.addr);
        end
    endtask
endclass

class Consumer;
    mailbox #(Packet) in_mbx;
    
    task run();
        Packet pkt;
        forever begin
            in_mbx.get(pkt);
            $display("Consumed: %h", pkt.addr);
            process(pkt);
        end
    endtask
    
    task process(Packet pkt);
        // 处理逻辑
    endtask
endclass

// 连接
program test;
    mailbox #(Packet) mbx = new();
    Producer prod = new();
    Consumer cons = new();
    
    initial begin
        prod.out_mbx = mbx;
        cons.in_mbx = mbx;
        
        fork
            prod.run();
            cons.run();
        join
    end
endprogram
```

---

## 6. 高级特性

### 6.1 静态变量与静态方法

```systemverilog
class Statistics;
    static int total_count = 0;
    static int success_count = 0;
    
    // 实例变量
    int instance_id;
    
    function new();
        instance_id = total_count++;
    endfunction
    
    // 静态方法只能访问静态变量
    static function void report();
        $display("Total: %0d, Success: %0d, Rate: %.2f%%",
                 total_count, success_count,
                 real'(success_count) / total_count * 100);
    endfunction
    
    static function void increment_success();
        success_count++;
    endfunction
endclass

// 使用静态成员
Statistics s1 = new();
Statistics s2 = new();
Statistics::report();       // 静态方法调用
```

### 6.2 深拷贝与浅拷贝

```systemverilog
class Inner;
    int value;
    
    function new(int v = 0);
        value = v;
    endfunction
    
    function Inner copy();
        copy = new(value);
    endfunction
endclass

class Outer;
    int id;
    Inner inner;
    
    function new();
        inner = new();
    endfunction
    
    // 浅拷贝（只拷贝句柄）
    function Outer shallow_copy();
        Outer c = new();
        c.id = this.id;
        c.inner = this.inner;  // 共享同一个 inner 对象
        return c;
    endfunction
    
    // 深拷贝（创建新对象）
    function Outer deep_copy();
        Outer c = new();
        c.id = this.id;
        c.inner = this.inner.copy();  // 创建新的 inner 对象
        return c;
    endfunction
endclass

// 使用
Outer o1 = new();
o1.inner.value = 10;

Outer o2 = o1.shallow_copy();
o2.inner.value = 20;  // o1.inner.value 也变成 20！

Outer o3 = o1.deep_copy();
o3.inner.value = 30;  // o1.inner.value 不受影响
```

### 6.3 回调机制

```systemverilog
// 回调基类
virtual class DriverCallback;
    pure virtual function void pre_send(ref Packet pkt);
    pure virtual function void post_send(Packet pkt);
endclass

// Driver 类
class Driver;
    DriverCallback callbacks[$];
    
    function void register_callback(DriverCallback cb);
        callbacks.push_back(cb);
    endfunction
    
    task send(Packet pkt);
        // 前回调
        foreach (callbacks[i])
            callbacks[i].pre_send(pkt);
        
        // 发送逻辑
        drive_to_bus(pkt);
        
        // 后回调
        foreach (callbacks[i])
            callbacks[i].post_send(pkt);
    endtask
endclass

// 具体回调实现
class ErrorInjector extends DriverCallback;
    virtual function void pre_send(ref Packet pkt);
        if ($urandom_range(0, 99) < 10)  // 10% 错误率
            pkt.data = ~pkt.data;        // 注入错误
    endfunction
    
    virtual function void post_send(Packet pkt);
        // 记录日志
    endfunction
endclass

// 使用
Driver drv = new();
drv.register_callback(ErrorInjector::new());
```

---

## 参考文档

- SystemVerilog for Verification 3rd Edition, Chris Spear & Greg Tumbush
- IEEE Std 1800-2023 SystemVerilog LRM
- Verification Methodology Manual for SystemVerilog

---

*整理自验证知识库 - 完整版*
