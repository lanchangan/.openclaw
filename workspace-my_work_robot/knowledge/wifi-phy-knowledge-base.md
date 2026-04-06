# WiFi PHY 知识库

> 芯片验证工程师专用 | WiFi 6/7 PHY 层技术参考

---

## 一、协议概览

### 1.1 WiFi 6 (802.11ax) - High Efficiency WLAN

| 特性 | 参数 |
|------|------|
| 标准代号 | IEEE P802.11ax/D8.0 (2020年10月) |
| 核心目标 | 高效率无线局域网（HE WLAN） |
| 频段 | 1 GHz ~ 7.125 GHz（2.4GHz、5GHz、6GHz） |
| 关键技术 | OFDMA、MU-MIMO、1024-QAM |

### 1.2 WiFi 7 (802.11be) - Extremely High Throughput (EHT)

| 特性 | 参数 |
|------|------|
| 标准代号 | IEEE P802.11be/D3.0 (2023年1月) |
| 核心目标 | 极高吞吐量（EHT），MAC 层吞吐 ≥ 30 Gbit/s |
| 频段 | 1 GHz ~ 7.250 GHz |
| 关键技术 | 320 MHz 带宽、4K QAM、MLO、16 空间流 |

### 1.3 WiFi 6 vs WiFi 7 关键差异

| 特性 | WiFi 6 (HE) | WiFi 7 (EHT) |
|------|-------------|--------------|
| 最大带宽 | 160 MHz | 320 MHz |
| 最大子载波 | 1992 | 3984 |
| 最大空间流 | 8 | 16 |
| 最高调制 | 1024-QAM (10 bits) | 4096-QAM (12 bits) |
| 前导码 | HE-SIG-A/B | U-SIG + EHT-SIG |

---

## 二、HE PPDU 格式

### 2.1 四种 PPDU 格式

| PPDU 格式 | 用途 | 特点 |
|-----------|------|------|
| HE SU PPDU | 单用户传输 | HE-SIG-A 不重复 |
| HE MU PPDU | 多用户下行传输 | 包含 HE-SIG-B 字段 |
| HE ER SU PPDU | 扩展范围单用户 | HE-SIG-A 长度为两倍 |
| HE TB PPDU | 触发式上行传输 | HE-STF 持续时间为两倍 |

### 2.2 PPDU 字段结构

```
L-STF (8µs) → L-LTF (8µs) → L-SIG (4µs) → RL-SIG (4µs) 
→ HE-SIG-A (8µs) → HE-STF (4µs) → HE-LTF (可变) → Data → PE
```

### 2.3 关键时序参数

| 参数 | 值 | 说明 |
|------|-----|------|
| L-STF | 8 µs | 非HT短训练字段 |
| L-LTF | 8 µs | 非HT长训练字段 |
| L-SIG | 4 µs | 非HT信号字段 |
| HE-SIG-A | 8 µs | HE信号A字段 |
| HE-STF | 4 µs (SU/MU) / 8 µs (TB) | HE短训练字段 |

---

## 三、OFDMA 资源单元 (RU)

### 3.1 RU 类型

| RU 类型 | 数据子载波 | 导频子载波 | 适用带宽 |
|---------|-----------|-----------|----------|
| 26-tone | 24 | 2 | 20/40/80/160 MHz |
| 52-tone | 48 | 4 | 20/40/80/160 MHz |
| 106-tone | 102 | 4 | 20/40/80/160 MHz |
| 242-tone | 234 | 8 | 20/40/80/160 MHz |
| 484-tone | 468 | 16 | 40/80/160 MHz |
| 996-tone | 980 | 16 | 80/160 MHz |
| 2×996-tone | 1960 | 32 | 160 MHz |

### 3.2 各带宽最大 RU 数量

| RU 类型 | 20 MHz | 40 MHz | 80 MHz | 160 MHz |
|---------|--------|--------|--------|---------|
| 26-tone | 9 | 18 | 37 | 74 |
| 52-tone | 4 | 8 | 16 | 32 |
| 106-tone | 2 | 4 | 8 | 16 |
| 242-tone | 1 | 2 | 4 | 8 |
| 484-tone | N/A | 1 | 2 | 4 |
| 996-tone | N/A | N/A | 1 | 2 |

---

## 四、MU-MIMO 机制

