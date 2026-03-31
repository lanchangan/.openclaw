# WiFi PHY 学习 - 第一阶段：时域基础

## Week 1-2：信号与系统基础

---

### Day 1: 时域信号基础

#### 核心概念

**1. 信号的分类**

| 分类维度 | 类型 | 说明 | WiFi中的应用 |
|---------|------|------|-------------|
| 确定性 | 确定性信号 | 可用数学函数精确描述 | 导频子载波、训练序列 |
| | 随机信号 | 只能用统计特性描述 | 信道噪声、干扰 |
| 周期性 | 周期信号 | 重复出现，周期T | STF（短训练序列） |
| | 非周期信号 | 不重复 | 数据符号 |
| 能量/功率 | 能量信号 | 有限能量，零平均功率 | 脉冲信号 |
| | 功率信号 | 无限能量，有限平均功率 | 周期信号、通信信号 |

**2. 周期信号的数学描述**

```
x(t) = x(t + nT), n ∈ Z

周期 T = 1/f₀
角频率 ω₀ = 2πf₀
```

**3. 能量信号与功率信号**

```
能量信号：E = ∫|x(t)|² dt < ∞
功率信号：P = lim(T→∞) [1/T ∫|x(t)|² dt] < ∞

WiFi信号特性：
- 有限时长 → 能量有限
- 持续传输 → 功率有限
```

**4. 确定性信号 vs 随机信号**

```
确定性信号示例：
- 正弦波：x(t) = A·sin(2πft + φ)
- 方波：周期性高低电平
- 脉冲：短时存在的信号

随机信号示例：
- 高斯白噪声：n(t) ~ N(0, σ²)
- 热噪声：电子随机运动产生
- 散粒噪声：载流子随机产生/复合
```

#### WiFi中的信号类型

```
┌─────────────────────────────────────────┐
│            WiFi PHY 信号结构             │
├─────────────────────────────────────────┤
│  L-STF  │ 确定性周期信号 │ 10个重复周期  │
│  L-LTF  │ 确定性信号     │ 信道估计用    │
│  L-SIG  │ 确定性信号     │ 控制信息      │
│  Data   │ 随机性数据     │ 承载信息      │
│  Noise  │ 随机信号       │ 干扰/噪声     │
└─────────────────────────────────────────┘
```

#### 实践要点

**验证工程师视角：**
- 时域信号可通过示波器/逻辑分析仪观测
- 周期性信号用于同步检测（自相关）
- 随机性用于测试误码率

**仿真代码示例（Python）：**
```python
import numpy as np
import matplotlib.pyplot as plt

# 周期信号示例
fs = 100e6  # 采样率 100MHz
t = np.arange(0, 1e-6, 1/fs)  # 1微秒
f0 = 10e6  # 10MHz
x_periodic = np.sin(2*np.pi*f0*t)

# 能量计算
energy = np.sum(np.abs(x_periodic)**2) / fs
print(f"信号能量: {energy:.6f} J·s")
```

---

### Day 2: 线性系统响应

#### 核心概念

**1. 线性时不变系统（LTI）**

```
线性特性：
若 x₁(t) → y₁(t), x₂(t) → y₂(t)
则 a·x₁(t) + b·x₂(t) → a·y₁(t) + b·y₂(t)

时不变特性：
若 x(t) → y(t)
则 x(t-τ) → y(t-τ)
```

**2. 冲激响应 h(t)**

```
定义：系统对单位冲激函数 δ(t) 的响应

δ(t) → h(t)

物理意义：
- h(t) 完全表征LTI系统
- 包含系统所有频率响应信息
```

**3. 卷积运算**

```
y(t) = x(t) * h(t) = ∫x(τ)·h(t-τ)dτ

性质：
- 交换律：x*h = h*x
- 结合律：(x*h₁)*h₂ = x*(h₁*h₂)
- 分配律：x*(h₁+h₂) = x*h₁ + x*h₂

离散形式：
y[n] = Σ x[k]·h[n-k]
```

