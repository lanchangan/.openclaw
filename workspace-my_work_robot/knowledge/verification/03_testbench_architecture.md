# 测试平台架构

> 本文档整理自《SystemVerilog for Verification》《VMM》等书籍

## 目录

1. [分层测试平台](#1-分层测试平台)
2. [接口与连接](#2-接口与连接)
3. [事务级建模](#3-事务级建模)
4. [验证组件设计](#4-验证组件设计)

---

## 1. 分层测试平台

### 1.1 测试平台层次结构

```
┌─────────────────────────────────────────────────────────────┐
│                     Test Layer (测试层)                      │
│  - 测试用例、测试序列、功能覆盖配置                           │
├─────────────────────────────────────────────────────────────┤
│                   Scenario Layer (场景层)                    │
│  - 序列生成器、场景控制                                      │
├─────────────────────────────────────────────────────────────┤
│                  Functional Layer (功能层)                   │
│  - 检查器、记分板、参考模型                                  │
├─────────────────────────────────────────────────────────────┤
│                   Command Layer (命令层)                     │
│  - 驱动器、监视器、断言检查器                                │
├─────────────────────────────────────────────────────────────┤
│                    Signal Layer (信号层)                     │
│  - 接口、时钟块、DUT 连接                                    │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 各层职责

| 层次 | 组件 | 职责 |
|------|------|------|
| 信号层 | Interface, Clocking Block | 物理信号连接、时序同步 |
| 命令层 | Driver, Monitor | 协议驱动、信号采集 |
| 功能层 | Scoreboard, Checker | 功能检查、数据比对 |
| 场景层 | Sequencer, Generator | 测试场景生成 |
| 测试层 | Test, Env | 测试控制、环境配置 |

---

## 2. 接口与连接

### 2.1 接口定义

```systemverilog
interface apb_if(input logic pclk, input logic preset_n);
    logic [31:0] paddr;
    logic [31:0] pwdata;
    logic [31:0] prdata;
    logic        psel;
    logic        penable;
    logic        pwrite;
    logic        pready;
    
    clocking cb @(posedge pclk);
        input  paddr, pwdata, psel, penable, pwrite;
        output prdata, pready;
    endclocking
    
    modport master (output paddr, pwdata, psel, penable, pwrite,
                    input  prdata, pready, clocking cb);
    
    modport slave (input  paddr, pwdata, psel, penable, pwrite,
                   output prdata, pready);
endinterface
```

### 2.2 虚拟接口

```systemverilog
class apb_driver extends uvm_driver;
    virtual apb_if vif;
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            seq_item_port.get_next_item(req);
            @vif.cb;
            vif.cb.psel <= 1;
            // ...
            seq_item_port.item_done();
        end
    endtask
endclass
```

### 2.3 顶层连接

```systemverilog
module top;
    logic clk, rst_n;
    
    apb_if apb_bus(clk, rst_n);
    
    DUT dut(.*);
    
    initial begin
        uvm_config_db #(virtual apb_if)::set(null, "uvm_test_top", "vif", apb_bus);
        run_test("apb_test");
    end
endmodule
```

---

## 3. 事务级建模

### 3.1 事务定义

```systemverilog
class apb_transaction extends uvm_sequence_item;
    `uvm_object_utils(apb_transaction)
    
    rand bit [31:0] addr;
    rand bit [31:0] data;
    rand bit        write;
    rand int        delay;
    
    constraint addr_c { addr[1:0] == 2'b00; }
    constraint delay_c { delay inside {[0:10]}; }
endclass
```

---

## 4. 验证组件设计

### 4.1 Driver 设计模式

```systemverilog
class apb_driver extends uvm_driver #(apb_transaction);
    virtual apb_if vif;
    int transactions_sent;
    
    virtual task run_phase(uvm_phase phase);
        reset_dut();
        forever begin
            seq_item_port.get_next_item(req);
            drive_transaction(req);
            seq_item_port.item_done();
        end
    endtask
    
    virtual task drive_transaction(apb_transaction tr);
        @vif.cb;
        vif.cb.psel   <= 1;
        vif.cb.pwrite <= tr.write;
        vif.cb.paddr  <= tr.addr;
        vif.cb.pwdata <= tr.data;
        
        @vif.cb;
        vif.cb.penable <= 1;
        wait(vif.cb.pready);
        
        @vif.cb;
        vif.cb.psel    <= 0;
        vif.cb.penable <= 0;
        
        transactions_sent++;
    endtask
endclass
```

### 4.2 Scoreboard 设计模式

```systemverilog
class apb_scoreboard extends uvm_scoreboard;
    uvm_analysis_imp #(apb_transaction, apb_scoreboard) ap;
    bit [31:0] mem [bit[31:0]];
    int matches, mismatches;
    
    virtual function void write(apb_transaction tr);
        if (tr.write) begin
            mem[tr.addr] = tr.data;
        end else begin
            bit [31:0] expected = mem.exists(tr.addr) ? mem[tr.addr] : 32'h0;
            if (tr.data === expected)
                matches++;
            else begin
                mismatches++;
                `uvm_error("SCOREBOARD", $sformatf(
                    "Mismatch: addr=%h, exp=%h, got=%h",
                    tr.addr, expected, tr.data))
            end
        end
    endfunction
endclass
```

---

*整理自验证知识库*
