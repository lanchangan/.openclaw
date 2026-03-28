# WiFi PHY 物理层知识整理

> 小E的学习笔记 - 持续更新中

---

## 一、WiFi 代际对照表

| WiFi 代数 | IEEE 标准 | 年份 | PHY 名称 | 最大带宽 | 最大调制 | 最大速率 |
|-----------|-----------|------|----------|----------|----------|----------|
| WiFi 4 | 802.11n | 2009 | HT (High Throughput) | 40 MHz | 64-QAM | 600 Mbps |
| WiFi 5 | 802.11ac | 2014 | VHT (Very High Throughput) | 160 MHz | 256-QAM | 6.9 Gbps |
| WiFi 6/6E | 802.11ax | 2021 | HEW (High Efficiency Wireless) | 160 MHz | 1024-QAM | 9.6 Gbps |
| WiFi 7 | 802.11be | 2024~ | EHT (Extremely High Throughput) | 320 MHz | 4096-QAM | 46 Gbps |
| WiFi 8 | 802.11bn | TBD | - | TBD | TBD | >100 Gbps |

---

## 二、PHY 层核心技术演进

### 2.1 调制技术 (Modulation)

```
WiFi 4: 64-QAM   (6 bits/symbol)
WiFi 5: 256-QAM  (8 bits/symbol)
WiFi 6: 1024-QAM (10 bits/symbol) - MCS 10, 11
WiFi 7: 4096-QAM (12 bits/symbol)
```

**QAM (正交幅度调制)** 要点：
- QAM阶数越高 → 每符号携带更多bit → 更高速率
- 但对 SNR 要求更高，抗干扰能力下降
- 需要更好的信道条件和硬件性能

### 2.2 信道带宽 (Channel Bandwidth)

```
WiFi 4: 20, 40 MHz
WiFi 5: 20, 40, 80, 80+80, 160 MHz
WiFi 6: 20, 40, 80, 80+80, 160 MHz
WiFi 7: 最高 320 MHz
```

### 2.3 OFDM vs OFDMA (WiFi 6 核心技术)

**OFDM (正交频分复用)**：
- 所有子载波传输一个用户的数据
- WiFi 4/5 使用

**OFDMA (正交频分多址)**：
- 子载波分成多个 RU (Resource Unit)
- 多用户可同时传输，降低延迟
- WiFi 6 引入，支持 DL 和 UL

RU 类型：
- 26-tone RU, 52-tone RU, 106-tone RU, 242-tone RU, 484-tone RU, 996-tone RU

### 2.4 MIMO 演进

```
WiFi 4: SU-MIMO (单用户MIMO)
WiFi 5: DL MU-MIMO (下行多用户MIMO)
WiFi 6: DL + UL MU-MIMO (上下行多用户MIMO)
WiFi 7: 最多 16 空间流
```

### 2.5 Guard Interval (保护间隔)

```
WiFi 4/5: 800ns, 400ns
WiFi 6: 800ns, 1.6μs, 3.2μs (更好抗多径)
```

---

## 三、WiFi 7 新特性

### 3.1 MLO (Multi-Link Operation)

多链路操作是 WiFi 7 最重要的特性：

**优势**：
- 多链路并行传输，降低延迟
- 带宽聚合，提升吞吐
- 链路冗余，提高可靠性

**模式**：
1. **Single-radio MLD**: 单射频，时分复用
2. **EMLSR (Enhanced Multi-Link Single-Radio)**: 增强型单射频
3. **Multi-radio MLD**: 多射频，可同时收发

### 3.2 Multi-RU

- WiFi 6: 单 RU 分配
- WiFi 7: 支持 Multi-RU，更灵活的资源分配

### 3.3 320 MHz 带宽

- 使用 6 GHz 频段
- 理论吞吐翻倍

### 3.4 4K-QAM

- 4096-QAM，每符号 12 bits
- 对信道质量要求极高

---

## 四、验证工程师关注点

### 4.1 PHY 帧结构

```
+--------+--------+--------+--------+--------+
|  L-STF |  L-LTF | L-SIG  | RL-SIG | HE-SIG |
+--------+--------+--------+--------+--------+
|                 Data Symbols               |
+-------------------------------------------+
```

关键字段：
- **L-STF**: Legacy Short Training Field (自动增益控制、同步)
- **L-LTF**: Legacy Long Training Field (信道估计)
- **L-SIG**: Legacy Signal (速率、长度信息)
- **HE-SIG**: High Efficiency Signal (WiFi 6 特有)

### 4.2 MCS 表 (Modulation and Coding Scheme)

| MCS Index | Modulation | Code Rate |
|-----------|------------|-----------|
| 0 | BPSK | 1/2 |
| 1 | QPSK | 1/2 |
| 2 | QPSK | 3/4 |
| 3 | 16-QAM | 1/2 |
| 4 | 16-QAM | 3/4 |
| 5 | 64-QAM | 2/3 |
| 6 | 64-QAM | 3/4 |
| 7 | 64-QAM | 5/6 |
| 8 | 256-QAM | 3/4 |
| 9 | 256-QAM | 5/6 |
| 10 | 1024-QAM | 3/4 |
| 11 | 1024-QAM | 5/6 |

### 4.3 验证要点

1. **调制解调**: QAM 星座图验证
2. **信道编码**: LDPC/BCC 编解码
3. **同步**: 符号定时、载波频偏估计
4. **信道估计**: 导频插入、CSI 估计
5. **MIMO**: 预编码、空间流分离
6. **OFDMA**: RU 分配、资源映射

---

## 五、协议文档获取

### 官方标准 (需购买)
- IEEE 802.11 标准文档：https://standards.ieee.org
- 价格较贵，企业通常会购买

### 公开资源
- WiFi Alliance 技术白皮书
- 各芯片厂商技术文档 (Qualcomm, Broadcom, MediaTek)
- 学术论文和技术博客

### 推荐学习路径
1. 先看技术概述白皮书
2. 学习 PHY 帧结构和信号流程
3. 深入各模块：调制、编码、MIMO、OFDMA
4. 结合仿真工具 (MATLAB WLAN Toolbox)

---

## 六、后续学习计划

- [ ] WiFi 6 OFDMA RU 分配机制详解
- [ ] WiFi 7 MLO 协议细节
- [ ] PHY 状态机设计
- [ ] 信道模型与仿真
- [ ] AP vs STA 验证差异

---

*小E 整理于 2026-03-26*
*持续更新中...*