**4. 因果性与稳定性**

```
因果系统：
h(t) = 0, ∀ t < 0
物理可实现系统的必要条件

稳定系统：
∫|h(t)|dt < ∞
有界输入产生有界输出（BIBO）
```

#### WiFi系统中的线性系统

```
┌────────────────────────────────────────────┐
│          WiFi 信道模型                      │
├────────────────────────────────────────────┤
│                                            │
│  发送信号 x(t) ──→ 信道 h(t) ──→ 接收信号 y(t)│
│                    ↓                       │
│                噪声 n(t)                    │
│                                            │
│  y(t) = x(t) * h(t) + n(t)                 │
│                                            │
└────────────────────────────────────────────┘

信道冲激响应 h(t) 特性：
- 多径时延扩展
- 衰落特性
- 相位失真
```

#### 卷积的物理解释

```
输入信号通过系统：
1. 将输入信号分解为无数个冲激
2. 每个冲激产生对应的冲激响应
3. 将所有响应叠加得到输出

┌─────────────────────────────────────────┐
│  卷积过程示意                            │
├─────────────────────────────────────────┤
│                                         │
│  输入：    ┌───┐                         │
│           │   │  脉冲                    │
│  ─────────┘   ┴─────                    │
│                                         │
│  冲激响应：  ∿∿∿                         │
│             衰减振荡                     │
│                                         │
│  输出：      ∿∿∿                         │
│           输入与h(t)的卷积               │
│                                         │
└─────────────────────────────────────────┘
```

#### 实践要点

**验证工程师视角：**
- 系统因果性：检查输出是否超前于输入
- 系统稳定性：注入大信号观察输出是否发散
- 冲激响应测试：发送窄脉冲观测系统特性

**仿真代码示例：**
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# 定义系统冲激响应（低通滤波器）
t = np.linspace(0, 1, 100)
h = np.exp(-t/0.1) * np.sin(2*np.pi*5*t)  # 衰减振荡

# 输入信号
x = np.zeros(100)
x[10] = 1  # 单位冲激

# 卷积
y = np.convolve(x, h)[:100]

plt.figure(figsize=(10, 4))
plt.subplot(131), plt.plot(x), plt.title('Input')
plt.subplot(132), plt.plot(h), plt.title('h(t)')
plt.subplot(133), plt.plot(y), plt.title('Output')
plt.tight_layout()
```

---

### Day 3: 相关函数

#### 核心概念

**1. 自相关函数**

```
定义：
Rₓₓ(τ) = ∫x(t)·x*(t-τ)dt

性质：
- Rₓₓ(0) = E[|x(t)|²] = 信号功率
- Rₓₓ(τ) = Rₓₓ*(-τ)  共轭对称
- |Rₓₓ(τ)| ≤ Rₓₓ(0)   最大值在τ=0
- 周期信号的自相关仍为周期信号

物理意义：
- 信号与自身时移版本的相似度
- 在时延τ处匹配程度的度量
```

**2. 互相关函数**

```
定义：
Rₓᵧ(τ) = ∫x(t)·y*(t-τ)dt

应用：
- 信号检测
- 时延估计
- 同步
```

**3. 匹配滤波器**

```
原理：
当滤波器冲激响应 h(t) = s(T-t) 时
输出SNR最大

匹配滤波器输出 = 输入信号的自相关

