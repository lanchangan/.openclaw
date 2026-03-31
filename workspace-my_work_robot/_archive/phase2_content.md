# WiFi PHY 学习 - 第二阶段：同步与定时

## Week 5-6：时域同步技术

---

### Day 15: 包检测

#### 核心概念

**1. 包检测的重要性**

```
包检测是接收机第一道工序：
- 判断是否有信号到达
- 触发后续同步流程
- 启动AGC调整

挑战：
- 未知到达时间
- 未知信号功率
- 噪声中检测信号
```

**2. 能量检测法**

```
原理：检测接收信号能量是否超过阈值

E[n] = Σ|r[k]|²  (k从n-L+1到n)

判决：
- E[n] > η → 检测到包
- E[n] ≤ η → 无信号

优点：简单、快速
缺点：对噪声敏感，需自适应阈值
```

**3. 自相关检测法**

```
利用STF的周期性：

C[n] = Σ r[m]·r*[m-D]

其中 D = STF周期 (16 samples @20MHz)

判决度量：
M[n] = |C[n]|² / Σ|r[m-D]|²  (k从n-L+1到n)

M[n] > η → 检测到包

优点：对功率变化不敏感
缺点：计算复杂度较高
```

**4. 双滑动窗口法**

```
结合能量检测和自相关：

计算两个窗口的能量：
E_A[n] = Σ|r[k]|²  (窗口A: n-L+1 到 n)
E_B[n] = Σ|r[k]|²  (窗口B: n+1 到 n+L)

比值：
R[n] = E_A[n] / E_B[n]

当R[n]突变（信号到达）时检测到包

优点：可同时估计信号功率
```

#### WiFi包检测实现

```
┌──────────────────────────────────────────────────────┐
│           WiFi 包检测流程                             │
├──────────────────────────────────────────────────────┤
│                                                      │
│  接收信号 ──→ 能量检测 ──→ 阈值判断 ──→ 初步检测      │
│                │                                     │
│                ↓                                     │
│            自相关检测 ──→ 周期确认 ──→ 最终检测       │
│                                    │                 │
│                                    ↓                 │
│                              触发同步流程            │
│                                                      │
│  检测状态机：                                         │
│  IDLE → ENERGY_DETECT → CORR_CONFIRM → DETECTED      │
│                                                      │
└──────────────────────────────────────────────────────┘
```

#### 实践要点

**SystemVerilog实现框架：**

```systemverilog
module packet_detector #(
    parameter D = 16,           // 延时（STF周期）
    parameter L = 32,           // 相关长度
    parameter THRESHOLD = 0.5   // 检测阈值
)(
    input  clk,
    input  rst_n,
    input  complex_t rx_sample,
    output logic packet_detected,
    output logic [15:0] corr_value
);

    // 延时线
    complex_t delay_line [0:D-1];
    integer i;
    
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < D; i++) delay_line[i] <= 0;
        end else begin
            delay_line[0] <= rx_sample;
            for (i = 1; i < D; i++) delay_line[i] <= delay_line[i-1];
        end
    end
    
    // 自相关计算
    complex_t corr_sum;
    always_ff @(posedge clk) begin
        corr_sum = 0;
        for (i = 0; i < L; i++) begin
            corr_sum += rx_sample * conj(delay_line[D-1]);
        end
        corr_value <= |corr_sum;
    end
    
    // 阈值判决
    always_ff @(posedge clk) begin
        packet_detected <= (corr_value > THRESHOLD * 65535);
    end

endmodule
```

---

### Day 16: 符号定时

#### 核心概念

**1. 粗同步 vs 细同步**

```
粗同步：
- 基于STF自相关
- 分辨率：一个STF周期
- 精度：±8 samples

细同步：
- 基于LTF互相关
- 分辨率：一个采样点
- 精度：±1 sample

同步精度要求：
- 定时误差 < CP长度（通常）
- 误差过大导致ISI和ICI
```

