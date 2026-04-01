# 随机化技术

> 本文档整理自《SystemVerilog for Verification》等书籍

## 目录

1. [随机化概述](#1-随机化概述)
2. [Rand 与 Randc](#2-rand-与-randc)
3. [约束 (Constraint)](#3-约束-constraint)
4. [约束块](#4-约束块)
5. [随机化方法](#5-随机化方法)
6. [随机化实战技巧](#6-随机化实战技巧)

---

## 1. 随机化概述

### 1.1 为什么需要随机化

- **提高验证效率**：自动生成大量测试用例
- **发现边界问题**：覆盖难以预料的边界情况
- **减少手动工作**：避免手动编写大量定向测试
- **提高覆盖率**：自动探索状态空间

### 1.2 随机化层次

```
┌─────────────────────────────────────────────────────────────┐
│                      随机化层次                              │
├─────────────────────────────────────────────────────────────┤
│  事务随机化                                                  │
│  ├── 数据值随机化                                           │
│  ├── 地址随机化                                             │
│  └── 协议参数随机化                                         │
├─────────────────────────────────────────────────────────────┤
│  控制随机化                                                  │
│  ├── 操作类型随机化                                         │
│  ├── 时序随机化                                             │
│  └── 延迟随机化                                             │
├─────────────────────────────────────────────────────────────┤
│  环境随机化                                                  │
│  ├── 配置随机化                                             │
│  ├── 拓扑随机化                                             │
│  └── 错误注入随机化                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Rand 与 Randc

### 2.1 Rand 关键字

```systemverilog
class Packet;
    rand bit [31:0] addr;    // 随机变量
    rand bit [31:0] data;    // 每次随机化可能重复
    
    function new();
        // 构造函数
    endfunction
endclass

Packet pkt = new();
pkt.randomize();  // 随机化
```

### 2.2 Randc 关键字

```systemverilog
class Packet;
    randc bit [3:0] id;  // 循环随机，不重复直到遍历完
    
    // id 会遍历 0-15，每个值出现一次后才重复
endclass

Packet pkt = new();
repeat(32) begin
    pkt.randomize();
    $display("id = %0d", pkt.id);  // 0,1,2,...,15,0,1,2,...
end
```

### 2.3 随机变量类型

```systemverilog
class Transaction;
    // 标量随机变量
    rand bit [31:0] addr;
    rand int        count;
    
    // 数组随机变量
    rand bit [7:0]  data[16];
    
    // 动态数组
    rand bit [7:0]  payload[];
    
    // 队列
    rand int        queue[$];
    
    // 结构体
    rand struct {
        bit [31:0] addr;
        bit [31:0] data;
    } header;
    
    // 枚举
    rand opcode_t opcode;
endclass
```

---

## 3. 约束 (Constraint)

### 3.1 基本约束

```systemverilog
class Packet;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    rand int        burst;
    
    // 约束块
    constraint addr_c {
        addr inside {[32'h0000_1000:32'h0000_1FFF]};
    }
    
    constraint burst_c {
        burst inside {1, 2, 4, 8};
    }
    
    constraint data_c {
        data != 0;  // 数据不为零
    }
endclass
```

### 3.2 约束表达式

```systemverilog
class Transaction;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    rand bit        read_write;
    rand int        burst;
    
    // 范围约束
    constraint addr_range {
        addr >= 32'h1000;
        addr <= 32'h1FFF;
    }
    
    // 等价写法
    constraint addr_range2 {
        addr inside {[32'h1000:32'h1FFF]};
    }
    
    // 条件约束
    constraint rw_constraint {
        if (read_write) {
            data != 0;  // 写操作数据不为零
        }
    }
    
    // 关系约束
    constraint burst_relation {
        burst <= 8;
        burst >= 1;
    }
endclass
```

### 3.3 分布约束

```systemverilog
class Transaction;
    rand bit [7:0] value;
    
    // 权重分布
    constraint dist_c {
        value dist {
            0       := 10,   // 权重 10
            [1:100] := 40,   // 范围权重 40
            [101:200] :/ 30, // 范围内均分 30
            [201:255] :/ 20  // 范围内均分 20
        };
    }
endclass
```

---

## 4. 约束块

### 4.1 集合约束

```systemverilog
class Packet;
    rand bit [7:0] value;
    
    // inside 集合
    constraint set_c {
        value inside {8'h00, 8'hFF, 8'h55, 8'hAA};
    }
    
    // 排除集合
    constraint exclude_c {
        !(value inside {[8'h01:8'hFE]});
    }
endclass
```

### 4.2 条件约束

```systemverilog
class Transaction;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    rand bit        read_write;
    rand int        burst;
    
    // if-else 约束
    constraint cond_c {
        if (read_write == 1) {
            data inside {[32'h0000_0001:32'hFFFF_FFFE]};
        } else {
            data == 0;
        }
    }
    
    // => 蕴含运算符
    constraint imply_c {
        (read_write == 1) -> (data != 0);
    }
    
    // case 约束
    constraint case_c {
        case (burst)
            1:  addr[1:0] == 2'b00;
            2:  addr[1:0] == 2'b00;
            4:  addr[1:0] == 2'b00;
            8:  addr[1:0] == 2'b00;
        endcase
    }
endclass
```

### 4.3 循环约束

```systemverilog
class ArrayTransaction;
    rand bit [7:0] array[16];
    
    // 数组元素约束
    constraint array_c {
        foreach (array[i]) {
            array[i] inside {[0:100]};
            if (i > 0) {
                array[i] >= array[i-1];  // 递增数组
            }
        }
    }
endclass
```

### 4.4 数组约束

```systemverilog
class Packet;
    rand bit [7:0] payload[];
    rand int       length;
    
    // 动态数组大小约束
    constraint length_c {
        length inside {[1:256]};
        payload.size() == length;
    }
    
    // 数组内容约束
    constraint payload_c {
        payload.sum() > 0;  // 总和大于零
        foreach (payload[i])
            payload[i] != 0;
    }
endclass
```

### 4.5 约束继承

```systemverilog
class BasePacket;
    rand bit [31:0] addr;
    
    constraint base_addr_c {
        addr inside {[32'h0000_0000:32'h0000_FFFF]};
    }
endclass

class ExtPacket extends BasePacket;
    rand bit [31:0] data;
    
    // 继承并添加约束
    constraint ext_addr_c {
        addr[1:0] == 2'b00;  // 4字节对齐
    }
    
    // 覆盖父类约束
    constraint base_addr_c {
        addr inside {[32'h0000_1000:32'h0000_1FFF]};
    }
endclass
```

---

## 5. 随机化方法

### 5.1 randomize()

```systemverilog
class Packet;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    
    constraint addr_c {
        addr inside {[32'h1000:32'h1FFF]};
    }
endclass

Packet pkt = new();

// 基本随机化
if (!pkt.randomize()) begin
    $error("Randomization failed");
end

// 带内联约束
pkt.randomize() with {
    addr == 32'h1000;  // 固定地址
    data > 100;        // 数据大于 100
};
```

### 5.2 pre_randomize() 和 post_randomize()

```systemverilog
class Packet;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    static int id = 0;
    
    // 随机化前调用
    function void pre_randomize();
        $display("Before randomization");
    endfunction
    
    // 随机化后调用
    function void post_randomize();
        id++;
        if (data == 0) begin
            data = $random;  // 后处理修正
        end
    endfunction
endclass
```

### 5.3 随机化控制

```systemverilog
class Packet;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    rand bit        fixed_addr;
    
    // 条件控制随机化
    constraint addr_fixed_c {
        if (fixed_addr) {
            addr == 32'h1000;
        }
    }
endclass

Packet pkt = new();

// 随机化时禁用约束
pkt.randomize() with {
    fixed_addr == 1;  // 固定地址
};

// 或者关闭约束
pkt.addr_fixed_c.constraint_mode(0);  // 关闭约束
pkt.randomize();
pkt.addr_fixed_c.constraint_mode(1);  // 开启约束
```

### 5.4 rand_mode()

```systemverilog
class Packet;
    rand bit [31:0] addr;
    rand bit [31:0] data;
endclass

Packet pkt = new();

// 禁用 addr 随机化
pkt.addr.rand_mode(0);
pkt.addr = 32'h1000;  // 手动设置
pkt.randomize();      // 只随机化 data

// 恢复 addr 随机化
pkt.addr.rand_mode(1);
pkt.randomize();      // 两者都随机化
```

### 5.5 constraint_mode()

```systemverilog
class Packet;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    
    constraint addr_c {
        addr inside {[32'h1000:32'h1FFF]};
    }
    
    constraint data_c {
        data > 0;
    }
endclass

Packet pkt = new();

// 检查约束状态
if (pkt.addr_c.constraint_mode())
    $display("addr_c is enabled");

// 禁用约束
pkt.addr_c.constraint_mode(0);

// 启用约束
pkt.addr_c.constraint_mode(1);
```

---

## 6. 随机化实战技巧

### 6.1 带权重的场景随机化

```systemverilog
typedef enum {
    READ, WRITE, IDLE
} op_t;

class Transaction;
    rand op_t    operation;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    
    // 操作类型分布
    constraint op_dist_c {
        operation dist {
            READ  := 40,  // 40% 读操作
            WRITE := 40,  // 40% 写操作
            IDLE  := 20   // 20% 空闲
        };
    }
    
    // 不同操作类型的约束
    constraint op_specific_c {
        if (operation == READ) {
            data == 0;  // 读操作数据域为 0
        } else if (operation == WRITE) {
            data inside {[32'h0000_0001:32'hFFFF_FFFE]};
        } else {  // IDLE
            addr == 0;
            data == 0;
        }
    }
endclass
```

### 6.2 随机化序列

```systemverilog
class SequenceGenerator;
    rand bit [7:0] item;
    rand int       delay;
    
    // 序列约束
    constraint sequence_c {
        // 按顺序生成 0, 1, 2, ...
        item == next_item;
    }
    
    // 延迟约束
    constraint delay_c {
        delay inside {[1:10]};
    }
    
    // 类成员
    static bit [7:0] next_item = 0;
    
    function void post_randomize();
        next_item = (next_item + 1) % 256;
    endfunction
endclass
```

### 6.3 动态约束

```systemverilog
class ConfigurablePacket;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    
    // 动态约束参数
    bit [31:0] min_addr = 32'h0000_0000;
    bit [31:0] max_addr = 32'hFFFF_FFFF;
    bit        enable_addr_constraint = 1;
    
    constraint dynamic_addr_c {
        if (enable_addr_constraint) {
            addr inside {[min_addr:max_addr]};
        }
    }
    
    // 运行时修改约束
    function void set_addr_range(bit [31:0] min, bit [31:0] max);
        min_addr = min;
        max_addr = max;
    endfunction
endclass
```

### 6.4 复杂对象随机化

```systemverilog
class Header;
    rand bit [15:0] length;
    rand bit [7:0]  type;
    
    constraint valid_c {
        length > 0;
        length <= 1500;
    }
endclass

class Payload;
    rand bit [7:0] data[];
    
    constraint size_c {
        data.size() inside {[1:1500]};
    }
endclass

class Packet;
    rand Header  header;
    rand Payload payload;
    
    // 关联约束
    constraint length_match_c {
        header.length == payload.data.size();
    }
    
    function new();
        header  = new();
        payload = new();
    endfunction
    
    function void post_randomize();
        // 确保一致性
        assert(payload.data.size() == header.length);
    endfunction
endclass
```

### 6.5 随机化调试

```systemverilog
class Packet;
    rand bit [31:0] addr;
    rand bit [31:0] data;
    
    constraint addr_c {
        addr inside {[32'h1000:32'h1FFF]};
    }
    
    // 打印约束信息
    function void pre_randomize();
        $display("=== Pre-randomize ===");
        $display("addr: %h, data: %h", addr, data);
    endfunction
    
    function void post_randomize();
        $display("=== Post-randomize ===");
        $display("addr: %h, data: %h", addr, data);
    endfunction
endclass

// 使用 srand 控制随机种子
initial begin
    $urandom(seed);  // 设置随机种子
    // 或
    pkt.srandom(seed);  // 对象级别种子
end
```

### 6.6 约束求解顺序

```systemverilog
class Packet;
    rand bit [3:0] size;
    rand bit [7:0] data[];
    
    // 约束求解顺序
    constraint size_c {
        solve size before data;  // 先解 size，再解 data
        size inside {[1:16]};
        data.size() == size;
    }
endclass
```

---

## 参考书籍

- SystemVerilog for Verification 3rd Edition
- IEEE 1800 SystemVerilog LRM

---

*整理自验证知识库*
