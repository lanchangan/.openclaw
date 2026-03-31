# MU-MIMO 与 Preamble Puncturing

> 多用户 MIMO 与前导码打孔技术

---

## 一句话总结

> **802.11be 引入 Non-OFDMA Preamble Puncturing，使 MU-MIMO 场景支持打孔传输，提高了频谱利用效率。**

---

## Preamble Puncturing 基础

### 什么是 Preamble Puncturing？

```
正常传输：
| 20MHz | 20MHz | 20MHz | 20MHz |  全带宽传输

Puncture 传输：
| 20MHz |  XX   | 20MHz | 20MHz |  打掉一个 20MHz 子信道
         ↑
      不发 preamble 和 data
```

### 目的

- 避免干扰其他系统（如雷达）
- 利用被占用的频段边缘资源
- 提高频谱利用率

---

## 协议支持情况

### 802.11ax (WiFi 6)

| 场景 | 是否支持 Puncture |
|------|------------------|
| **OFDMA MU** | ✅ 支持 |
| **MU-MIMO (non-OFDMA)** | ❌ 不支持 |
| **SU** | ❌ 不支持 |

### 802.11be (WiFi 7)

| 场景 | 是否支持 Puncture |
|------|------------------|
| **OFDMA MU** | ✅ 支持 |
| **MU-MIMO (non-OFDMA)** | ✅ **支持** |
| **SU** | ✅ 支持 |

> 🎯 **重大变化**：802.11be 引入 **Non-OFDMA Preamble Puncturing**

---

## Non-OFDMA Preamble Puncturing

### 支持的 MRU 组合

在 non-OFDMA 模式（包括 MU-MIMO）下：

| 带宽 | 可 Puncture 后形成的 MRU |
|------|------------------------|
| 80 MHz | 484+242-tone MRU |
| 160 MHz | 996+484+242-tone MRU, 996+484-tone MRU |
| 320 MHz | 3x996+484-tone MRU, 2x996+484-tone MRU 等 |

### 示例：320MHz MU-MIMO + Puncture

```
完整 320MHz：| 80MHz | 80MHz | 80MHz | 80MHz |

Puncture 第3个 40MHz：
| 80MHz | 80MHz |  XX   | 80MHz |
                   ↑
              打掉的 40MHz

形成 3x996+484-tone MRU
可在该 MRU 上进行 MU-MIMO 传输
```

---

## 协议细节

### U-SIG 字段

EHT MU 包的 U-SIG 字段携带 punctured sub-channel indication：

```
U-SIG 字段：
├── BW (带宽)
├── Punctured Channel Field (打孔指示)
└── 其他字段
```

### Puncture Pattern 编码

| 带宽 | PuncturedChannelFieldValue | 打孔位置 |
|------|---------------------------|---------|
| 160 MHz | 2 | 第2个 20MHz |
| 160 MHz | 4 | 第4个 20MHz |
| 320 MHz | 3 | 第3个 40MHz |

---

## 与验证工作的关联

### 验证关注点

| 验证项 | 说明 |
|--------|------|
| **U-SIG 解析** | 正确解析 Punctured Channel Indication 字段 |
| **EHT-SIG 解析** | 正确处理 puncture 后的 RU 分配 |
| **频谱映射** | puncture 的子信道不发 preamble 和 data |
| **MU-MIMO + Puncture** | 多用户在同一 MRU 上，puncture 不影响空间流分配 |
| **UL/DL** | UL TB transmission 也要支持 puncture pattern |

### 测试场景

1. **基本功能**：不同带宽、不同打孔位置
2. **MU-MIMO 组合**：
   - 不同用户数（2/4/8 用户）
   - 不同空间流分配
   - 不同 MCS
3. **边界条件**：
   - 连续打多个子信道
   - 极端带宽组合
4. **UL/DL 对称性**：上行下行行为一致

### 波形验证

```matlab
% MATLAB 示例：320MHz MU-MIMO + Puncture
cfg = wlanEHTMUConfig('CBW320', 'NumUsers', 2, ...
                       'PuncturedChannelFieldValue', 3);
cfg.User{1}.NumSpaceTimeStreams = 4;
cfg.User{2}.NumSpaceTimeStreams = 4;

% 生成波形并观察频谱
tx = wlanWaveformGenerator(psdu, cfg);
```

---

## 快速参考

| 协议 | MU-MIMO + Puncture |
|------|-------------------|
| 802.11ax | ❌ 不支持（只支持 OFDMA 场景） |
| 802.11be | ✅ 支持（Non-OFDMA Preamble Puncturing） |

---

## 参考资料

- IEEE 802.11be Draft 5.0, Section 36.3.12
- [MathWorks: 802.11be Waveform Generation](https://www.mathworks.com/help/wlan/ug/802-11be-waveform-generation.html)
- [Rohde & Schwarz: IEEE 802.11be Whitepaper](https://www.rohde-schwarz.com/)