**2. 最佳采样点**

```
OFDM符号结构：
┌─────────────────────────────────────┐
│  CP  │        Symbol Data           │
│  Tg  │           Tu                 │
└──────┴──────────────────────────────┘

最佳采样点：
- 在CP和数据交界处
- 避开多径干扰区域
- 通常在CP末尾

定时偏差影响：
- 早采：使用下一符号的CP，可能ISI
- 晚采：丢失本符号数据，产生ICI
```

**3. LTF互相关同步**

```
LTF结构：2个相同的长训练符号

互相关：
R[n] = Σ r[m]·LTF*[m-n]

LTF已知，可作为参考信号

峰值位置 = 最佳定时点

精度：采样级
```

#### 定时偏差分析

```
┌─────────────────────────────────────────────────────┐
│          定时偏差对系统的影响                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  误差 ε (samples) → 相位旋转                        │
│                                                     │
│  Y[k] = H[k]·X[k]·exp(j·2π·k·ε/N)                  │
│                                                     │
│  其中 N = FFT点数                                   │
│                                                     │
│  影响分析：                                          │
│  - 低频子载波：相位旋转小                            │
│  - 高频子载波：相位旋转大                            │
│  - 可通过信道均衡补偿                               │
│                                                     │
│  误差超出CP：                                        │
│  - 产生ISI（符号间干扰）                            │
│  - 产生ICI（载波间干扰）                            │
│  - 性能严重下降                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

#### 实践要点

**定时同步算法：**

```python
def fine_timing_sync(rx_signal, ltf_ref):
    """基于LTF互相关的精细定时同步"""
    # 互相关
    corr = np.correlate(rx_signal, ltf_ref, mode='same')
    
    # 找峰值
    peak_idx = np.argmax(np.abs(corr))
    
    # 细化峰值位置（抛物线插值）
    if peak_idx > 0 and peak_idx < len(corr) - 1:
        alpha = np.abs(corr[peak_idx - 1])
        beta = np.abs(corr[peak_idx])
        gamma = np.abs(corr[peak_idx + 1])
        
        fine_offset = 0.5 * (alpha - gamma) / (alpha - 2*beta + gamma)
        precise_idx = peak_idx + fine_offset
    else:
        precise_idx = peak_idx
    
    return int(round(precise_idx)), corr
```

---

### Day 17: 载波频偏估计

#### 核心概念

**1. 载波频偏来源**

```
频偏来源：
1. 本振频差：发射机和接收机晶振不一致
2. 多普勒频移：移动场景
3. 相位噪声：本振不理想

典型值：
- 晶振精度：±20ppm
- 5GHz载波：±100kHz频偏
- 要求：< 子载波间隔的 1-2%
```

**2. STF-based粗估计**

```
利用STF的周期性：

频偏引起的相位旋转：
φ = 2π·Δf·D·T_s

其中：
- Δf = 频偏
- D = STF周期
- T_s = 采样周期

估计方法：
φ_est = angle(Σ r[n]·r*[n-D])

Δf_est = φ_est / (2π·D·T_s)

精度：子载波间隔的 1/2
```

**3. LTF-based精估计**

```
LTF包含两个相同的长训练符号

频偏估计：
φ_est = angle(Σ LTF1[n]·LTF2*[n])

其中 LTF1 和 LTF2 是两个长训练符号

精度：子载波间隔的 1/16 到 1/32
```

**4. 频偏补偿**

```
时域补偿：
r_comp[n] = r[n]·exp(-j·2π·Δf_est·n·T_s)

频域补偿（残余频偏）：
Y_comp[k] = Y[k]·exp(-j·φ_residual[k])

