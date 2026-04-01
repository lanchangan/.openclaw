# 实战案例

> 本文档整理验证实战中的典型案例

## 目录

1. [APB 总线验证](#1-apb-总线验证)
2. [FIFO 验证](#2-fifo-验证)
3. [状态机验证](#3-状态机验证)
4. [UART 验证](#4-uart-验证)
5. [多通道验证](#5-多通道验证)

---

## 1. APB 总线验证

### 1.1 APB 协议简介

APB (Advanced Peripheral Bus) 是 AMBA 总线协议的一部分，特点：
- 低功耗、低成本
- 非流水线操作
- 两阶段传输：SETUP 和 ACCESS

### 1.2 APB 事务定义

```systemverilog
// APB 事务类
class apb_transaction extends uvm_sequence_item;
    `uvm_object_utils(apb_transaction)
    
    rand bit [31:0] paddr;
    rand bit [31:0] pwdata;
    rand bit        pwrite;  // 1=write, 0=read
    rand bit [3:0]  pstrb;
    rand int        delay;
    
    bit [31:0]      prdata;
    bit             pslverr;
    
    constraint addr_c {
        paddr[1:0] == 2'b00;  // 4字节对齐
    }
    
    constraint strb_c {
        if (pwrite)
            pstrb inside {4'b0001, 4'b0011, 4'b1111};
        else
            pstrb == 4'b0000;
    }
    
    constraint delay_c {
        delay inside {[0:10]};
    }
    
    function new(string name = "apb_transaction");
        super.new(name);
    endfunction
    
    virtual function string convert2string();
        return $sformatf("%s paddr=%h pwdata=%h prdata=%h",
            pwrite ? "WR" : "RD", paddr, pwdata, prdata);
    endfunction
endclass
```

### 1.3 APB Driver

```systemverilog
class apb_driver extends uvm_driver #(apb_transaction);
    `uvm_component_utils(apb_driver)
    
    virtual apb_if vif;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db #(virtual apb_if)::get(this, "", "vif", vif))
            `uvm_fatal("NO_VIF", "Virtual interface not found")
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        reset_dut();
        forever begin
            seq_item_port.get_next_item(req);
            drive_transaction(req);
            seq_item_port.item_done();
        end
    endtask
    
    virtual task reset_dut();
        vif.cb.psel    <= 0;
        vif.cb.penable <= 0;
        vif.cb.pwrite  <= 0;
        vif.cb.paddr   <= 0;
        vif.cb.pwdata  <= 0;
        vif.cb.pstrb   <= 0;
        repeat(5) @vif.cb;
    endtask
    
    virtual task drive_transaction(apb_transaction tr);
        // SETUP phase
        @vif.cb;
        vif.cb.psel   <= 1;
        vif.cb.pwrite <= tr.pwrite;
        vif.cb.paddr  <= tr.paddr;
        vif.cb.pwdata <= tr.pwdata;
        vif.cb.pstrb  <= tr.pstrb;
        
        // ACCESS phase
        @vif.cb;
        vif.cb.penable <= 1;
        
        // Wait for completion
        while (!vif.cb.pready) @vif.cb;
        
        // Capture response
        if (!tr.pwrite)
            tr.prdata = vif.cb.prdata;
        tr.pslverr = vif.cb.pslverr;
        
        // IDLE phase
        @vif.cb;
        vif.cb.psel    <= 0;
        vif.cb.penable <= 0;
    endtask
endclass
```

### 1.4 APB Monitor

```systemverilog
class apb_monitor extends uvm_monitor;
    `uvm_component_utils(apb_monitor)
    
    virtual apb_if vif;
    uvm_analysis_port #(apb_transaction) ap;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
        ap = new("ap", this);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db #(virtual apb_if)::get(this, "", "vif", vif))
            `uvm_fatal("NO_VIF", "Virtual interface not found")
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            apb_transaction tr;
            
            // Wait for SETUP phase
            wait(vif.psel && !vif.penable);
            
            // Capture SETUP
            tr = apb_transaction::type_id::create("tr");
            tr.paddr  = vif.paddr;
            tr.pwrite = vif.pwrite;
            tr.pwdata = vif.pwdata;
            tr.pstrb  = vif.pstrb;
            
            // Wait for ACCESS phase
            wait(vif.penable);
            wait(vif.pready);
            
            // Capture response
            if (!tr.pwrite)
                tr.prdata = vif.prdata;
            tr.pslverr = vif.pslverr;
            
            ap.write(tr);
        end
    endtask
endclass
```

### 1.5 APB Scoreboard

```systemverilog
class apb_scoreboard extends uvm_scoreboard;
    `uvm_component_utils(apb_scoreboard)
    
    uvm_analysis_imp #(apb_transaction, apb_scoreboard) ap;
    
    // 参考模型
    bit [31:0] mem [bit[31:0]];
    
    // 统计
    int matches, mismatches;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
        ap = new("ap", this);
    endfunction
    
    virtual function void write(apb_transaction tr);
        if (tr.pwrite) begin
            // 写操作：更新存储
            mem[tr.paddr] = tr.pwdata;
            `uvm_info("SCOREBOARD",
                $sformatf("Write: addr=%h, data=%h", tr.paddr, tr.pwdata),
                UVM_HIGH)
        end else begin
            // 读操作：比较数据
            bit [31:0] expected = mem.exists(tr.paddr) ? mem[tr.paddr] : 32'h0;
            
            if (tr.prdata === expected) begin
                matches++;
                `uvm_info("SCOREBOARD",
                    $sformatf("Read OK: addr=%h, data=%h", tr.paddr, tr.prdata),
                    UVM_HIGH)
            end else begin
                mismatches++;
                `uvm_error("SCOREBOARD",
                    $sformatf("Read MISMATCH: addr=%h, exp=%h, got=%h",
                        tr.paddr, expected, tr.prdata))
            end
        end
    endfunction
    
    virtual function void report_phase(uvm_phase phase);
        `uvm_info("SCOREBOARD",
            $sformatf("Matches: %0d, Mismatches: %0d", matches, mismatches),
            UVM_LOW)
    endfunction
endclass
```

---

## 2. FIFO 验证

### 2.1 FIFO 事务

```systemverilog
class fifo_transaction extends uvm_sequence_item;
    `uvm_object_utils(fifo_transaction)
    
    rand bit        wr_en;
    rand bit        rd_en;
    rand bit [7:0]  data_in;
    
    bit [7:0]       data_out;
    bit             full;
    bit             empty;
    
    constraint operation_c {
        // 不能同时满时写、空时读
        if (full) wr_en == 0;
        if (empty) rd_en == 0;
    }
    
    function new(string name = "fifo_transaction");
        super.new(name);
    endfunction
endclass
```

### 2.2 FIFO Coverage

```systemverilog
class fifo_coverage extends uvm_subscriber #(fifo_transaction);
    `uvm_component_utils(fifo_coverage)
    
    fifo_transaction tr;
    
    covergroup cg_fifo;
        cp_operation: coverpoint {tr.wr_en, tr.rd_en} {
            bins idle      = {2'b00};
            bins write     = {2'b10};
            bins read      = {2'b01};
            bins sim_rw    = {2'b11};
        }
        
        cp_full: coverpoint tr.full;
        cp_empty: coverpoint tr.empty;
        
        cp_full_empty: cross cp_full, cp_empty {
            ignore_bins invalid = binsof(cp_full) intersect {1} &&
                                  binsof(cp_empty) intersect {1};
        }
        
        cp_data: coverpoint tr.data_in {
            bins zero     = {0};
            bins max      = {255};
            bins others   = default;
        }
    endcovergroup
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
        cg_fifo = new();
    endfunction
    
    virtual function void write(fifo_transaction t);
        tr = t;
        cg_fifo.sample();
    endfunction
endclass
```

### 2.3 FIFO 断言

```systemverilog
module fifo_assertions (
    input logic clk,
    input logic rst_n,
    input logic wr_en,
    input logic rd_en,
    input logic full,
    input logic empty,
    input logic [3:0] count
);
    default clocking cb @(posedge clk);
    endclocking
    
    default disable iff (!rst_n);
    
    // 满时不写
    assert property (full |-> !wr_en)
    else $error("FIFO: Write when full");
    
    // 空时不读
    assert property (empty |-> !rd_en)
    else $error("FIFO: Read when empty");
    
    // 满和空互斥
    assert property (!(full && empty))
    else $error("FIFO: Full and empty both asserted");
    
    // 计数器范围
    assert property (count <= 4'd15)
    else $error("FIFO: Count out of range");
    
    // 写操作增加计数
    assert property ((wr_en && !rd_en && !full) |=> $past(count) + 1 == count)
    else $error("FIFO: Count increment failed");
    
    // 读操作减少计数
    assert property ((rd_en && !wr_en && !empty) |=> $past(count) - 1 == count)
    else $error("FIFO: Count decrement failed");
endmodule
```

---

## 3. 状态机验证

### 3.1 状态机定义

```systemverilog
typedef enum logic [2:0] {
    IDLE    = 3'b000,
    FETCH   = 3'b001,
    DECODE  = 3'b010,
    EXECUTE = 3'b011,
    WRITE   = 3'b100
} state_t;

class state_transaction extends uvm_sequence_item;
    `uvm_object_utils(state_transaction)
    
    rand bit        start;
    rand bit        stall;
    rand bit        done;
    
    state_t         current_state;
    state_t         next_state;
    
    function new(string name = "state_transaction");
        super.new(name);
    endfunction
endclass
```

### 3.2 状态机覆盖

```systemverilog
covergroup cg_fsm;
    cp_current_state: coverpoint current_state {
        bins states[] = {IDLE, FETCH, DECODE, EXECUTE, WRITE};
    }
    
    cp_next_state: coverpoint next_state {
        bins states[] = {IDLE, FETCH, DECODE, EXECUTE, WRITE};
    }
    
    // 状态转换覆盖
    cp_transition: coverpoint {current_state, next_state} {
        bins idle_to_fetch    = (IDLE    => FETCH);
        bins fetch_to_decode  = (FETCH   => DECODE);
        bins decode_to_exec   = (DECODE  => EXECUTE);
        bins exec_to_write    = (EXECUTE => WRITE);
        bins write_to_idle    = (WRITE   => IDLE);
        
        // 非法转换
        illegal_bins illegal = (IDLE => WRITE);
    }
endcovergroup
```

---

## 4. UART 验证

### 4.1 UART 配置

```systemverilog
class uart_config extends uvm_object;
    `uvm_object_utils(uart_config)
    
    rand int baud_rate = 115200;
    rand int data_bits = 8;
    rand int stop_bits = 1;
    rand bit parity_en = 0;
    rand bit parity_type = 0;  // 0=even, 1=odd
    
    constraint valid_config {
        baud_rate inside {9600, 19200, 38400, 57600, 115200};
        data_bits inside {5, 6, 7, 8};
        stop_bits inside {1, 2};
    }
endclass
```

### 4.2 UART 事务

```systemverilog
class uart_transaction extends uvm_sequence_item;
    `uvm_object_utils(uart_transaction)
    
    rand bit [7:0] data;
    rand bit       parity_err;
    
    bit            framing_err;
    bit            overrun_err;
    
    function new(string name = "uart_transaction");
        super.new(name);
    endfunction
endclass
```

---

## 5. 多通道验证

### 5.1 多通道环境

```systemverilog
class multi_channel_env extends uvm_env;
    `uvm_component_utils(multi_channel_env)
    
    apb_agent   apb_agent_inst[4];
    axi_agent   axi_agent;
    scoreboard  sb;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        
        // 创建 4 个 APB agent
        foreach (apb_agent_inst[i])
            apb_agent_inst[i] = apb_agent::type_id::create(
                $sformatf("apb_agent_inst[%0d]", i), this);
        
        // 创建 AXI agent
        axi_agent = axi_agent::type_id::create("axi_agent", this);
        
        // 创建 scoreboard
        sb = scoreboard::type_id::create("sb", this);
    endfunction
    
    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        
        foreach (apb_agent_inst[i])
            apb_agent_inst[i].ap.connect(sb.apb_ap[i]);
        
        axi_agent.ap.connect(sb.axi_ap);
    endfunction
endclass
```

### 5.2 多通道 Sequence

```systemverilog
class multi_channel_sequence extends uvm_sequence;
    `uvm_object_utils(multi_channel_sequence)
    
    function new(string name = "multi_channel_sequence");
        super.new(name);
    endfunction
    
    virtual task body();
        fork
            run_channel(0);
            run_channel(1);
            run_channel(2);
            run_channel(3);
        join
    endtask
    
    virtual task run_channel(int ch);
        apb_sequence seq;
        seq = apb_sequence::type_id::create("seq");
        seq.start(p_sequencer.apb_seqr[ch]);
    endtask
endclass
```

---

## 参考书籍

- UVM实战
- SystemVerilog for Verification
- WiFi PHY 验证实践

---

*整理自验证知识库*