应用：
- 已知信号的检测
- 雷达、通信中的信号检测
```

#### WiFi中的相关应用

```
┌────────────────────────────────────────────────────┐
│            WiFi 包检测与同步                        │
├────────────────────────────────────────────────────┤
│                                                    │
│  自相关检测：                                       │
│  C(n) = Σ r(n+k)·r*(n+k-D)                        │
│                                                    │
│  其中 D = STF周期 = 16 samples (20MHz)             │
│                                                    │
│  ┌────────────────────────────────────────┐        │
│  │ 接收信号 ──→ 延时D ──→ × ──→ 累加 ──→ C(n)│     │
│  │              ↑                          │       │
│  │              └──── 共轭 ────┘           │       │
│  └────────────────────────────────────────┘        │
│                                                    │
│  判决：|C(n)| > 阈值 → 检测到包                     │
│                                                    │
└────────────────────────────────────────────────────┘
```

**STF自相关特性：**

```
L-STF 结构：10个重复的短训练符号
每个符号：16 samples (0.8μs @20MHz)

自相关输出：
- 在STF期间，|C(n)| 出现峰值平台
- 可用于：
  1. 包检测
  2. 粗定时同步
  3. AGC调整
```

#### 实践要点

**验证工程师视角：**
- 自相关峰值位置对应周期信号的周期
- 峰值宽度与时延扩展相关
- 信噪比影响相关峰的清晰度

**仿真代码示例：**
```python
import numpy as np
import matplotlib.pyplot as plt

# 生成STF类似的周期信号
N = 16  # 周期
stf_period = np.exp(1j * 2 * np.pi * np.arange(N) * 5 / N)
stf = np.tile(stf_period, 10)  # 10个周期

# 添加噪声
noise = 0.1 * (np.random.randn(len(stf)) + 1j*np.random.randn(len(stf)))
r = stf + noise

# 自相关
D = N  # 延时 = 周期
autocorr = np.zeros(len(r)-D, dtype=complex)
for n in range(len(r)-D):
    autocorr[n] = np.sum(r[n:n+D] * np.conj(r[n+D:n+2*D]))

# 检测峰值
plt.figure(figsize=(10, 3))
plt.plot(np.abs(autocorr))
plt.xlabel('Sample index')
plt.ylabel('|Autocorrelation|')
plt.title('STF Autocorrelation for Packet Detection')
plt.axhline(y=0.7*np.max(np.abs(autocorr)), color='r', linestyle='--')
plt.show()
```

---

### Day 4: 噪声模型

#### 核心概念

**1. 高斯白噪声（AWGN）**

```
定义：
- 概率密度：p(x) = (1/√(2πσ²))·exp(-x²/2σ²)
- 功率谱密度：常数 N₀/2
- 自相关：R(τ) = N₀/2·δ(τ)

特性：
- 均值：μ = 0
- 方差：σ² = 噪声功率
- 不同时刻的噪声独立
```

**2. 信噪比（SNR）**

```
定义：
SNR = 信号功率 / 噪声功率
SNR_dB = 10·log₁₀(P_signal/P_noise)

E_b/N₀（比特能量信噪比）：
- 数字通信常用指标
- E_b = 每比特能量
- N₀ = 噪声功率谱密度

关系：
SNR = (E_b/N₀)·(R/B)
其中 R = 比特率，B = 带宽
```

**3. 噪声功率谱密度**

```
N₀ = k·T·NF

其中：
- k = 1.38×10⁻²³ J/K (玻尔兹曼常数)
- T = 绝对温度(K)
- NF = 噪声系数

室温 T=290K 时：
N₀ ≈ -174 dBm/Hz
```

#### WiFi中的噪声模型

```
┌────────────────────────────────────────────────┐
│          WiFi 接收机噪声模型                    │
├────────────────────────────────────────────────┤
│                                                │
│  天线 ──→ LNA ──→ 混频 ──→ 滤波 ──→ ADC ──→ 解调│
│          │       │       │       │            │
│          ↓       ↓       ↓       ↓            │
│        热噪声  相位噪声  量化噪声  采样噪声     │
│                                                │
│  主要噪声源：                                   │
│  1. 热噪声：kTB（无法避免）                     │
│  2. 接收机噪声系数：NF = SNR_in/SNR_out        │
│  3. 相位噪声：本振不理想                        │
│  4. 量化噪声：ADC有限位数                        │
│                                                │
└────────────────────────────────────────────────┘
```

**WiFi接收机灵敏度计算：**

```
灵敏度 = N₀ + NF + SNR_min + 10log(B)