导频辅助：
利用导频子载波跟踪残余频偏
```

#### 频偏影响分析

```
┌─────────────────────────────────────────────────────┐
│          载波频偏对OFDM的影响                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  大频偏（>> 子载波间隔）：                           │
│  - 载波位置偏移                                      │
│  - 信号落入错误的子载波                             │
│  - 解调完全失败                                     │
│                                                     │
│  小频偏（< 子载波间隔）：                            │
│  - ICI（载波间干扰）                                │
│  - 信噪比损失：                                     │
│    SNR_loss ≈ (π·Δf·T_u)²/3                        │
│    其中 T_u = OFDM符号时长                          │
│                                                     │
│  示例（WiFi 20MHz）：                               │
│  - 子载波间隔：312.5kHz                             │
│  - 允许频偏：< 6.25kHz (2%)                         │
│  - 10kHz频偏 → SNR损失约 1.4dB                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

#### 实践要点

**频偏估计与补偿代码：**

```python
def cfo_estimate_stf(rx_signal, D=16):
    """基于STF的粗频偏估计"""
    # 自相关
    corr = np.sum(rx_signal[D:] * np.conj(rx_signal[:-D]))
    
    # 相位
    phase = np.angle(corr)
    
    # 频偏
    cfo = phase / (2 * np.pi * D)
    
    return cfo

def cfo_compensate(rx_signal, cfo, fs=20e6):
    """频偏补偿"""
    t = np.arange(len(rx_signal)) / fs
    compensation = np.exp(-1j * 2 * np.pi * cfo * t)
    return rx_signal * compensation

# 完整流程
cfo_coarse = cfo_estimate_stf(rx_stf)
rx_compensated = cfo_compensate(rx_signal, cfo_coarse * fs)
```

---

### Day 18: 采样频偏

#### 核心概念

**1. SFO来源**

```
采样频偏来源：
- ADC和DAC时钟源不同
- 时钟漂移

SFO定义：
δ = (f_s,tx - f_s,rx) / f_s,tx

典型值：
- 晶振精度：±20ppm
- 两侧累计误差：±40ppm
```

**2. SFO的影响**

```
时域影响：
- 符号边界漂移
- 每符号累积采样误差

频域影响：
- 子载波相位旋转
- ICI增加

累积效应：
每个OFDM符号：
- 相位旋转：Δφ = 2π·k·δ
- 位置偏移：Δn = N·δ

N个符号后：
- 累积偏移：N·N_sym·δ
- 可能超出CP
```

**3. SFO估计方法**

```
方法1：导频相位跟踪
- 比较连续符号中导频相位变化
- 估计SFO

方法2：循环前缀相关
- 比较CP和数据的相关性
- 追踪采样漂移

估计公式：
δ_est = Δφ / (2π·k·N_sym)

其中：
- Δφ = 导频相位变化
- k = 导频子载波索引
- N_sym = 符号间采样数
```

**4. SFO补偿**

```
时域补偿：
- 重采样
- 插值/抽取

频域补偿：
- 相位旋转补偿
- 每个符号按比例修正

补偿流程：
1. 估计SFO
2. 计算累积相位误差
3. 在频域进行相位补偿
4. 周期性重置
```

#### SFO vs CFO对比

```
┌─────────────────────────────────────────────────────┐
│          CFO 与 SFO 对比                             │
├────────────────────┬────────────────┬───────────────┤
│      特性          │     CFO        │     SFO       │
├────────────────────┼────────────────┼───────────────┤
│  来源              │ 载波频率偏差   │ 采样频率偏差  │
│  相位旋转          │ 线性累积       │ 与子载波相关  │
│  ICI               │ 均匀           │ 非均匀        │
│  估计方法          │ STF/LTF        │ 导频跟踪      │
│  补偿复杂度        │ 低             │ 中等          │
│  残余影响          │ 小             │ 累积性        │
└────────────────────┴────────────────┴───────────────┘
```

---

### Day 19: 相位噪声

#### 核心概念

**1. 相位噪声来源**

```
相位噪声：本振信号的随机相位波动

理想本振：V(t) = A·cos(2πf_c·t)
实际本振：V(t) = A·cos(2πf_c·t + φ(t))

φ(t) = 相位噪声

来源：
- 振荡器热噪声
- 闪烁噪声
- 电源噪声
```

