# UVM 验证框架

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

### 1.1 UVM 类层次结构

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
    └── uvm_config_db
```

---

## 2. UVM 工厂机制

### 2.1 工厂注册

```systemverilog
class my_packet extends uvm_sequence_item;
    `uvm_object_utils(my_packet)  // 注册到工厂
    
    function new(string name = "my_packet");
        super.new(name);
    endfunction
endclass

class my_driver extends uvm_driver;
    `uvm_component_utils(my_driver)  // 注册到工厂
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
endclass
```

### 2.2 创建对象

```systemverilog
// 使用工厂创建对象
my_packet pkt;
pkt = my_packet::type_id::create("pkt");

my_driver drv;
drv = my_driver::type_id::create("drv", this);
```

### 2.3 工厂覆盖

```systemverilog
// 类型覆盖
initial begin
    my_packet::type_id::set_type_override(
        my_extended_packet::get_type()
    );
end

// 实例覆盖
initial begin
    my_packet::type_id::set_inst_override(
        my_extended_packet::get_type(),
        "env.agent.sequencer.*"
    );
end
```

---

## 3. UVM 组件

### 3.1 Driver

```systemverilog
class my_driver extends uvm_driver #(my_packet);
    `uvm_component_utils(my_driver)
    
    virtual interface vif;
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db #(virtual interface)::get(this, "", "vif", vif))
            `uvm_fatal("NO_VIF", "Interface not found")
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            seq_item_port.get_next_item(req);
            drive_item(req);
            seq_item_port.item_done();
        end
    endtask
endclass
```

### 3.2 Monitor

```systemverilog
class my_monitor extends uvm_monitor;
    `uvm_component_utils(my_monitor)
    
    uvm_analysis_port #(my_packet) ap;
    virtual interface vif;
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            my_packet pkt;
            // 收集事务
            ap.write(pkt);
        end
    endtask
endclass
```

### 3.3 Agent

```systemverilog
class my_agent extends uvm_agent;
    `uvm_component_utils(my_agent)
    
    my_driver    driver;
    my_sequencer sequencer;
    my_monitor   monitor;
    
    uvm_analysis_port #(my_packet) ap;
    
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
        monitor.ap.connect(ap);
        
        if (is_active == UVM_ACTIVE)
            driver.seq_item_port.connect(sequencer.seq_item_export);
    endfunction
endclass
```

### 3.4 Scoreboard

```systemverilog
class my_scoreboard extends uvm_scoreboard;
    `uvm_component_utils(my_scoreboard)
    
    uvm_analysis_imp #(my_packet, my_scoreboard) ap;
    
    virtual function void write(my_packet pkt);
        check_packet(pkt);
    endfunction
endclass
```

---

## 4. UVM Phase 机制

### 4.1 Phase 列表

```
Common Phases:
  1. build_phase
  2. connect_phase
  3. end_of_elaboration_phase
  4. start_of_simulation_phase

Run-Time Phases:
  5. pre_reset_phase
  6. reset_phase
  7. post_reset_phase
  8. pre_configure_phase
  9. configure_phase
  10. post_configure_phase
  11. pre_main_phase
  12. main_phase           ◄──── 主要测试
  13. post_main_phase
  14. pre_shutdown_phase
  15. shutdown_phase
  16. post_shutdown_phase

Cleanup Phases:
  17. extract_phase
  18. check_phase
  19. report_phase
  20. final_phase
```

### 4.2 Phase Objection

```systemverilog
virtual task main_phase(uvm_phase phase);
    phase.raise_objection(this);
    
    // 测试逻辑
    
    phase.drop_objection(this);
endtask
```

---

## 5. Sequence 机制

### 5.1 定义 Sequence Item

```systemverilog
class my_packet extends uvm_sequence_item;
    `uvm_object_utils(my_packet)
    
    rand bit [31:0] addr;
    rand bit [31:0] data;
    
    constraint addr_c {
        addr inside {[32'h0000_1000:32'h0000_1FFF]};
    }
endclass
```

### 5.2 定义 Sequence

```systemverilog
class my_sequence extends uvm_sequence #(my_packet);
    `uvm_object_utils(my_sequence)
    
    virtual task body();
        my_packet pkt;
        
        repeat(10) begin
            pkt = my_packet::type_id::create("pkt");
            start_item(pkt);
            assert(pkt.randomize());
            finish_item(pkt);
        end
    endtask
endclass
```

### 5.3 启动 Sequence

```systemverilog
virtual task run_phase(uvm_phase phase);
    my_sequence seq;
    
    phase.raise_objection(this);
    seq = my_sequence::type_id::create("seq");
    seq.start(env.agent.sequencer);
    phase.drop_objection(this);
endtask
```

---

## 6. Config DB

### 6.1 设置配置

```systemverilog
virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    
    uvm_config_db #(virtual interface)::set(this, "*", "vif", my_interface);
    uvm_config_db #(int)::set(this, "env.agent*", "timeout", 1000);
endfunction
```

### 6.2 获取配置

```systemverilog
virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    
    if (!uvm_config_db #(virtual interface)::get(this, "", "vif", vif))
        `uvm_fatal("NO_VIF", "Interface not found")
endfunction
```

---

## 7. TLM 通信

### 7.1 Analysis Port

```systemverilog
// 生产者
class my_monitor extends uvm_monitor;
    uvm_analysis_port #(my_packet) ap;
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            my_packet pkt;
            ap.write(pkt);  // 广播
        end
    endtask
endclass

// 消费者
class my_scoreboard extends uvm_scoreboard;
    uvm_analysis_imp #(my_packet, my_scoreboard) ap;
    
    virtual function void write(my_packet pkt);
        check_packet(pkt);
    endfunction
endclass
```

### 7.2 TLM FIFO

```systemverilog
class my_component extends uvm_component;
    uvm_tlm_analysis_fifo #(my_packet) fifo;
    uvm_get_port #(my_packet) get_port;
    
    virtual task run_phase(uvm_phase phase);
        my_packet pkt;
        forever begin
            get_port.get(pkt);
            process_packet(pkt);
        end
    endtask
endclass
```

---

*整理自验证知识库*