以WiFi 6为例：
- 带宽 B = 20MHz
- NF = 6dB（典型值）
- SNR_min = 按调制方式不同

MCS0 (BPSK 1/2): SNR ≈ 2dB, 灵敏度 ≈ -82dBm
MCS7 (64QAM 5/6): SNR ≈ 25dB, 灵敏度 ≈ -59dBm
MCS11 (1024QAM 5/6): SNR ≈ 35dB, 灵敏度 ≈ -49dBm
```

#### 实践要点

**验证工程师视角：**

```
SystemVerilog 噪声建模：

// 高斯噪声生成（Box-Muller变换）
function real gaussian_noise(real mean, real std);
    real u1, u2, z;
    u1 = $urandom_range(1, 10000) / 10000.0;
    u2 = $urandom_range(1, 10000) / 10000.0;
    z = $sqrt(-2.0 * $ln(u1)) * $cos(2.0 * 3.14159 * u2);
    return mean + std * z;
endfunction

// SNR计算
function real calculate_snr(real signal_power, real noise_power);
    return 10.0 * $log10(signal_power / noise_power);
endfunction
```

**仿真代码示例：**
```python
import numpy as np
import matplotlib.pyplot as plt

def add_awgn(signal, snr_db):
    """添加AWGN噪声"""
    signal_power = np.mean(np.abs(signal)**2)
    snr_linear = 10**(snr_db/10)
    noise_power = signal_power / snr_linear
    noise = np.sqrt(noise_power/2) * (np.random.randn(len(signal)) + 
                                        1j*np.random.randn(len(signal)))
    return signal + noise

# 测试
t = np.linspace(0, 1, 1000)
signal = np.exp(1j*2*np.pi*10*t)
noisy = add_awgn(signal, 20)  # 20dB SNR

plt.figure(figsize=(10, 3))
plt.subplot(121)
plt.psd(signal, Fs=100, label='Original')
plt.psd(noisy, Fs=100, label='With AWGN')
plt.legend()
plt.subplot(122)
plt.scatter(noisy.real, noisy.imag, s=1)
plt.axis('equal')
plt.show()
```

---

### Day 5: 带限信号

#### 核心概念

**1. 带限信号定义**

```
带限信号：频谱在有限频带内非零

X(f) = 0, |f| > B

B = 信号带宽

WiFi信号带宽：
- 20MHz, 40MHz, 80MHz, 160MHz
- 带限特性由发射滤波器保证
```

**2. 采样定理（Nyquist定理）**

```
采样定理：
带限信号最高频率 f_max
采样率 f_s ≥ 2·f_max 时
可无失真恢复原信号

f_s,min = 2·f_max （Nyquist率）

欠采样（f_s < 2f_max）：
- 频谱混叠
- 无法恢复原信号
```

**3. 带通采样**

```
对于带通信号（f_L ~ f_H）：
不必按 2f_H 采样

带通采样定理：
f_s ≥ 2B（B = f_H - f_L）
且满足：f_s = 4f_c/(2n-1)