**2. 相位噪声模型**

```
相位噪声功率谱密度：

L(f) = 相位噪声功率 / 载波功率 (dBc/Hz)

典型值（锁相环输出）：
- 1kHz offset: -80 dBc/Hz
- 10kHz offset: -90 dBc/Hz
- 1MHz offset: -120 dBc/Hz

相位噪声类型：
1. 白相位噪声：平坦频谱
2. 闪烁噪声：1/f 特性
3. 随机游走：1/f² 特性
```

**3. 对OFDM的影响**

```
公共相位误差（CPE）：
- 所有子载波相同的相位旋转
- 可通过导频估计和补偿

载波间干扰（ICI）：
- 相邻子载波的干扰
- 类似频偏效果
- 难以完全补偿

影响程度：
SNR_loss ≈ (π·β·T_u)²

其中 β = 相位噪声带宽
```

**4. 相位噪声跟踪**

```
相位噪声跟踪环路：

┌─────────────────────────────────────────────────┐
│                                                 │
│  接收符号 ──→ 导频提取 ──→ 相位估计 ──→ 滤波   │
│                                │               │
│                                ↓               │
│  补偿后符号 ←── 相位补偿 ←────┘               │
│                                                 │
└─────────────────────────────────────────────────┘

环路参数：
- 环路带宽：权衡噪声抑制和跟踪速度
- 典型值：10kHz - 100kHz
```

#### EVM影响

```
┌─────────────────────────────────────────────────────┐
│          相位噪声对EVM的影响                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  EVM_pn ≈ √(2·∫L(f)·|H_θ(f)|² df)                  │
│                                                     │
│  其中 H_θ(f) 为相位跟踪环路传递函数                 │
│                                                     │
│  不同调制方式的要求：                               │
│  ┌──────────┬──────────┬───────────────┐           │
│  │ 调制方式 │ EVM要求  │ 相位噪声要求  │           │
│  ├──────────┼──────────┼───────────────┤           │
│  │ QPSK     │ < 17%    │ 宽松          │           │
│  │ 16QAM    │ < 12%    │ 中等          │           │
│  │ 64QAM    │ < 8%     │ 严格          │           │
│  │ 256QAM   │ < 4%     │ 很严格        │           │
│  │ 1024QAM  │ < 2%     │ 极严格        │           │
│  └──────────┴──────────┴───────────────┘           │
│                                                     │
│  WiFi 6 (1024QAM) 对相位噪声要求最高               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### Day 20-21: 复习与实践

#### 本周知识点回顾

```
┌────────────────────────────────────────────────────┐
│          Week 5-6 核心知识点                        │
├────────────────────────────────────────────────────┤
│                                                    │
│  1. 包检测                                         │
│     ✓ 能量检测、自相关检测                         │
│     ✓ 双滑动窗口法                                 │
│     ✓ 检测状态机设计                               │
│                                                    │
│  2. 符号定时                                       │
│     ✓ 粗同步与细同步                               │
│     ✓ 最佳采样点确定                               │
│     ✓ LTF互相关同步                                │
│                                                    │
│  3. 载波频偏估计                                   │
│     ✓ STF粗估计、LTF精估计                         │
│     ✓ 频偏对OFDM的影响                             │
│     ✓ 频偏补偿方法                                 │
│                                                    │
│  4. 采样频偏                                       │
│     ✓ SFO来源与影响                                │
│     ✓ SFO估计与补偿                                │
│     ✓ SFO vs CFO对比                               │
│                                                    │
│  5. 相位噪声                                       │
│     ✓ 相位噪声模型                                 │
│     ✓ 对OFDM的影响（CPE、ICI）                     │
│     ✓ 相位噪声跟踪                                 │
│                                                    │
└────────────────────────────────────────────────────┘
```

#### 综合同步仿真

```python
# complete_sync_chain.py - 完整同步链路仿真

