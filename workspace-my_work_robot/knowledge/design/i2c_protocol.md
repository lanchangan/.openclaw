# I2C 协议详解

> 整理自 I2C 总线规范

## 目录

1. [协议概述](#1-协议概述)
2. [信号定义](#2-信号定义)
3. [时序规范](#3-时序规范)
4. [传输协议](#4-传输协议)
5. [设计实例](#5-设计实例)

---

## 1. 协议概述

### 1.1 I2C 简介

I2C (Inter-Integrated Circuit) 是一种两线式串行通信协议，由 Philips（现 NXP）开发。

**核心特性**:
- **两线通信**: SDA (数据) + SCL (时钟)
- **多主多从**: 支持多个主设备和从设备
- **地址寻址**: 7-bit 或 10-bit 地址
- **应答机制**: 每字节传输后需要应答
- **多种速率**: 标准模式、快速模式、高速模式

### 1.2 速率模式

| 模式 | 速率 | 描述 |
|------|------|------|
| 标准模式 | 100 kbps | 原始版本 |
| 快速模式 | 400 kbps | 兼容标准模式 |
| 快速模式+ | 1 Mbps | 增强版 |
| 高速模式 | 3.4 Mbps | 需要特殊时序 |
| 超快模式 | 5 Mbps | 单向传输 |

### 1.3 总线拓扑

```
            VCC
             │
    ┌────────┼────────┐
    │        │        │
   Rp       Rp       Rp (上拉电阻)
    │        │        │
    │   ┌────┴────┐   │
    │   │         │   │
   SDA  │   总线   │  SCL
    │   │         │   │
    │   └────┬────┘   │
    │        │        │
   ├──┬──┬───┼───┬──┬──┤
   │  │  │   │   │  │  │
  M1 M2 S1  S2  S3 S4 Sn
   
   M = Master (主设备)
   S = Slave (从设备)
   Rp = 上拉电阻 (典型值 4.7kΩ)
```

---

## 2. 信号定义

### 2.1 信号线

| 信号 | 方向 | 描述 |
|------|------|------|
| SDA | 双向 | 串行数据线 |
| SCL | 双向 | 串行时钟线 |

### 2.2 总线状态

| 状态 | SDA | SCL | 描述 |
|------|-----|-----|------|
| 空闲 | 高 | 高 | 无数据传输 |
| 启动 | 高→低 | 高 | START 条件 |
| 停止 | 低→高 | 高 | STOP 条件 |
| 数据变化 | 变化 | 低 | 数据可变 |
| 数据有效 | 稳定 | 高 | 采样数据 |

### 2.3 START 和 STOP 条件

```
       _____       _____
SCL         |_____|     |_____
      ____________
SDA              |_____
                  ↑
              START 条件
(SDA 在 SCL 高电平时下降沿)

       _____
SCL         |_____
                 _____
SDA        _____|
               ↑
           STOP 条件
(SDA 在 SCL 高电平时上升沿)
```

---

## 3. 时序规范

### 3.1 标准模式时序参数

| 参数 | 符号 | 最小值 | 典型值 | 最大值 |
|------|------|--------|--------|--------|
| SCL 时钟频率 | fSCL | 0 | - | 100 kHz |
| START 保持时间 | tHD;STA | 4.0 μs | - | - |
| START 建立时间 | tSU;STA | 4.7 μs | - | - |
| 数据保持时间 | tHD;DAT | 0 | - | 3.45 μs |
| 数据建立时间 | tSU;DAT | 250 ns | - | - |
| STOP 建立时间 | tSU;STO | 4.0 μs | - | - |
| 总线空闲时间 | tBUF | 4.7 μs | - | - |

### 3.2 快速模式时序参数

| 参数 | 符号 | 最小值 | 典型值 | 最大值 |
|------|------|--------|--------|--------|
| SCL 时钟频率 | fSCL | 0 | - | 400 kHz |
| START 保持时间 | tHD;STA | 0.6 μs | - | - |
| START 建立时间 | tSU;STA | 0.6 μs | - | - |
| 数据保持时间 | tHD;DAT | 0 | - | 0.9 μs |
| 数据建立时间 | tSU;DAT | 100 ns | - | - |
| STOP 建立时间 | tSU;STO | 0.6 μs | - | - |
| 总线空闲时间 | tBUF | 1.3 μs | - | - |

---

## 4. 传输协议

### 4.1 数据帧格式

```
START | 从地址(7bit) | R/W(1bit) | ACK | 数据(8bit) | ACK | ... | STOP
  │         │           │         │        │          │
  │         │           │         │        │          └─ 从机应答
  │         │           │         │        └─ 数据字节
  │         │           │         └─ 从机应答 (0=ACK, 1=NACK)
  │         │           └─ 读/写位 (0=写, 1=读)
  │         └─ 从机地址
  └─ 启动条件
```

### 4.2 7-bit 地址格式

```
     ┌──────────────────────────┬───┐
     │     从机地址 (7-bit)      │R/W│
     ├───┬───┬───┬───┬───┬───┬───┼───┤
     │A6 │A5 │A4 │A3 │A2 │A1 │A0 │R/W│
     └───┴───┴───┴───┴───┴───┴───┴───┘
      MSB                         LSB
```

### 4.3 10-bit 地址格式

```
     ┌────────────┬───┬───┬─────────────────┬───┐
     │  11110     │A9 │A8 │    A7-A0        │R/W│
     ├───┬───┬───┬───┼───┼───┬───┬───┬───┬───┼───┤
     │ 1 │ 1 │ 1 │ 1 │ 0 │A9 │A8 │   │   │   │R/W│
     └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
      第一字节                      第二字节
```

### 4.4 写传输序列

```
主机:  START | 地址+写 |     | 数据1 |     | 数据2 |     | STOP
                    ↓         ↓         ↓         ↓
从机:              ACK       ACK       ACK
```

### 4.5 读传输序列

```
主机:  START | 地址+读 |     |      | 数据1 |      | 数据2 | NACK | STOP
                    ↓         ↓               ↓
从机:              ACK       数据1           数据2
```

### 4.6 重复 START

```
主机:  START | 地址1+写 | ACK | 数据 | ACK | Sr | 地址2+读 | ACK | ...
                                           ↑
                                      重复 START (Sr)
                                      
用途：不释放总线的情况下切换方向或设备
```

---

## 5. 设计实例

### 5.1 I2C Master 控制器

```verilog
module i2c_master #(
    parameter CLK_FREQ = 50_000_000,  // 系统时钟频率
    parameter I2C_FREQ = 400_000      // I2C 频率
)(
    input  logic        clk,
    input  logic        rst_n,
    
    // I2C 接口
    inout  logic        sda,
    inout  logic        scl,
    
    // 用户接口
    input  logic        start,
    input  logic        read_write,   // 0=写, 1=读
    input  logic [6:0]  addr,
    input  logic [7:0]  wr_data,
    output logic [7:0]  rd_data,
    output logic        done,
    output logic        ack_error
);

    // 时钟分频
    localparam DIV = CLK_FREQ / (I2C_FREQ * 4);
    logic [15:0] clk_cnt;
    logic [1:0]  clk_phase;
    logic        scl_tick;
    
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            clk_cnt <= 0;
            clk_phase <= 0;
        end else if (clk_cnt >= DIV - 1) begin
            clk_cnt <= 0;
            clk_phase <= clk_phase + 1;
        end else begin
            clk_cnt <= clk_cnt + 1;
        end
    end
    
    assign scl_tick = (clk_cnt == DIV - 1);
    
    // 状态机
    typedef enum logic [3:0] {
        IDLE,
        START,
        ADDR_0, ADDR_1, ADDR_2, ADDR_3, ADDR_4, ADDR_5, ADDR_6,
        RW,
        ACK_ADDR,
        DATA_0, DATA_1, DATA_2, DATA_3, DATA_4, DATA_5, DATA_6, DATA_7,
        ACK_DATA,
        STOP,
        DONE_ST
    } state_t;
    
    state_t state, next_state;
    logic [7:0] shift_reg;
    logic [3:0] bit_cnt;
    logic       sda_out, scl_out;
    logic       sda_in, scl_in;
    
    // 三态缓冲
    assign sda = sda_out ? 1'bz : 1'b0;
    assign scl = scl_out ? 1'bz : 1'b0;
    assign sda_in = sda;
    assign scl_in = scl;
    
    // 状态转换
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
        end else if (scl_tick) begin
            state <= next_state;
        end
    end
    
    // 组合逻辑
    always_comb begin
        next_state = state;
        
        case (state)
            IDLE: if (start) next_state = START;
            
            START: next_state = ADDR_0;
            
            ADDR_0: next_state = ADDR_1;
            ADDR_1: next_state = ADDR_2;
            ADDR_2: next_state = ADDR_3;
            ADDR_3: next_state = ADDR_4;
            ADDR_4: next_state = ADDR_5;
            ADDR_5: next_state = ADDR_6;
            ADDR_6: next_state = RW;
            
            RW: next_state = ACK_ADDR;
            
            ACK_ADDR: next_state = DATA_0;
            
            DATA_0: next_state = DATA_1;
            DATA_1: next_state = DATA_2;
            DATA_2: next_state = DATA_3;
            DATA_3: next_state = DATA_4;
            DATA_4: next_state = DATA_5;
            DATA_5: next_state = DATA_6;
            DATA_6: next_state = DATA_7;
            DATA_7: next_state = ACK_DATA;
            
            ACK_DATA: next_state = STOP;
            
            STOP: next_state = DONE_ST;
            
            DONE_ST: next_state = IDLE;
        endcase
    end
    
    // 输出逻辑
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sda_out <= 1;
            scl_out <= 1;
            shift_reg <= 0;
            ack_error <= 0;
            done <= 0;
            rd_data <= 0;
        end else if (scl_tick) begin
            done <= 0;
            
            case (state)
                IDLE: begin
                    sda_out <= 1;
                    scl_out <= 1;
                    shift_reg <= {addr, read_write};
                end
                
                START: begin
                    // START 条件：SCL 高时 SDA 下降
                    if (clk_phase == 0) sda_out <= 0;
                    if (clk_phase == 1) scl_out <= 0;
                end
                
                ADDR_0, ADDR_1, ADDR_2, ADDR_3,
                ADDR_4, ADDR_5, ADDR_6, RW: begin
                    // 发送地址位
                    scl_out <= (clk_phase >= 2);
                    sda_out <= shift_reg[7];
                    if (clk_phase == 3) shift_reg <= shift_reg << 1;
                end
                
                ACK_ADDR: begin
                    scl_out <= (clk_phase >= 2);
                    if (clk_phase == 2) ack_error <= sda_in;
                end
                
                DATA_0, DATA_1, DATA_2, DATA_3,
                DATA_4, DATA_5, DATA_6, DATA_7: begin
                    scl_out <= (clk_phase >= 2);
                    if (read_write) begin
                        // 读模式
                        if (clk_phase == 2) rd_data <= {rd_data[6:0], sda_in};
                    end else begin
                        // 写模式
                        sda_out <= wr_data[7 - (state - DATA_0)];
                    end
                end
                
                ACK_DATA: begin
                    scl_out <= (clk_phase >= 2);
                    if (read_write) sda_out <= 1;  // NACK for last read
                end
                
                STOP: begin
                    // STOP 条件：SCL 高时 SDA 上升
                    scl_out <= 1;
                    if (clk_phase >= 2) sda_out <= 1;
                end
                
                DONE_ST: begin
                    done <= 1;
                end
            endcase
        end
    end

endmodule
```

### 5.2 I2C Slave 控制器

```verilog
module i2c_slave #(
    parameter [6:0] SLAVE_ADDR = 7'h50
)(
    input  logic        clk,
    input  logic        rst_n,
    
    // I2C 接口
    inout  logic        sda,
    inout  logic        scl,
    
    // 用户接口
    output logic [7:0]  rx_data,
    output logic        rx_valid,
    input  logic [7:0]  tx_data,
    input  logic        tx_ready
);

    // 同步输入
    logic sda_sync, scl_sync;
    logic sda_prev, scl_prev;
    
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sda_sync <= 1;
            scl_sync <= 1;
            sda_prev <= 1;
            scl_prev <= 1;
        end else begin
            sda_prev <= sda_sync;
            scl_prev <= scl_sync;
            sda_sync <= sda;
            scl_sync <= scl;
        end
    end
    
    // 边沿检测
    wire sda_fall = sda_prev & ~sda_sync;
    wire sda_rise = ~sda_prev & sda_sync;
    wire scl_rise = ~scl_prev & scl_sync;
    wire scl_fall = scl_prev & ~sda_sync;
    
    // START/STOP 检测
    wire start_cond = scl_sync & sda_fall;
    wire stop_cond  = scl_sync & sda_rise;
    
    // 状态机
    typedef enum logic [2:0] {
        IDLE,
        ADDR,
        ACK_ADDR,
        DATA,
        ACK_DATA
    } state_t;
    
    state_t state;
    logic [7:0] shift_reg;
    logic [3:0] bit_cnt;
    logic       addr_match;
    logic       is_read;
    logic       sda_out;
    
    // 三态
    assign sda = sda_out ? 1'bz : 1'b0;
    
    // 状态机
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            shift_reg <= 0;
            bit_cnt <= 0;
            addr_match <= 0;
            sda_out <= 1;
        end else begin
            // START 条件
            if (start_cond) begin
                state <= ADDR;
                shift_reg <= 0;
                bit_cnt <= 0;
                sda_out <= 1;
            end
            // STOP 条件
            else if (stop_cond) begin
                state <= IDLE;
                sda_out <= 1;
            end
            // SCL 上升沿采样
            else if (scl_rise) begin
                case (state)
                    ADDR: begin
                        shift_reg <= {shift_reg[6:0], sda_sync};
                        bit_cnt <= bit_cnt + 1;
                        if (bit_cnt == 7) begin
                            addr_match <= (shift_reg[6:0] == SLAVE_ADDR);
                            is_read <= sda_sync;
                            state <= ACK_ADDR;
                        end
                    end
                    
                    DATA: begin
                        shift_reg <= {shift_reg[6:0], sda_sync};
                        bit_cnt <= bit_cnt + 1;
                        if (bit_cnt == 7) begin
                            rx_data <= {shift_reg[6:0], sda_sync};
                            rx_valid <= 1;
                            state <= ACK_DATA;
                        end
                    end
                endcase
            end
            // SCL 下降沿输出
            else if (scl_fall) begin
                case (state)
                    ACK_ADDR: begin
                        if (addr_match) begin
                            sda_out <= 0;  // ACK
                        end
                        state <= DATA;
                        bit_cnt <= 0;
                    end
                    
                    ACK_DATA: begin
                        sda_out <= 0;  // ACK
                        state <= DATA;
                        bit_cnt <= 0;
                        rx_valid <= 0;
                    end
                endcase
            end
        end
    end

endmodule
```

---

## 参考文档

- NXP I2C-bus specification and user manual (UM10204)
- I2C 总线规范简易版

---

*整理自协议&标准知识库*
