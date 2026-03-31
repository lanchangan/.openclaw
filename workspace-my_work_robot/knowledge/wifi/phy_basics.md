# WiFi PHY 物理层基础

> WiFi 协议 PHY 层核心知识

---

## 一句话总结

> WiFi PHY 从 802.11n 到 802.11be，核心演进是：更高带宽、更高阶调制、更高效多址。

---

## 一、WiFi 代际对照表

| WiFi 代数 | IEEE 标准 | 年份 | PHY 名称 | 最大带宽 | 最大调制 | 最大速率 |
|-----------|-----------|------|----------|----------|----------|----------|
| WiFi 4 | 802.11n | 2009 | HT | 40 MHz | 64-QAM | 600 Mbps |
| WiFi 5 | 802.11ac | 2014 | VHT | 160 MHz | 256-QAM | 6.9 Gbps |
| WiFi 6/6E | 802.11ax | 2021 | HE | 160 MHz | 1024-QAM | 9.6 Gbps |
| WiFi 7 | 802.11be | 2024~ | EHT | 320 MHz | 4096-QAM | 46 Gbps |

---

## 二、PHY 核心技术演进

### 2.1 调制技术

```
WiFi 4: 64-QAM   (6 bits/symbol)
WiFi 5: 256-QAM  (8 bits/symbol)
WiFi 6: 1024-QAM (10 bits/symbol) - MCS 10, 11
WiFi 7: 4096-QAM (12 bits/symbol)
```

**QAM 阶数 vs 性能**：
- 阶数越高 → 每符号携带更多 bit → 更高速率
- 但对 SNR 要求更高，抗干扰能力下降

### 2.2 信道带宽

| 协议 | 支持带宽 |
|------|---------|
| WiFi 4 | 20, 40 MHz |
| WiFi 5 | 20, 40, 80, 80+80, 160 MHz |
| WiFi 6 | 20, 40, 80, 80+80, 160 MHz |
| WiFi 7 | 最高 320 MHz |

### 2.3 OFDM vs OFDMA

**OFDM**：所有子载波传输一个用户的数据（WiFi 4/5）

**OFDMA**：子载波分成多个 RU，多用户同时传输（WiFi 6 引入）

**RU 类型**：
- 26-tone, 52-tone, 106-tone, 242-tone, 484-tone, 996-tone

### 2.4 MIMO 演进

| 协议 | MIMO 支持 |
|------|----------|
| WiFi 4 | SU-MIMO |
| WiFi 5 | DL MU-MIMO |
| WiFi 6 | DL + UL MU-MIMO |
| WiFi 7 | 最多 16 空间流 |

### 2.5 Guard Interval

| 协议 | GI 选项 |
|------|--------|
| WiFi 4/5 | 800ns, 400ns |
| WiFi 6 | 800ns, 1.6μs, 3.2μs |

---

## 三、WiFi 7 新特性

### 3.1 MLO (Multi-Link Operation)

**优势**：
- 多链路并行传输，降低延迟
- 带宽聚合，提升吞吐
- 链路冗余，提高可靠性

**模式**：
1. Single-radio MLD：单射频，时分复用
2. EMLSR：增强型单射频
3. Multi-radio MLD：多射频，可同时收发

### 3.2 Multi-RU / MRU

- WiFi 6：单 RU 分配
- WiFi 7：支持 Multi-RU，更灵活的资源分配

### 3.3 320 MHz 带宽

- 使用 6 GHz 频段
- 理论吞吐翻倍

### 3.4 4K-QAM

- 4096-QAM，每符号 12 bits
- 对信道质量要求极高

---

## 四、MCS 表

| MCS | Modulation | Code Rate |
|-----|------------|-----------|
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
| 12 | 4096-QAM | 3/4 (WiFi 7) |
| 13 | 4096-QAM | 5/6 (WiFi 7) |

---

## 五、PHY 帧结构

```
+--------+--------+--------+--------+--------+
|  L-STF |  L-LTF | L-SIG  | RL-SIG | HE-SIG |
+--------+--------+--------+--------+--------+
|                 Data Symbols               |
+-------------------------------------------+
```

**关键字段**：
| 字段 | 作用 |
|------|------|
| L-STF | 自动增益控制、同步 |
| L-LTF | 信道估计 |
| L-SIG | 速率、长度信息 |
| HE/EHT-SIG | WiFi 6/7 特有信令 |

---

## 六、验证关注点

| 验证项 | 说明 |
|--------|------|
| 调制解调 | QAM 星座图验证 |
| 信道编码 | LDPC/BCC 编解码 |
| 同步 | 符号定时、载波频偏估计 |
| 信道估计 | 导频插入、CSI 估计 |
| MIMO | 预编码、空间流分离 |
| OFDMA | RU 分配、资源映射 |

---

## 参考资料

- IEEE 802.11 标准文档
- WiFi Alliance 技术白皮书
- MathWorks WLAN Toolbox