import numpy as np
import matplotlib.pyplot as plt

class WiFiSynchronizer:
    """WiFi同步器"""
    
    def __init__(self, fs=20e6):
        self.fs = fs
        self.stf_period = 16  # samples
        
    def packet_detect(self, rx, threshold=0.5):
        """包检测"""
        D = self.stf_period
        L = 32
        
        metric = np.zeros(len(rx) - D - L)
        for n in range(len(metric)):
            num = np.abs(np.sum(rx[n:n+L] * np.conj(rx[n+D:n+D+L])))
            den = np.sum(np.abs(rx[n:n+L])**2) + 1e-10
            metric[n] = num / den
        
        detect_idx = np.where(metric > threshold)[0]
        return detect_idx[0] if len(detect_idx) > 0 else -1
    
    def cfo_estimate(self, rx, start_idx):
        """频偏估计"""
        stf = rx[start_idx:start_idx + 160]  # 10个STF周期
        D = self.stf_period
        
        # 使用多个周期平均
        phases = []
        for i in range(9):
            corr = np.sum(stf[i*D:(i+1)*D] * np.conj(stf[(i+1)*D:(i+2)*D]))
            phases.append(np.angle(corr))
        
        phase = np.mean(phases)
        cfo = phase / (2 * np.pi * D / self.fs)
        
        return cfo
    
    def cfo_compensate(self, rx, cfo):
        """频偏补偿"""
        t = np.arange(len(rx)) / self.fs
        return rx * np.exp(-1j * 2 * np.pi * cfo * t)
    
    def fine_timing(self, rx, ltf_ref, search_start, search_range):
        """精细定时"""
        search_region = rx[search_start:search_start+search_range]
        corr = np.abs(np.correlate(search_region, ltf_ref, mode='valid'))
        fine_offset = search_start + np.argmax(corr)
        return fine_offset
    
    def full_sync(self, rx, ltf_ref):
        """完整同步流程"""
        # 1. 包检测
        detect_idx = self.packet_detect(rx)
        print(f"Packet detected at sample {detect_idx}")
        
        if detect_idx < 0:
            return None
        
        # 2. 粗频偏估计
        cfo = self.cfo_estimate(rx, detect_idx)
        print(f"CFO estimated: {cfo:.2f} Hz")
        
        # 3. 频偏补偿
        rx_comp = self.cfo_compensate(rx, cfo)
        
        # 4. 精细定时
        fine_idx = self.fine_timing(rx_comp, ltf_ref, detect_idx + 160, 64)
        print(f"Fine timing at sample {fine_idx}")
        
        return {
            'detect_idx': detect_idx,
            'cfo': cfo,
            'fine_timing': fine_idx,
            'rx_compensated': rx_comp
        }
```

---

## Week 7：同步验证方法论

### Day 22: 同步测试向量

#### 测试向量设计原则

```
同步测试向量分类：

1. 正常场景
   - 标准信号功率
   - 标准SNR范围
   - 理想同步条件

2. 边界条件
   - 最小可检测功率
   - 最大频偏范围
   - 最小/最大定时偏差

3. 异常场景
   - 极低SNR
   - 超大频偏
   - 多包冲突
   - 脉冲干扰

4. 回归测试
   - 历史bug复现
   - 边缘case覆盖
```

#### 关键测试点

```
┌─────────────────────────────────────────────────────┐
│          同步模块测试清单                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  包检测：                                           │
│  □ 最小检测功率测试                                 │
│  □ 虚警概率测试（无信号时）                         │
│  □ 检测延迟测试                                     │
│  □ 多包连续检测                                     │
│                                                     │
│  频偏估计：                                         │
│  □ 频偏范围测试（±100kHz）                          │
│  □ 频偏估计精度测试                                 │
│  □ 残余频偏影响测试                                 │
│                                                     │
│  定时同步：                                         │
│  □ 定时精度测试                                     │
│  □ 多径信道定时测试                                 │
│  □ 符号边界跟踪测试                                 │
│                                                     │
│  相位跟踪：                                         │
│  □ 相位噪声容限测试                                 │
│  □ 跟踪速度测试                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### Day 23: 时序检查