### 4.1 DL MU-MIMO（下行）

- RU 大小 ≥ 106-tone 时支持部分带宽 DL MU-MIMO
- 全带宽 MU-MIMO：最大空间流数 = min(4, HE SU PPDU 最大空间流数)
- 带宽 ≤ 80 MHz：总空间流 ≤ Beamformee STS ≤ 80 MHz
- 带宽 > 80 MHz：总空间流 ≤ Beamformee STS > 80 MHz

### 4.2 UL MU-MIMO（上行）

- RU 大小 ≥ 106-tone 时支持部分带宽 UL MU-MIMO
- 每用户空间流：1 ~ min(4, 最大支持空间流)
- 总空间流 ≤ 8

### 4.3 HE-LTF 模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| HE single stream pilot HE-LTF mode | 单流导频 | 部分带宽 UL MU-MIMO |
| HE masked HE-LTF sequence mode | 掩码序列 | 全带宽 UL MU-MIMO |
| HE no pilot HE-LTF mode (1× HE-LTF) | 无导频 | 特殊配置 |

---

## 五、WiFi 7 新特性

### 5.1 EHT PPDU 格式

| PPDU 格式 | 用途 | U-SIG 设置 |
|-----------|------|------------|
| EHT MU PPDU | 多用户下行传输 | UL/DL = 0, PPDU Type = 0/1/2 |
| EHT TB PPDU | 触发式上行传输 | UL/DL = 1, PPDU Type = 0 |
| EHT SU PPDU | 单用户传输 | PPDU Type = 1 |
| EHT Sounding NDP | 信道探测 | PPDU Type = 1, EHT-SIG MCS = 0 |

### 5.2 U-SIG 字段

**U-SIG-1 (26 bits):**
- PHY Version Identifier (3 bits): EHT = 0
- Bandwidth (3 bits): 0=20M, 1=40M, 2=80M, 3=160M, 4=320M-1, 5=320M-2
- UL/DL (1 bit)
- BSS Color (6 bits)
- TXOP (7 bits)

**U-SIG-2 (26 bits):**
- PPDU Type And Compression (2 bits)
- Punctured Channel Info (5 bits)
- EHT-SIG MCS (2 bits)
- EHT-SIG Symbols (3 bits)
- CRC (4 bits)
- Tail (6 bits)

### 5.3 MRU (Multiple Resource Unit)

WiFi 7 引入 MRU 概念，允许组合相邻 RU：

| MRU 类型 | 适用场景 |
|----------|----------|
| 52+26-tone | 20 MHz 内 |
| 106+26-tone | 20 MHz 内 |
| 484+242-tone | 80 MHz 打孔 |
| 996+484-tone | 160 MHz 打孔 |
| 3×996-tone | 320 MHz 80M打孔 |
| 4×996-tone | 320 MHz 全带宽 |

---

## 六、同步技术

### 6.1 包检测方法

| 方法 | 原理 | 优点 | 缺点 |
|------|------|------|------|
| 能量检测法 | 检测能量是否超过阈值 | 简单、快速 | 对噪声敏感 |
| 自相关检测法 | 利用STF周期性 | 对功率变化不敏感 | 计算复杂度较高 |
| 双滑动窗口法 | 结合能量和自相关 | 可同时估计信号功率 | - |

### 6.2 同步流程

```
接收信号 → 能量检测 → 阈值判断 → 初步检测
              ↓
          自相关检测 → 周期确认 → 最终检测
                            ↓
                       触发同步流程
```

### 6.3 频偏估计

**STF 粗估计:**
```
φ_est = angle(Σ r[n]·r*[n-D])
Δf_est = φ_est / (2π·D·T_s)
```

**LTF 精估计:**
```
φ_est = angle(Σ LTF1[n]·LTF2*[n])
精度：子载波间隔的 1/16 到 1/32
```

---

## 七、OFDM 调制

### 7.1 FFT 参数

| 带宽 | FFT点数 | 有效子载波 | 保护子载波 | 子载波间隔 |
|------|---------|-----------|-----------|-----------|
| 20MHz | 64 | 52 | 12 | 312.5kHz |
| 40MHz | 128 | 114 | 14 | 312.5kHz |
| 80MHz | 256 | 242 | 14 | 312.5kHz |
| 160MHz | 512 | 484 | 28 | 312.5kHz |