其中 f_c = (f_L + f_H)/2，n为正整数
```

#### WiFi信号的带宽限制

```
┌────────────────────────────────────────────────────┐
│            WiFi 信道带宽与采样                      │
├────────────────────────────────────────────────────┤
│                                                    │
│  带宽配置：                                         │
│  ┌─────────┬────────┬──────────┬──────────┐        │
│  │ 带宽    │ 采样率 │ FFT点数  │ 有效子载波│        │
│  ├─────────┼────────┼──────────┼──────────┤        │
│  │ 20MHz   │ 20MHz  │ 64       │ 52       │        │
│  │ 40MHz   │ 40MHz  │ 128      │ 114      │        │
│  │ 80MHz   │ 80MHz  │ 256      │ 242      │        │
│  │ 160MHz  │ 160MHz │ 512      │ 484      │        │
│  └─────────┴────────┴──────────┴──────────┘        │
│                                                    │
│  频谱模板要求：                                     │
│  - 带内平坦度：< ±2dB                               │
│  - 带外抑制：> 20dB @±11MHz (20MHz模式)            │
│                                                    │
└────────────────────────────────────────────────────┘
```

**WiFi发射频谱：**

```
         │
    0dB ─┼───────────────────────
         │        ┌───────┐
         │        │       │
         │        │  有效  │
   -20dB ─┼────────│ 带宽  │────────
         │        │       │
         │        └───────┘
         │
         └──────┴───────┴──────┴─────→ f
              -B      0      B

保护带：防止邻道干扰
```

#### 实践要点

**验证工程师视角：**
- 检查发射信号是否满足频谱模板
- 验证采样时钟精度
- 测试混叠抑制能力

**仿真代码示例：**
```python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# WiFi 20MHz 信号
fs = 20e6  # 采样率
N_fft = 64
N_used = 52

# 生成OFDM符号（频域）
X = np.zeros(N_fft, dtype=complex)
X[1:27] = np.random.randn(26) + 1j*np.random.randn(26)  # 数据子载波
X[-26:] = np.conj(X[1:27][::-1])  # 共轭对称（实数IFFT）

# IFFT
x = np.fft.ifft(X) * np.sqrt(N_fft)

# 升余弦窗（带限）
window = signal.windows.cosine(len(x))
x_windowed = x * window

# 频谱分析
plt.figure(figsize=(10, 3))
plt.subplot(121)
plt.plot(np.abs(x_windowed))
plt.title('Time Domain')
plt.subplot(122)
plt.psd(x_windowed, Fs=fs, NFFT=512)
plt.title('Frequency Domain')
plt.axvline(10e6, color='r', linestyle='--', label='Band edge')
plt.axvline(-10e6, color='r', linestyle='--')
plt.legend()
plt.tight_layout()
```

---

### Day 6-7: 复习与实践

#### 本周知识点回顾

```
┌────────────────────────────────────────────────────┐
│          Week 1-2 核心知识点                        │
├────────────────────────────────────────────────────┤
│                                                    │
│  1. 时域信号基础                                    │
│     ✓ 信号分类：确定性/随机、周期/非周期            │
│     ✓ 能量信号 vs 功率信号                         │
│     ✓ WiFi信号特性分析                             │
│                                                    │
│  2. 线性系统响应                                    │
│     ✓ LTI系统特性                                  │
│     ✓ 冲激响应与卷积                               │
│     ✓ 因果性与稳定性                               │
│                                                    │
│  3. 相关函数                                       │
│     ✓ 自相关与互相关                               │
│     ✓ 匹配滤波器                                   │
│     ✓ WiFi包检测原理                               │
│                                                    │
│  4. 噪声模型                                       │
│     ✓ AWGN特性                                     │
│     ✓ SNR与E_b/N₀                                  │
│     ✓ 接收机灵敏度计算                             │
│                                                    │
│  5. 带限信号                                       │
│     ✓ Nyquist采样定理                              │
│     ✓ WiFi带宽配置                                 │
│     ✓ 频谱模板要求                                 │
│                                                    │
└────────────────────────────────────────────────────┘
```

#### 实践项目：时域仿真平台

搭建一个基础的时域仿真平台，包含以下模块：

```python
# wifi_phy_sim.py - 时域仿真平台框架

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

