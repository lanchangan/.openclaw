# 进阶主题

> 本文档整理自验证相关书籍中的进阶主题

## 目录

1. [常见陷阱](#1-常见陷阱)
2. [性能优化](#2-性能优化)
3. [调试技巧](#3-调试技巧)
4. [高级UVM用法](#4-高级uvm用法)
5. [形式验证基础](#5-形式验证基础)

---

## 1. 常见陷阱

### 1.1 SystemVerilog 陷阱

#### 竞争条件

```systemverilog
// 错误: 竞争条件
always @(posedge clk) begin
    count = count + 1;  // 阻塞赋值
end

// 正确: 非阻塞赋值
always @(posedge clk) begin
    count <= count + 1;  // 非阻塞赋值
end

// 测试平台使用 clocking block
clocking cb @(posedge clk);
    input  #1step data;
    output #0 enable;
endclocking
```

#### 静态变量陷阱

```systemverilog
// 错误: 静态变量共享
class Transaction;
    static int id = 0;  // 所有实例共享
    // 问题: 多个实例会看到相同的 id
endclass

// 正确: 根据需求选择
class Transaction;
    int id;  // 实例变量
    
    function new();
        id = id_counter++;
    endfunction
    
    static int id_counter = 0;
endclass
```

#### 数组越界

```systemverilog
// 危险: 数组越界
int arr[10];
int idx = 15;
arr[idx] = 100;  // 越界!

// 安全: 边界检查
int arr[10];
int idx = 15;
if (idx >= 0 && idx < 10)
    arr[idx] = 100;
else
    $error("Array index out of bounds");
```

#### 随机化失败

```systemverilog
// 问题: 约束冲突
class Packet;
    rand bit [3:0] size;
    rand bit [7:0] data[];
    
    constraint size_c { size > 20; }  // size 最大 15
    constraint data_c { data.size() == size; }
    // 随机化必然失败!
endclass

// 解决: 检查约束一致性
class Packet;
    rand bit [3:0] size;
    rand bit [7:0] data[];
    
    constraint size_c { size inside {[1:15]}; }
    constraint data_c { data.size() == size; }
endclass
```

### 1.2 UVM 陷阱

#### Objection 忘记 drop

```systemverilog
// 错误: 忘记 drop objection
task run_phase(uvm_phase phase);
    phase.raise_objection(this);
    // ... 测试代码
    // 忘记 drop_objection -> 仿真卡住
endtask

// 正确: 使用 begin-end 确保成对
task run_phase(uvm_phase phase);
    phase.raise_objection(this);
    begin
        // ... 测试代码
    end
    phase.drop_objection(this);
endtask

// 更好: 使用 automatic objection
class my_sequence extends uvm_sequence;
    task body();
        `uvm_do_with(req, {...})
    endtask
endclass
// sequence 执行完自动 drop
```

#### Config DB 路径错误

```systemverilog
// 错误: 路径不匹配
// 设置
uvm_config_db #(int)::set(null, "uvm_test_top.env", "value", 100);
// 获取
uvm_config_db #(int)::get(this, "", "value", val);  // 路径错误!

// 正确: 路径匹配
// 设置
uvm_config_db #(int)::set(null, "uvm_test_top.env", "value", 100);
// 获取 (在 env 中)
uvm_config_db #(int)::get(this, "", "value", val);
```

#### 工厂覆盖问题

```systemverilog
// 问题: 覆盖时机错误
initial begin
    run_test();  // 先运行测试
    // 太晚! 工厂覆盖需要在 run_test 之前
    my_class::type_id::set_type_override(my_ext_class::get_type());
end

// 正确: 在 build_phase 或之前覆盖
initial begin
    my_class::type_id::set_type_override(my_ext_class::get_type());
    run_test();
end
```

---

## 2. 性能优化

### 2.1 仿真性能优化

```systemverilog
// 减少不必要的计算
// 差: 每次都计算
always @(posedge clk) begin
    if (complex_calculation(a, b, c))
        result <= d;
end

// 好: 只在需要时计算
always @(posedge clk) begin
    if (enable)
        if (complex_calculation(a, b, c))
            result <= d;
end

// 使用时间精度
timescale 1ns/1ps  // 合理选择精度
```

### 2.2 内存优化

```systemverilog
// 减少内存使用
// 差: 大数组
int huge_array[1000000];

// 好: 关联数组
int sparse_array[bit[31:0]];  // 只存储使用的元素

// 及时释放
mailbox mbx;
mbx = new();
// 使用完后
mbx.delete();  // 释放内存
```

### 2.3 日志优化

```systemverilog
// 减少日志输出
// 差: 高频日志
always @(posedge clk) begin
    `uvm_info("DEBUG", $sformatf("data=%h", data), UVM_LOW)
end

// 好: 条件日志
always @(posedge clk) begin
    if (error_condition)
        `uvm_error("ERR", $sformatf("data=%h", data))
    else if (debug_enable)
        `uvm_info("DEBUG", $sformatf("data=%h", data), UVM_HIGH)
end
```

### 2.4 回归测试优化

```tcl
# 并行执行
vcs -ntb_opts random_init_randomize -parallel

# 分层编译
vcs -sverilog -full64 -timescale=1ns/1ps \
    -f filelist.f \
    -l comp.log \
    -debug_access+all \
    -kdb

# 增量编译
vcs -incr_comp -sverilog ...
```

---

## 3. 调试技巧

### 3.1 波形调试

```systemverilog
// VCS 波形
initial begin
    $fsdbDumpfile("wave.fsdb");
    $fsdbDumpvars(0, top);
end

// Verdi 自动打开
verdi -ssf wave.fsdb

// 选择性 dump
initial begin
    $fsdbDumpvars(1, top.dut);  // 只 dump DUT
end
```

### 3.2 日志分析

```systemverilog
// 结构化日志
`define INFO(tag, msg) \
    $display("[%t] [%s] [INFO] %s", $time, tag, msg)

`define ERROR(tag, msg) \
    $display("[%t] [%s] [ERROR] %s", $time, tag, msg)

// 使用
`INFO("APB", "Transaction started")
`ERROR("FIFO", "Overflow detected")

// 日志过滤
+UVM_VERBOSITY=UVM_MEDIUM
+UVM_LOG_RECORD=YES
```

### 3.3 断点调试

```systemverilog
// 条件断点
initial begin
    forever @(posedge clk) begin
        if (addr == 32'hDEAD_BEEF) begin
            $display("Hit breakpoint at time %t", $time);
            $stop;  // 暂停仿真
        end
    end
end

// 信号跟踪
initial begin
    $monitor("[%t] state=%b, count=%d", $time, state, count);
end
```

### 3.4 UVM 调试

```systemverilog
// 打印拓扑结构
initial begin
    uvm_top.print_topology();
end

// 打印配置
initial begin
    uvm_config_db #(int)::dump();
end

// 打印工厂
initial begin
    factory.print();
end

// 使用 command line debugger
+UVM_PHASE_TRACE
+UVM_CONFIG_DB_TRACE
+UVM_OBJECTION_TRACE
```

---

## 4. 高级UVM用法

### 4.1 Callback 机制

```systemverilog
// 定义 callback 类
class my_callback extends uvm_callback;
    virtual function void pre_send(my_transaction tr);
        // 修改事务
        tr.data = tr.data ^ 32'hFFFFFFFF;
    endfunction
    
    virtual function void post_send(my_transaction tr);
        // 记录日志
        `uvm_info("CB", "Transaction sent", UVM_LOW)
    endfunction
endclass

// 在 driver 中使用 callback
class my_driver extends uvm_driver;
    `uvm_register_cb(my_driver, my_callback)
    
    task run_phase(uvm_phase phase);
        forever begin
            seq_item_port.get_next_item(req);
            
            `uvm_do_callbacks(my_driver, my_callback, pre_send(req))
            drive_item(req);
            `uvm_do_callbacks(my_driver, my_callback, post_send(req))
            
            seq_item_port.item_done();
        end
    endtask
endclass

// 在 test 中注册 callback
class my_test extends uvm_test;
    my_callback cb;
    
    function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        cb = my_callback::type_id::create("cb");
        uvm_callbacks #(my_driver, my_callback)::add(env.agent.driver, cb);
    endfunction
endclass
```

### 4.2 Factory 覆盖高级用法

```systemverilog
// 类型覆盖
initial begin
    my_base::type_id::set_type_override(my_ext::get_type());
end

// 实例覆盖
initial begin
    my_base::type_id::set_inst_override(
        my_ext::get_type(),
        "env.agent1.driver"
    );
end

// 批量覆盖
initial begin
    // 覆盖所有 agent 的 driver
    uvm_coreservice_t cs = uvm_coreservice_t::get();
    uvm_factory factory = cs.get_factory();
    factory.set_inst_override_by_type(
        my_base::get_type(),
        my_ext::get_type(),
        "*.*.driver"
    );
end
```

### 4.3 自定义 Phase

```systemverilog
// 定义自定义 phase
class my_custom_phase extends uvm_task_phase;
    function new(string name = "my_custom");
        super.new(name);
    endfunction
    
    virtual task exec_task(uvm_component comp, uvm_phase phase);
        my_component my_comp;
        if ($cast(my_comp, comp))
            my_comp.my_custom_phase(phase);
    endtask
endclass

// 在 component 中实现
class my_component extends uvm_component;
    virtual task my_custom_phase(uvm_phase phase);
        // 自定义 phase 逻辑
    endtask
endclass
```

---

## 5. 形式验证基础

### 5.1 形式验证概念

```
┌─────────────────────────────────────────────────────────────┐
│                    形式验证类型                              │
├─────────────────────────────────────────────────────────────┤
│  等价性检查 (Equivalence Checking)                           │
│  ├── RTL vs RTL                                             │
│  ├── RTL vs Gate                                            │
│  └── Gate vs Gate                                           │
├─────────────────────────────────────────────────────────────┤
│  模型检查 (Model Checking)                                   │
│  ├── 属性验证                                                │
│  ├── 状态机验证                                              │
│  └── 协议验证                                                │
├─────────────────────────────────────────────────────────────┤
│  定理证明 (Theorem Proving)                                  │
│  └── 数学证明正确性                                          │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 断言与形式验证

```systemverilog
// 形式验证断言
module formal_check (
    input logic clk,
    input logic rst_n,
    input logic req,
    output logic gnt
);
    // Assume: 环境约束
    assume property (@(posedge clk) !rst_n |-> !req);
    
    // Assert: 设计属性
    assert property (@(posedge clk) req |-> ##[1:3] gnt);
    
    // Cover: 覆盖属性
    cover property (@(posedge clk) req ##1 gnt);
endmodule
```

### 5.3 形式验证流程

```
┌─────────────────────────────────────────────────────────────┐
│                    形式验证流程                              │
├─────────────────────────────────────────────────────────────┤
│  1. 定义属性                                                 │
│     ├── 从规格提取属性                                       │
│     └── 编写 SVA 断言                                        │
├─────────────────────────────────────────────────────────────┤
│  2. 设置约束                                                 │
│     ├── 输入约束 (assume)                                    │
│     └── 环境假设                                             │
├─────────────────────────────────────────────────────────────┤
│  3. 运行验证                                                 │
│     ├── 遍历状态空间                                         │
│     └── 检查所有可能情况                                     │
├─────────────────────────────────────────────────────────────┤
│  4. 分析结果                                                 │
│     ├── Pass: 属性成立                                       │
│     ├── Fail: 找到反例                                       │
│     └── Inconclusive: 状态爆炸                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 参考书籍

- 101个Verilog和SystemVerilog陷阱
- SystemVerilog for Verification 3rd Edition
- Formal Verification Techniques

---

*整理自验证知识库*