### 7.2 子载波分配 (20MHz)

```
索引:  -32 ... -7  -6 -5 ... -1  0  1 ... 5  6  7 ... 31
        │    │    └───┴──┴────┘  └──┴────┴──┘  │    │
        │    │         保护(11)    DC(1)       │    │
        │    └─ 数据子载波(26) ─────────────────┘    │
        └──────────────────────────────────────────┘
```

### 7.3 循环前缀 (CP)

| 模式 | CP长度 | 占比 | 用途 |
|------|--------|------|------|
| 标准 | 0.8µs | 1/4 | 室内 |
| 短CP | 0.4µs | 1/8 | 低时延 |
| 长CP | 1.6µs | 1/2 | 室外 |

---

## 八、信道估计与均衡

### 8.1 LS 信道估计

```
Ĥ_LS[k] = Y[k] / X[k] = H[k] + N[k]/X[k]
```

### 8.2 均衡方法

| 方法 | 公式 | 优点 | 缺点 |
|------|------|------|------|
| ZF | X̂[k] = Y[k] / Ĥ[k] | 完全消除信道影响 | 放大噪声 |
| MMSE | X̂[k] = Ĥ*[k] / (\|Ĥ[k]\|² + σ²/σ_x²) | 避免噪声过度放大 | 需要噪声方差 |

---

## 九、MIMO 技术

### 9.1 空间复用原理

```
信号模型：y = H·x + n

MIMO信道容量：
C = max log₂(det(I + SNR·H·H^H))
≈ min(N,M)·log₂(SNR)  (高SNR)
```

### 9.2 信道探测流程

```
AP (Beamformer)                    STA (Beamformee)
      │                                   │
      │─────── NDP Announcement ──────────→│
      │                                   │
      │←────────── NDP -------------------│
      │                                   │
      │←───── Compressed Beamforming ─────│
      │       Report                      │
```

---

## 十、项目规格

### 10.1 PHY/MAC 规格参数

| 参数 | 规格 |
|------|------|
| 最大带宽 | 160 MHz |
| STA 最大天线数 | 2 |
| AP 最大天线数 | 8 |
| AP 最大并发用户数 | 16 |
| 最大空间流（AP TX） | 8 |
| 最大空间流（AP RX） | 8 |

### 10.2 PPDU 格式支持

| PPDU 格式 | 支持状态 |
|-----------|----------|
| HE SU PPDU | ✅ |
| HE MU PPDU | ✅ |
| HE ER SU PPDU | ✅ |
| HE TB PPDU | ✅ |
| EHT MU PPDU | ✅ |
| EHT TB PPDU | ✅ |

---

## 十一、验证关键点

### 11.1 前导码验证

| 检查项 | 验证方法 | 预期结果 |
|--------|----------|----------|
| L-STF 检测 | 自相关 | 0.8 µs 周期峰值 |
| L-LTF 同步 | 互相关 | 精确定时 |
| HE-SIG-A CRC | CRC-4 校验 | 通过 |
| HE-SIG-A Tail | 全零检测 | 6 bits 全零 |

### 11.2 RU 分配验证

| RU类型 | 数据子载波范围 | 导频位置 |
|--------|---------------|----------|
| 26-tone (RU1, 20MHz) | -122 ~ -107 | -112, -116 |
| 52-tone (RU3, 20MHz) | -103 ~ -52 | -102, -90, -78, -66 |

### 11.3 MU-MIMO 验证

| 测试项 | 测试配置 | 通过标准 |
|--------|----------|----------|
| DL MU-MIMO 最大流 | 4 用户，各 2 SS | 8 SS 总计，正确分离 |
| UL MU-MIMO 最大流 | 4 用户，各 2 SS | 8 SS 总计，AP 正确接收 |
| HE-LTF 正交性 | P 矩阵验证 | P×P^T = NHE-LTF × I |

---

## 参考文档

1. IEEE P802.11ax/D8.0 - WiFi 6 标准（820 页）
2. IEEE P802.11be/D3.0 - WiFi 7 标准（999 页）
3. WIFI7-PHY.pdf - WiFi 7 PHY 层专题

---

*文档来源：飞书云空间学习笔记*
*整理时间：2026-04-03*