#### SVA断言应用

```systemverilog
// 同步模块断言示例

// 1. 包检测后必须在规定时间内完成频偏估计
property cfo_est_after_detect;
    @(posedge clk) packet_detected |-> ##[1:100] cfo_estimated;
endproperty
assert property (cfo_est_after_detect)
    else $error("CFO estimation timeout after packet detection");

// 2. 频偏估计值范围检查
property cfo_range_check;
    @(posedge clk) cfo_estimated |-> (cfo_value >= -100000 && cfo_value <= 100000);
endproperty
assert property (cfo_range_check)
    else $error("CFO estimate out of range");

// 3. 精细定时必须在粗定时后
property fine_after_coarse;
    @(posedge clk) coarse_timing_done |-> ##[1:200] fine_timing_done;
endproperty
assert property (fine_after_coarse)
    else $error("Fine timing not done after coarse timing");

// 4. 同步完成后才能开始数据解调
property sync_before_data;
    @(posedge clk) data_demod_start |-> sync_complete;
endproperty
assert property (sync_before_data)
    else $error("Data demod started before sync complete");

// 5. 状态机覆盖断言
cover property (@(posedge clk) state == IDLE);
cover property (@(posedge clk) state == STF_DETECT);
cover property (@(posedge clk) state == CFO_EST);
cover property (@(posedge clk) state == FINE_TIMING);
cover property (@(posedge clk) state == SYNC_COMPLETE);
```

---

### Day 24: 覆盖率分析

#### 功能点覆盖

```systemverilog
// 功能覆盖组定义

covergroup sync_metrics @(posedge clk);
    // 频偏估计覆盖
    cfo_estimate: coverpoint cfo_value {
        bins small_neg = {[-100000:-10000]};
        bins small_pos = {[10000:100000]};
        bins medium_neg = {[-100000:-50000]};
        bins medium_pos = {[50000:100000]};
        bins large_neg = {[-100000:-90000]};
        bins large_pos = {[90000:100000]};
    }
    
    // 定时偏差覆盖
    timing_offset: coverpoint timing_error {
        bins early = {[-16:-1]};
        bins perfect = {0};
        bins late = {[1:16]};
    }
    
    // SNR覆盖
    snr_level: coverpoint snr_db {
        bins low = {[0:10]};
        bins medium = {[10:20]};
        bins high = {[20:40]};
    }
    
    // 交叉覆盖
    cross cfo_estimate, snr_level;
    cross timing_offset, snr_level;
endcovergroup

// 实例化
sync_metrics sync_cov = new();
```

#### 覆盖率目标

```
┌─────────────────────────────────────────────────────┐
│          同步模块覆盖率目标                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  代码覆盖率：                                       │
│  - 行覆盖率：> 95%                                  │
│  - 分支覆盖率：> 90%                                │
│  - 条件覆盖率：> 85%                                │
│  - FSM覆盖率：100%                                  │
│                                                     │
│  功能覆盖率：                                       │
│  - 频偏范围：100%                                   │
│  - 定时偏差：100%                                   │
│  - SNR范围：100%                                    │
│  - 交叉覆盖：> 80%                                  │
│                                                     │
│  验证计划完成度：> 95%                              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 本阶段总结

### 关键要点

1. **包检测**是接收机的第一步，需要快速可靠
2. **同步精度**直接影响解调性能
3. **频偏和采样频偏**都需要估计和补偿
4. **相位噪声**对高阶调制影响大
5. **验证方法论**确保同步模块可靠性

### 与验证工作的联系

- 同步模块是验证重点之一
- 需要大量边界条件测试
- SVA断言可有效检查时序
- 覆盖率分析确保测试完整性