class WiFiTimeDomainSimulator:
    """WiFi时域仿真平台"""
    
    def __init__(self, bandwidth_mhz=20):
        self.bandwidth = bandwidth_mhz * 1e6
        self.fs = self.bandwidth  # 采样率 = 带宽
        self.fft_size = {20: 64, 40: 128, 80: 256, 160: 512}[bandwidth_mhz]
        
    def generate_stf(self) -> np.ndarray:
        """生成短训练序列"""
        # STF: 10个重复的短符号
        stf_period = np.array([1, -1, 1, -1, 1, -1, 1, -1,
                               1, -1, 1, -1, 1, -1, 1, -1])
        return np.tile(stf_period, 10)
    
    def add_awgn(self, signal: np.ndarray, snr_db: float) -> np.ndarray:
        """添加AWGN噪声"""
        signal_power = np.mean(np.abs(signal)**2)
        snr_linear = 10**(snr_db/10)
        noise_power = signal_power / snr_linear
        noise = np.sqrt(noise_power/2) * (np.random.randn(len(signal)) + 
                                            1j*np.random.randn(len(signal)))
        return signal + noise
    
    def packet_detection(self, signal: np.ndarray, threshold: float) -> Tuple[int, float]:
        """包检测（自相关方法）"""
        D = 16  # STF周期
        autocorr = np.abs(np.array([
            np.sum(signal[n:n+D] * np.conj(signal[n+D:n+2*D]))
            for n in range(len(signal)-2*D)
        ]))
        
        detect_idx = np.where(autocorr > threshold * np.max(autocorr))[0]
        if len(detect_idx) > 0:
            return detect_idx[0], autocorr[detect_idx[0]]
        return -1, 0
    
    def calculate_snr(self, signal: np.ndarray, noisy: np.ndarray) -> float:
        """计算实际SNR"""
        signal_power = np.mean(np.abs(signal)**2)
        noise_power = np.mean(np.abs(noisy - signal)**2)
        return 10 * np.log10(signal_power / noise_power)

# 使用示例
if __name__ == "__main__":
    sim = WiFiTimeDomainSimulator(bandwidth_mhz=20)
    
    # 生成信号
    stf = sim.generate_stf()
    
    # 添加噪声
    noisy_stf = sim.add_awgn(stf, snr_db=10)
    
    # 包检测
    idx, peak = sim.packet_detection(noisy_stf, threshold=0.5)
    
    print(f"Packet detected at sample {idx}, peak = {peak:.2f}")
    print(f"Actual SNR: {sim.calculate_snr(stf, noisy_stf):.2f} dB")
```

#### 思考题

1. 为什么WiFi使用周期性的STF而不是单个脉冲进行同步？
2. 卷积运算复杂度如何？有没有快速算法？
3. 如何在SystemVerilog中实现自相关检测？
4. 实际系统中噪声不完全是AWGN，会有什么影响？
5. 如果采样率略低于2B，会发生什么？

---

## Week 3-4：WiFi时域信号结构

### Day 8: PPDU帧结构

#### 核心概念

**1. PPDU（PLCP Protocol Data Unit）**

```
PPDU = PLCP前导码 + PLCP头 + PSDU

层次结构：
┌─────────────────────────────────────────────────────┐
│                      PPDU                           │
├──────────┬──────────┬───────────────────────────────┤
│  Preamble │  SIGNAL  │           DATA                │
│  (前导码) │  (信号)   │         (数据)                │
└──────────┴──────────┴───────────────────────────────┘

不同WiFi标准的PPDU格式：
- Legacy (802.11a/g): L-STF + L-LTF + L-SIG + Data
- HT (802.11n): Legacy + HT-SIG + HT-STF + HT-LTF + Data
- VHT (802.11ac): Legacy + VHT-SIG-A + VHT-STF + VHT-LTF + VHT-SIG-B + Data
- HE (802.11ax): Legacy + RL-SIG + HE-SIG-A + HE-STF + HE-LTF + Data
```

**2. Legacy前导码结构**

```
时间（μs）:
┌──────────────────────────────────────────────────────┐
│  L-STF    │  L-LTF   │  L-SIG   │     Data Symbols   │
│   8μs     │   8μs    │   4μs    │      Variable      │
├───────────┼──────────┼──────────┼────────────────────┤
│  10个短   │  2个长   │ BPSK     │  OFDM符号          │
│  训练符号 │  训练符号 │ OFDM     │  各种调制          │
│           │          │ R=1/2    │                    │
└───────────┴──────────┴──────────┴────────────────────┘

