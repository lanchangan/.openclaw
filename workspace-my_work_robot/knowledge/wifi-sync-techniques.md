# WiFi 同步技术详解

> 芯片验证工程师参考 | 时域同步与定时

---

## 一、包检测

### 1.1 包检测的重要性

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

### 1.2 能量检测法

```python
# 原理：检测接收信号能量是否超过阈值
E[n] = Σ|r[k]|²  (k从n-L+1到n)

# 判决：
# E[n] > η → 检测到包
# E[n] ≤ η → 无信号

# 优点：简单、快速
# 缺点：对噪声敏感，需自适应阈值
```

### 1.3 自相关检测法

```python
# 利用STF的周期性
C[n] = Σ r[m]·r*[m-D]
# 其中 D = STF周期 (16 samples @20MHz)

# 判决度量
M[n] = |C[n]|² / Σ|r[m-D]|²

# M[n] > η → 检测到包

# 优点：对功率变化不敏感
# 缺点：计算复杂度较高
```

### 1.4 双滑动窗口法

```python
# 结合能量检测和自相关
# 计算两个窗口的能量
E_A[n] = Σ|r[k]|²  (窗口A: n-L+1 到 n)
E_B[n] = Σ|r[k]|²  (窗口B: n+1 到 n+L)

# 比值
R[n] = E_A[n] / E_B[n]

# 当R[n]突变（信号到达）时检测到包
# 优点：可同时估计信号功率
```

### 1.5 WiFi包检测流程

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

### 1.6 SystemVerilog 实现框架

```systemverilog
module packet_detector #(
    parameter D = 16,           // 延时（STF周期）
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

## 二、符号定时

### 2.1 粗同步 vs 细同步

| 类型 | 方法 | 分辨率 | 精度 |
|------|------|--------|------|
| 粗同步 | STF自相关 | 一个STF周期 | ±8 samples |
| 细同步 | LTF互相关 | 一个采样点 | ±1 sample |

**同步精度要求：**
- 定时误差 < CP长度（通常）
- 误差过大导致ISI和ICI

### 2.2 最佳采样点

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

### 2.3 LTF互相关同步

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

### 2.4 定时偏差分析

```
误差 ε (samples) → 相位旋转

Y[k] = H[k]·X[k]·exp(j·2π·k·ε/N)

其中 N = FFT点数

影响分析：
- 低频子载波：相位旋转小
- 高频子载波：相位旋转大
- 可通过信道均衡补偿

误差超出CP：
- 产生ISI（符号间干扰）
- 产生ICI（载波间干扰）
- 性能严重下降
```

---

## 三、载波频偏估计

### 3.1 频偏来源

| 来源 | 说明 |
|------|------|
| 本振频差 | 发射机和接收机晶振不一致 |
| 多普勒频移 | 移动场景 |
| 相位噪声 | 本振不理想 |

**典型值：**
- 晶振精度：±20ppm
- 5GHz载波：±100kHz频偏
- 要求：< 子载波间隔的 1-2%

### 3.2 STF-based 粗估计

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

# 精度：子载波间隔的 1/2
```

### 3.3 LTF-based 精估计

```python
# LTF包含两个相同的长训练符号
# 频偏估计
φ_est = angle(Σ LTF1[n]·LTF2*[n])

# 精度：子载波间隔的 1/16 到 1/32
```

### 3.4 频偏补偿

```python
def cfo_compensate(rx_signal, cfo, fs=20e6):
    """频偏补偿"""
    t = np.arange(len(rx_signal)) / fs
    compensation = np.exp(-1j * 2 * np.pi * cfo * t)
    return rx_signal * compensation
```

### 3.5 频偏影响分析

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
│                                                     │
│  示例（WiFi 20MHz）：                               │
│  - 子载波间隔：312.5kHz                             │
│  - 允许频偏：< 6.25kHz (2%)                         │
│  - 10kHz频偏 → SNR损失约 1.4dB                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 四、采样频偏 (SFO)

### 4.1 SFO 来源

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

### 4.2 SFO 的影响

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

### 4.3 SFO 估计方法

```
方法1：导频相位跟踪
- 比较连续符号中导频相位变化
- 估计SFO

方法2：循环前缀相关
- 比较CP和数据的相关性
- 追踪采样漂移

估计公式：
δ_est = Δφ / (2π·k·N_sym)
```

### 4.4 SFO vs CFO 对比

| 特性 | CFO | SFO |
|------|-----|-----|
| 来源 | 载波频率偏差 | 采样频率偏差 |
| 相位旋转 | 线性累积 | 与子载波相关 |
| ICI | 均匀 | 非均匀 |
| 估计方法 | STF/LTF | 导频跟踪 |
| 补偿复杂度 | 低 | 中等 |
| 残余影响 | 小 | 累积性 |

---

## 五、相位噪声

### 5.1 相位噪声来源

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

### 5.2 对 OFDM 的影响

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

### 5.3 不同调制方式的相位噪声要求

| 调制方式 | EVM要求 | 相位噪声要求 |
|----------|---------|--------------|
| QPSK | < 17% | 宽松 |
| 16QAM | < 12% | 中等 |
| 64QAM | < 8% | 严格 |
| 256QAM | < 4% | 很严格 |
| 1024QAM | < 2% | 极严格 |

---

## 六、完整同步流程

### 6.1 同步状态机

```
检测状态机：
IDLE → ENERGY_DETECT → CORR_CONFIRM → DETECTED
```

### 6.2 完整同步链路

```python
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

## 七、验证要点

### 7.1 包检测验证

| 检查项 | 验证方法 | 预期结果 |
|--------|----------|----------|
| 最小检测功率测试 | 逐渐降低功率 | 找到检测阈值 |
| 虚警概率测试 | 无信号时检测 | 虚警率 < 0.1% |
| 检测延迟测试 | 测量检测时间 | < 4 µs |
| 多包连续检测 | 连续发送多包 | 100% 检测率 |

### 7.2 频偏估计验证

| 检查项 | 验证方法 | 预期结果 |
|--------|----------|----------|
| 频偏范围测试 | ±100kHz 扫描 | 全范围正确估计 |
| 频偏估计精度 | 固定频偏测试 | 误差 < 1% |
| 残余频偏影响 | 补偿后解调 | PER 满足要求 |

### 7.3 SVA 断言示例

```systemverilog
// 包检测后必须在规定时间内完成频偏估计
property cfo_est_after_detect;
    @(posedge clk) packet_detected |-> ##[1:100] cfo_estimated;
endproperty
assert property (cfo_est_after_detect)
    else $error("CFO estimation timeout after packet detection");

// 频偏估计值范围检查
property cfo_range_check;
    @(posedge clk) cfo_estimated |-> (cfo_value >= -100000 && cfo_value <= 100000);
endproperty
assert property (cfo_range_check)
    else $error("CFO estimate out of range");

// 同步完成后才能开始数据解调
property sync_before_data;
    @(posedge clk) data_demod_start |-> sync_complete;
endproperty
assert property (sync_before_data)
    else $error("Data demod started before sync complete");
```

---

*文档来源：飞书云空间学习笔记*
*整理时间：2026-04-03*
