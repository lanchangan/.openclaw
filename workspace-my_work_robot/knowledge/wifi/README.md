# WiFi 知识库

> WiFi 协议学习笔记，从基础到进阶

---

## 📚 知识索引

### 一、协议标准

| 协议 | 文件 | 关键词 |
|------|------|--------|
| WiFi 6 (802.11ax) | [80211ax_protocol.md](./80211ax_protocol.md) | OFDMA, MU-MIMO, 1024-QAM |
| WiFi 7 (802.11be) | [80211be_protocol.md](./80211be_protocol.md) | 320MHz, 4096-QAM, MRU, MLO |

### 二、PHY 基础

| 主题 | 文件 | 关键词 |
|------|------|--------|
| PHY 物理层基础 | [phy_basics.md](./phy_basics.md) | WiFi 代际, MCS, 帧结构, OFDMA |
| 调制基础 | [modulation_basics.md](./modulation_basics.md) | AM/FM/PM, ASK/FSK/PSK, QAM |
| 学习计划 | [learning_plan.md](./learning_plan.md) | WiFi PHY 学习路线图 |
| AGC 笔记 | [agc_notes.md](./agc_notes.md) | 自动增益控制 |

### 三、调制与编码

| 主题 | 文件 | 关键词 |
|------|------|--------|
| DCM 双载波调制 | [dcm.md](./dcm.md) | Dual Carrier Modulation, MCS 15, 频率分集 |
| CORDIC 算法 | [cordic.md](./cordic.md) | 相位旋转, 迭代逼近, EVM |

### 四、多天线技术

| 主题 | 文件 | 关键词 |
|------|------|--------|
| MU-MIMO + Puncture | [mu_mimo_puncture.md](./mu_mimo_puncture.md) | 802.11be, preamble puncturing, MRU |

### 五、协议演进

| 协议 | 代号 | 主要特性 |
|------|------|---------|
| 802.11n | WiFi 4 | MIMO, 40MHz |
| 802.11ac | WiFi 5 | MU-MIMO, 160MHz, 256-QAM |
| 802.11ax | WiFi 6/6E | OFDMA, MU-MIMO, 1024-QAM |
| 802.11be | WiFi 7 | 320MHz, 4096-QAM, MRU, Multi-Link |

---

## 🎯 学习路径

```
基础 → 协议 → 验证

1. 调制基础 → 理解 BPSK/QPSK/QAM
2. OFDM 原理 → 理解子载波、RU、MRU
3. MIMO 技术 → 理解空间复用、波束成形
4. 协议细节 → 理解帧结构、信令、流程
5. 验证实战 → 理解测试点、覆盖场景
```

---

## 📖 参考资料

- **IEEE 802.11 标准文档**: 802.11ax D8.0, 802.11be D3.0
- **原始提取内容**: `../protocols_raw/` 目录
- [MathWorks WiFi 文档](https://www.mathworks.com/help/wlan/)
- [Rohde & Schwarz WiFi 白皮书](https://www.rohde-schwarz.com/)

---

## 🔄 更新记录

| 日期 | 新增/更新内容 |
|------|-------------|
| 2026-04-01 | 添加 802.11ax/802.11be 协议详解 |
| 2026-03-30 | 创建知识库，整理调制基础、DCM、CORDIC、MU-MIMO+Puncture |