功能：
- L-STF: 包检测、AGC、粗同步
- L-LTF: 精细同步、信道估计
- L-SIG: 速率、长度信息
```

**3. HE (WiFi 6) PPDU结构**

```
┌──────────────────────────────────────────────────────────────────────┐
│                    HE-SU PPDU Structure                              │
├─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┤
│ L-STF   │ L-LTF   │ L-SIG   │ RL-SIG  │HE-SIG-A │ HE-STF  │ HE-LTF  │
│  8μs    │  8μs    │  4μs    │  4μs    │  8μs    │  4μs    │  Var    │
├─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┤
│                           HE-SIG-A                                  │
│  ┌─────────────────────┬─────────────────────┐                      │
│  │     HE-SIG-A1       │     HE-SIG-A2       │                      │
│  │  Format, Beam Change│  TXOP, Coding, LDPC │                      │
│  └─────────────────────┴─────────────────────┘                      │
├─────────────────────────────────────────────────────────────────────┤
│                            Data Symbols                             │
└─────────────────────────────────────────────────────────────────────┘

新增字段：
- RL-SIG: 重复L-SIG，标识HE格式
- HE-SIG-A: HE信号字段，包含HE特有参数
- HE-STF: HE短训练序列，用于MIMO
- HE-LTF: HE长训练序列，用于MIMO信道估计
```

#### 时序图

```
Legacy (802.11a/g) PPDU:

    8μs      8μs     4μs      Variable
├────────┼────────┼────────┼────────────────┤
│        │        │        │                │
│ L-STF  │ L-LTF  │ L-SIG  │    Data        │
│        │        │        │                │
└────────┴────────┴────────┴────────────────┘

HE-SU (WiFi 6) PPDU:

    8μs      8μs     4μs     4μs     8μs     4μs    Var    Var
├────────┼────────┼────────┼────────┼────────┼────────┼──────┼──────┤
│        │        │        │        │        │        │      │      │
│ L-STF  │ L-LTF  │ L-SIG  │ RL-SIG │HE-SIG-A│ HE-STF │HE-LTF│ Data │
│        │        │        │        │        │        │      │      │
└────────┴────────┴────────┴────────┴────────┴────────┴──────┴──────┘
```

#### 实践要点

**验证工程师视角：**

```systemverilog
// PPDU字段检测状态机
typedef enum {
    IDLE,
    STF_DETECT,
    LTF_SYNC,
    SIG_DECODE,
    DATA_RECEIVE
} ppdu_state_e;

module ppdu_receiver (
    input  clk,
    input  rst_n,
    input  complex_t rx_sample,
    output logic packet_detected,
    output logic sig_valid,
    output logic [7:0] rate,
    output logic [15:0] length
);

ppdu_state_e state, next_state;

// 状态转换逻辑
always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) state <= IDLE;
    else state <= next_state;
end

// 状态机逻辑
always_comb begin
    case (state)
        IDLE: begin
            if (packet_detected) next_state = STF_DETECT;
            else next_state = IDLE;
        end
        STF_DETECT: next_state = LTF_SYNC;
        LTF_SYNC: next_state = SIG_DECODE;
        SIG_DECODE: next_state = DATA_RECEIVE;
        DATA_RECEIVE: next_state = IDLE;
        default: next_state = IDLE;
    endcase
end

endmodule
```

---

### Day 9: 短训练序列 (STF)

#### 核心概念

**1. L-STF结构**

```
L-STF: 10个重复的短训练符号
每个符号：16 samples = 0.8μs @20MHz
总时长：10 × 0.8μs = 8μs

