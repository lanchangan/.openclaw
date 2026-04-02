# AXI3 协议详解

> 整理自 ARM AMBA AXI3 协议规范 v1.0

## 目录

1. [协议概述](#1-协议概述)
2. [信号定义](#2-信号定义)
3. [传输机制](#3-传输机制)
4. [突发传输](#4-突发传输)
5. [握手协议](#5-握手协议)
6. [设计实例](#6-设计实例)

---

## 1. 协议概述

### 1.1 AXI3 简介

AXI3 (Advanced eXtensible Interface 3) 是 ARM AMBA 3 规范中的高性能片上总线协议。

**核心特性**:
- **独立通道架构**: 读写地址/数据/响应通道独立
- **突发传输**: 单次地址传输多个数据
- **乱序支持**: 支持乱序完成
- **寄存器切片**: 支持流水线化
- **低功耗**: 支持时钟门控

**性能指标**:
| 参数 | 数值 |
|------|------|
| 最大突发长度 | 16 (写) / 16 (读) |
| 数据宽度 | 8/16/32/64/128/256/512/1024 bit |
| 地址宽度 | 32/64 bit |
| ID 宽度 | 可配置 |

### 1.2 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        AXI Master                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Write Address │  │ Write Data   │  │ Write Response│          │
│  │    Channel    │  │   Channel    │  │    Channel    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│         ▼                 ▼                 ▼                   │
│  ┌─────────────────────────────────────────────────────┐        │
│  │                    AXI Interconnect                  │        │
│  └─────────────────────────────────────────────────────┘        │
│         │                 │                 ▲                   │
│         │                 ▼                 │                   │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌─────┴───────┐          │
│  │ Read Address  │  │  Read Data   │  │   (Response) │          │
│  │    Channel    │  │   Channel    │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                        AXI Slave                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 信号定义

### 2.1 全局信号

| 信号 | 方向 | 描述 |
|------|------|------|
| ACLK | 时钟 | 全局时钟信号 |
| ARESETn | 复位 | 全局复位，低有效 |

### 2.2 写地址通道 (Write Address Channel)

| 信号 | 宽度 | 描述 |
|------|------|------|
| AWID[WID_WIDTH-1:0] | ID | 写地址事务 ID |
| AWADDR[ADDR_WIDTH-1:0] | 地址 | 写地址 |
| AWLEN[3:0] | 4bit | 突发长度 (1-16) |
| AWSIZE[2:0] | 3bit | 每次传输字节数 |
| AWBURST[1:0] | 2bit | 突发类型 |
| AWLOCK[1:0] | 2bit | 锁定类型 |
| AWCACHE[3:0] | 4bit | 缓存属性 |
| AWPROT[2:0] | 3bit | 保护属性 |
| AWVALID | 1bit | 地址有效 |
| AWREADY | 1bit | 从机就绪 |

### 2.3 写数据通道 (Write Data Channel)

| 信号 | 宽度 | 描述 |
|------|------|------|
| WID[WID_WIDTH-1:0] | ID | 写数据事务 ID |
| WDATA[DATA_WIDTH-1:0] | 数据 | 写数据 |
| WSTRB[DATA_WIDTH/8-1:0] | 选通 | 写选通，每字节 1 bit |
| WLAST | 1bit | 最后一个数据 |
| WVALID | 1bit | 数据有效 |
| WREADY | 1bit | 从机就绪 |

### 2.4 写响应通道 (Write Response Channel)

| 信号 | 宽度 | 描述 |
|------|------|------|
| BID[WID_WIDTH-1:0] | ID | 响应事务 ID |
| BRESP[1:0] | 2bit | 写响应 |
| BVALID | 1bit | 响应有效 |
| BREADY | 1bit | 主机就绪 |

**BRESP 响应值**:
| 值 | 名称 | 描述 |
|------|------|------|
| 2'b00 | OKAY | 正常成功 |
| 2'b01 | EXOKAY | 独占访问成功 |
| 2'b10 | SLVERR | 从机错误 |
| 2'b11 | DECERR | 解码错误 |

### 2.5 读地址通道 (Read Address Channel)

| 信号 | 宽度 | 描述 |
|------|------|------|
| ARID[RID_WIDTH-1:0] | ID | 读地址事务 ID |
| ARADDR[ADDR_WIDTH-1:0] | 地址 | 读地址 |
| ARLEN[3:0] | 4bit | 突发长度 (1-16) |
| ARSIZE[2:0] | 3bit | 每次传输字节数 |
| ARBURST[1:0] | 2bit | 突发类型 |
| ARLOCK[1:0] | 2bit | 锁定类型 |
| ARCACHE[3:0] | 4bit | 缓存属性 |
| ARPROT[2:0] | 3bit | 保护属性 |
| ARVALID | 1bit | 地址有效 |
| ARREADY | 1bit | 从机就绪 |

### 2.6 读数据通道 (Read Data Channel)

| 信号 | 宽度 | 描述 |
|------|------|------|
| RID[RID_WIDTH-1:0] | ID | 读数据事务 ID |
| RDATA[DATA_WIDTH-1:0] | 数据 | 读数据 |
| RRESP[1:0] | 2bit | 读响应 |
| RLAST | 1bit | 最后一个数据 |
| RVALID | 1bit | 数据有效 |
| RREADY | 1bit | 主机就绪 |

---

## 3. 传输机制

### 3.1 握手协议

AXI 使用 VALID/READY 握手机制：

```
        ┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐
ACLK    │   │   │   │   │   │   │   │   │   │
      ──┘   └───┘   └───┘   └───┘   └───┘   └───

        ┌───────────────────┐
VALID ──┘                   └──────────────────

            ┌───────────────────┐
READY ──────┘                   └──────────────

                ┌───────────────┐
DATA   ─────────┘  TRANSFER     └──────────────
```

**握手规则**:
- VALID 变高后必须保持，直到 READY 变高
- READY 可以在 VALID 之前或之后变高
- 数据传输发生在 VALID && READY 的时钟沿

### 3.2 单次写传输

```
1. Master 发送 AWADDR + AWVALID
2. Slave 返回 AWREADY
3. Master 发送 WDATA + WVALID
4. Slave 返回 WREADY
5. Slave 返回 BRESP + BVALID
6. Master 返回 BREADY
```

### 3.3 单次读传输

```
1. Master 发送 ARADDR + ARVALID
2. Slave 返回 ARREADY
3. Slave 返回 RDATA + RVALID
4. Master 返回 RREADY
```

---

## 4. 突发传输

### 4.1 突发类型 (ARBURST/AWBURST)

| 值 | 类型 | 描述 |
|------|------|------|
| 2'b00 | FIXED | 固定地址 (FIFO) |
| 2'b01 | INCR | 递增地址 (常规) |
| 2'b10 | WRAP | 环绕地址 (Cache line) |
| 2'b11 | Reserved | 保留 |

### 4.2 突发长度 (ARLEN/AWLEN)

```
实际突发长度 = AWLEN + 1

AWLEN = 0  → 1 次传输
AWLEN = 3  → 4 次传输
AWLEN = 15 → 16 次传输 (最大)
```

### 4.3 传输大小 (ARSIZE/AWSIZE)

| 值 | 字节数 | 数据位宽 (假设 32-bit 总线) |
|------|--------|------------------------------|
| 3'b000 | 1 | 8 bit |
| 3'b001 | 2 | 16 bit |
| 3'b010 | 4 | 32 bit |
| 3'b011 | 8 | 64 bit (需 64-bit 总线) |
| 3'b100 | 16 | 128 bit |
| 3'b101 | 32 | 256 bit |
| 3'b110 | 64 | 512 bit |
| 3'b111 | 128 | 1024 bit |

### 4.4 地址计算

```
INCR 突发:
  地址_n = 起始地址 + n × 传输大小

WRAP 突发:
  边界 = 传输大小 × 突发长度
  地址_n = (起始地址 + n × 传输大小) % 边界 + 起始地址低bits
```

---

## 5. 握手协议详解

### 5.1 VALID 信号规则

```verilog
// VALID 必须保持直到 READY 有效
always @(posedge ACLK or negedge ARESETn) begin
    if (!ARESETn) begin
        AWVALID <= 1'b0;
    end else begin
        if (AWVALID && AWREADY) begin
            AWVALID <= 1'b0;  // 握手成功，拉低
        end else if (aw_valid_req && !AWVALID) begin
            AWVALID <= 1'b1;  // 新请求
        end
    end
end
```

### 5.2 READY 信号规则

```verilog
// READY 可以随时变化
always @(posedge ACLK or negedge ARESETn) begin
    if (!ARESETn) begin
        AWREADY <= 1'b0;
    end else begin
        // 可以根据内部状态设置
        AWREADY <= !fifo_full;
    end
end
```

### 5.3 死锁避免

**关键原则**:
1. VALID 绝不能依赖 READY
2. READY 可以依赖 VALID
3. 等待 READY 时保持 VALID

```verilog
// 错误示例 - 死锁
assign AWVALID = AWREADY && has_data;  // ✗ 错误！

// 正确示例
assign AWVALID = has_data;  // ✓ 正确
```

---

## 6. 设计实例

### 6.1 简单 AXI Master

```verilog
module axi_master #(
    parameter ADDR_WIDTH = 32,
    parameter DATA_WIDTH = 32,
    parameter ID_WIDTH = 4
)(
    input  logic                    ACLK,
    input  logic                    ARESETn,
    
    // 写地址通道
    output logic [ID_WIDTH-1:0]     AWID,
    output logic [ADDR_WIDTH-1:0]   AWADDR,
    output logic [3:0]              AWLEN,
    output logic [2:0]              AWSIZE,
    output logic [1:0]              AWBURST,
    output logic                    AWVALID,
    input  logic                    AWREADY,
    
    // 写数据通道
    output logic [DATA_WIDTH-1:0]   WDATA,
    output logic [DATA_WIDTH/8-1:0] WSTRB,
    output logic                    WLAST,
    output logic                    WVALID,
    input  logic                    WREADY,
    
    // 写响应通道
    input  logic [ID_WIDTH-1:0]     BID,
    input  logic [1:0]              BRESP,
    input  logic                    BVALID,
    output logic                    BREADY,
    
    // 读地址通道
    output logic [ID_WIDTH-1:0]     ARID,
    output logic [ADDR_WIDTH-1:0]   ARADDR,
    output logic [3:0]              ARLEN,
    output logic [2:0]              ARSIZE,
    output logic [1:0]              ARBURST,
    output logic                    ARVALID,
    input  logic                    ARREADY,
    
    // 读数据通道
    input  logic [ID_WIDTH-1:0]     RID,
    input  logic [DATA_WIDTH-1:0]   RDATA,
    input  logic [1:0]              RRESP,
    input  logic                    RLAST,
    input  logic                    RVALID,
    output logic                    RREADY,
    
    // 用户接口
    input  logic                    start_write,
    input  logic [ADDR_WIDTH-1:0]   write_addr,
    input  logic [DATA_WIDTH-1:0]   write_data,
    output logic                    write_done
);

    // 状态机
    typedef enum logic [2:0] {
        IDLE,
        WRITE_ADDR,
        WRITE_DATA,
        WRITE_RESP,
        DONE
    } state_t;
    
    state_t state, next_state;
    
    always_ff @(posedge ACLK or negedge ARESETn) begin
        if (!ARESETn) begin
            state <= IDLE;
        end else begin
            state <= next_state;
        end
    end
    
    // 状态转换逻辑
    always_comb begin
        next_state = state;
        case (state)
            IDLE: begin
                if (start_write) next_state = WRITE_ADDR;
            end
            
            WRITE_ADDR: begin
                if (AWREADY) next_state = WRITE_DATA;
            end
            
            WRITE_DATA: begin
                if (WREADY) next_state = WRITE_RESP;
            end
            
            WRITE_RESP: begin
                if (BVALID) next_state = DONE;
            end
            
            DONE: begin
                next_state = IDLE;
            end
        endcase
    end
    
    // 输出逻辑
    always_ff @(posedge ACLK or negedge ARESETn) begin
        if (!ARESETn) begin
            AWVALID <= 1'b0;
            WVALID  <= 1'b0;
            BREADY  <= 1'b1;
        end else begin
            case (state)
                WRITE_ADDR: begin
                    AWADDR  <= write_addr;
                    AWVALID <= 1'b1;
                end
                
                WRITE_DATA: begin
                    WDATA  <= write_data;
                    WVALID <= 1'b1;
                    WLAST  <= 1'b1;
                end
                
                default: begin
                    AWVALID <= 1'b0;
                    WVALID  <= 1'b0;
                end
            endcase
        end
    end
    
    assign write_done = (state == DONE);

endmodule
```

### 6.2 简单 AXI Slave

```verilog
module axi_slave #(
    parameter ADDR_WIDTH = 32,
    parameter DATA_WIDTH = 32,
    parameter ID_WIDTH = 4,
    parameter MEM_DEPTH = 1024
)(
    input  logic                    ACLK,
    input  logic                    ARESETn,
    
    // 写地址通道
    input  logic [ID_WIDTH-1:0]     AWID,
    input  logic [ADDR_WIDTH-1:0]   AWADDR,
    input  logic [3:0]              AWLEN,
    input  logic [2:0]              AWSIZE,
    input  logic [1:0]              AWBURST,
    input  logic                    AWVALID,
    output logic                    AWREADY,
    
    // 写数据通道
    input  logic [DATA_WIDTH-1:0]   WDATA,
    input  logic [DATA_WIDTH/8-1:0] WSTRB,
    input  logic                    WLAST,
    input  logic                    WVALID,
    output logic                    WREADY,
    
    // 写响应通道
    output logic [ID_WIDTH-1:0]     BID,
    output logic [1:0]              BRESP,
    output logic                    BVALID,
    input  logic                    BREADY,
    
    // 读地址通道
    input  logic [ID_WIDTH-1:0]     ARID,
    input  logic [ADDR_WIDTH-1:0]   ARADDR,
    input  logic [3:0]              ARLEN,
    input  logic [2:0]              ARSIZE,
    input  logic [1:0]              ARBURST,
    input  logic                    ARVALID,
    output logic                    ARREADY,
    
    // 读数据通道
    output logic [ID_WIDTH-1:0]     RID,
    output logic [DATA_WIDTH-1:0]   RDATA,
    output logic [1:0]              RRESP,
    output logic                    RLAST,
    output logic                    RVALID,
    input  logic                    RREADY
);

    // 存储器
    logic [DATA_WIDTH-1:0] mem [0:MEM_DEPTH-1];
    
    // 写状态机
    typedef enum logic [1:0] {W_IDLE, W_ADDR, W_DATA, W_RESP} w_state_t;
    w_state_t w_state;
    
    logic [ADDR_WIDTH-1:0] wr_addr;
    logic [ID_WIDTH-1:0]   wr_id;
    
    always_ff @(posedge ACLK or negedge ARESETn) begin
        if (!ARESETn) begin
            w_state  <= W_IDLE;
            AWREADY  <= 1'b1;
            WREADY   <= 1'b0;
            BVALID   <= 1'b0;
        end else begin
            case (w_state)
                W_IDLE: begin
                    if (AWVALID) begin
                        wr_addr <= AWADDR;
                        wr_id   <= AWID;
                        AWREADY <= 1'b0;
                        WREADY  <= 1'b1;
                        w_state <= W_DATA;
                    end
                end
                
                W_DATA: begin
                    if (WVALID) begin
                        // 写入存储器
                        for (int i = 0; i < DATA_WIDTH/8; i++) begin
                            if (WSTRB[i]) begin
                                mem[wr_addr[ADDR_WIDTH-1:2] + i/4][i*8 +: 8] <= WDATA[i*8 +: 8];
                            end
                        end
                        
                        if (WLAST) begin
                            WREADY <= 1'b0;
                            BID    <= wr_id;
                            BRESP  <= 2'b00;  // OKAY
                            BVALID <= 1'b1;
                            w_state <= W_RESP;
                        end
                    end
                end
                
                W_RESP: begin
                    if (BREADY) begin
                        BVALID  <= 1'b0;
                        AWREADY <= 1'b1;
                        w_state <= W_IDLE;
                    end
                end
            endcase
        end
    end

endmodule
```

---

## 参考文档

- ARM AMBA AXI Protocol v1.0 Specification
- AMBA 3 AXI Protocol Specification

---

*整理自协议&标准知识库*
