# 设计知识库

本知识库整理自协议标准书籍，涵盖总线协议和接口协议。

## 知识库结构

```
design/
├── README.md              # 本文件 - 索引
├── axi_protocol.md        # AXI 总线协议
├── amba_bus.md            # AMBA 总线规范
├── i2c_protocol.md        # I2C 接口协议
└── raw/                   # 原始提取内容
```

---

## 协议清单

| 协议 | 类型 | 来源 | 主要内容 |
|------|------|------|----------|
| AXI3 | 片上总线 | ARM AMBA 3 | 高性能总线协议 |
| AMBA | 片上总线 | ARM | 总线架构规范 |
| I2C | 板级接口 | NXP | 两线式串行通信 |

---

## 快速参考

### AXI3 关键特性
- 5 个独立通道: Write Address, Write Data, Write Response, Read Address, Read Data
- 支持突发传输
- 支持乱序操作
- 支持寄存器切片

### AMBA 总线
- AHB: 高性能总线
- APB: 外设总线
- AXI: 高级扩展接口

### I2C 协议
- 两线: SDA (数据) + SCL (时钟)
- 支持多主多从
- 7-bit/10-bit 寻址
- 多种速率模式

---

*生成时间: 2026-04-01*