频域定义：
- 使用4个子载波（-21, -7, 7, 21）
- 子载波间隔：312.5kHz × 4 = 1.25MHz
- 周期：1/1.25MHz = 0.8μs

时域特性：
x_STF[n] = Σ S[k]·exp(j·2π·k·n/64)
其中 S[k] 非零值在 k = -21, -7, 7, 21
```

**2. 自相关检测原理**

```
STF周期性用于包检测：

┌──────────────────────────────────────────────────┐
│                                                  │
│  接收信号 r[n] ──→ 延时D ──→ 共轭 ──→ × ──→ 累加 │
│                          ↑                       │
│                          └───────────────────────┘
│                                                  │
│  C[n] = Σ r[m]·r*[m-D]  (D=16 samples)          │
│                                                  │
│  |C[n]| 在STF期间形成平台                         │
│  判决：|C[n]| > threshold → 检测到包              │
│                                                  │
└──────────────────────────────────────────────────┘
```

**3. AGC训练**

```
AGC功能：
- 自动调整接收机增益
- 利用STF的8μs进行功率估计
- 防止ADC饱和或量化噪声过大

AGC流程：
1. 检测到能量上升
2. 测量STF期间的平均功率
3. 计算所需增益调整
4. 在L-LTF前完成调整

增益调整范围：
P_rx = P_ref - AGC_gain
其中 P_ref 为目标功率
```

#### WiFi 6 HE-STF增强

```
HE-STF 与 L-STF 的区别：

L-STF:
- 单流
- 4个子载波
- 周期0.8μs

HE-STF:
- 支持多流（MIMO）
- 更高的峰值功率比
- 用于MIMO AGC训练
- 周期可变（4μs或8μs）

不同NSS的HE-STF序列：
NSS=1: 使用L-STF序列
NSS=2: 两流正交序列
NSS>2: 扩展的正交序列
```

#### 实践要点

**自相关检测仿真：**

```python
import numpy as np
import matplotlib.pyplot as plt

def generate_lstf(fs_mhz=20):
    """生成L-STF"""
    n_samples_per_symbol = int(fs_mhz * 0.8)  # 16 @20MHz
    # 简化的STF序列
    stf_symbol = np.exp(1j * 2 * np.pi * np.arange(n_samples_per_symbol) * 0.25)
    stf = np.tile(stf_symbol, 10)
    return stf

def packet_detection_autocorr(rx_signal, threshold_ratio=0.5):
    """基于自相关的包检测"""
    D = 16  # 延时（STF周期）
    
    autocorr = np.zeros(len(rx_signal) - 2*D, dtype=complex)
    energy = np.zeros(len(rx_signal) - 2*D)
    
    for n in range(len(rx_signal) - 2*D):
        autocorr[n] = np.sum(rx_signal[n:n+D] * np.conj(rx_signal[n+D:n+2*D]))
        energy[n] = np.sum(np.abs(rx_signal[n:n+D])**2)
    
    # 归一化自相关
    metric = np.abs(autocorr) / (energy + 1e-10)
    
    # 检测
    threshold = threshold_ratio
    detected = np.where(metric > threshold)[0]
    
    return metric, detected[0] if len(detected) > 0 else -1

# 测试
stf = generate_lstf()
noise = 0.1 * (np.random.randn(len(stf)) + 1j*np.random.randn(len(stf)))
rx = stf + noise

metric, detect_idx = packet_detection_autocorr(rx)
print(f"Packet detected at sample: {detect_idx}")

plt.figure(figsize=(10, 3))
plt.plot(np.abs(rx), label='|rx|')
plt.plot(metric, label='Detection metric')
plt.axvline(detect_idx, color='r', linestyle='--', label='Detection point')
plt.legend()
plt.title('STF Packet Detection')
plt.show()
```

---

（Week 3-4 的 Day 10-14 内容将在下一部分继续）

