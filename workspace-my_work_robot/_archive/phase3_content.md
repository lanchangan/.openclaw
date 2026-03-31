# WiFi PHY 学习 - 第三阶段：频域基础

## Week 8-9：FFT与OFDM原理

---

### Day 25: DFT/FFT原理

#### 核心概念

**1. 离散傅里叶变换（DFT）**

```
DFT定义：
X[k] = Σ x[n]·exp(-j·2π·k·n/N), k = 0,1,...,N-1

IDFT定义：
x[n] = (1/N)·Σ X[k]·exp(j·2π·k·n/N), n = 0,1,...,N-1

物理意义：
- DFT：时域 → 频域
- IDFT：频域 → 时域
- N个采样点对应N个频率分量
```

**2. FFT算法**

```
FFT = Fast Fourier Transform（快速傅里叶变换）

DFT复杂度：O(N²)
FFT复杂度：O(N·log₂N)

基-2 FFT要求：N = 2^m

蝶形运算：
┌────────────────────────────────┐
│    a ────┬────→ a + W·b       │
│          │                     │
│    b ────┼────→ a - W·b       │
│          │                     │
│          W = 旋转因子          │
└────────────────────────────────┘

旋转因子：
W_N^k = exp(-j·2π·k/N)
```

**3. FFT结构**

```
64点FFT结构（WiFi 20MHz）：

Stage 1: 32个蝶形运算，跨度=1
Stage 2: 16个蝶形运算，跨度=2
Stage 3: 8个蝶形运算，跨度=4
...
Stage 6: 1个蝶形运算，跨度=32

每级：
- N/2次蝶形运算
- 位反转排序
- 原位计算

总运算量：
- 复数乘法：(N/2)·log₂N
- 复数加法：N·log₂N
```

#### WiFi FFT参数

```
┌─────────────────────────────────────────────────────┐
│          WiFi 不同带宽的FFT参数                      │
├─────────┬────────┬──────────┬──────────┬───────────┤
│ 带宽    │ FFT点数 │ 有效子载波│ 保护子载波│ 子载波间隔│
├─────────┼────────┼──────────┼──────────┼───────────┤
│ 20MHz   │ 64     │ 52       │ 12       │ 312.5kHz  │
│ 40MHz   │ 128    │ 114      │ 14       │ 312.5kHz  │
│ 80MHz   │ 256    │ 242      │ 14       │ 312.5kHz  │
│ 160MHz  │ 512    │ 484      │ 28       │ 312.5kHz  │
└─────────┴────────┴──────────┴──────────┴───────────┘

关键特性：
- 子载波间隔固定为312.5kHz
- FFT点数与带宽成正比
- 有效子载波用于数据和导频
- 保护子载波用于频谱成形
```

#### 实践要点

**蝶形运算实现：**

```verilog
// 蝶形运算单元
module butterfly #(
    parameter DATA_WIDTH = 16
)(
    input  clk,
    input  rst_n,
    input  signed [DATA_WIDTH-1:0] a_re, a_im,
    input  signed [DATA_WIDTH-1:0] b_re, b_im,
    input  signed [DATA_WIDTH-1:0] w_re, w_im,
    output signed [DATA_WIDTH-1:0] y_re, y_im,
    output signed [DATA_WIDTH-1:0] z_re, z_im
);

    // W·b (复数乘法)
    wire signed [2*DATA_WIDTH-1:0] wb_re = (w_re * b_re - w_im * b_im) >>> (DATA_WIDTH-1);
    wire signed [2*DATA_WIDTH-1:0] wb_im = (w_re * b_im + w_im * b_re) >>> (DATA_WIDTH-1);
    
    // 蝶形输出
    assign y_re = a_re + wb_re;
    assign y_im = a_im + wb_im;
    assign z_re = a_re - wb_re;
    assign z_im = a_im - wb_im;

endmodule
```

---

### Day 26: OFDM调制

#### 核心概念

**1. OFDM原理**

```
OFDM = Orthogonal Frequency Division Multiplexing

核心思想：
- 将宽带信道划分为多个窄带子信道
- 子载波相互正交，无需保护频带
- 并行传输，降低符号率

正交性：
∫exp(j·2π·k·t/T)·exp(-j·2π·m·t/T)dt = 0, k≠m

频率关系：
f_k = f_0 + k·Δf

正交条件：
Δf = 1/T_symbol
```

**2. 子载波映射**

```
WiFi子载波分配（20MHz, 64点FFT）：

索引:  -32 ... -7  -6 -5 ... -1  0  1 ... 5  6  7 ... 31
        │    │    │   │  │    │  │  │    │  │  │    │
        │    │    └───┴──┴────┘  └──┴────┴──┘  │    │
        │    │         保护子载波(11)    DC(1)  │    │
        │    └─ 数据子载波(26) ────────────────┘    │
        └──────────────────────────────────────────┘

详细分配：
- DC子载波：k=0，设为0（避免直流偏移）
- 数据子载波：k=[-26:-1, 1:26]，共52个
- 导频子载波：k=[-21, -7, 7, 21]，4个
- 保护子载波：k=[-32:-27, 27:31]，共11个
```

**3. IDFT实现OFDM**

```
OFDM调制流程：

数据比特 ──→ 调制映射 ──→ 子载波映射 ──→ IDFT ──→ 加CP ──→ 时域OFDM符号

步骤：
1. 将数据映射到星座点（BPSK/QPSK/QAM）
2. 分配到子载波位置
3. 插入导频
4. IDFT变换到时域
5. 添加循环前缀

数学表示：
x[n] = (1/N)·Σ X[k]·exp(j·2π·k·n/N)

其中 X[k] 为子载波k上的调制符号
```

#### WiFi OFDM符号结构

```
┌───────────────────────────────────────────────────────────┐
│            WiFi OFDM 符号结构                              │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  时域：                                                    │
│  ┌─────────┬──────────────────────────────────────┐       │
│  │   CP    │            Symbol Data               │       │
│  │  16 samples    64 samples              │       │
│  └─────────┴──────────────────────────────────────┘       │
│     ←────────── OFDM符号 (80 samples) ──────────→         │
│                                                           │
│  符号时长：                                                 │
│  - T_symbol = 3.2μs (数据部分)                             │
│  - T_cp = 0.8μs 或 0.4μs (保护间隔)                        │
│  - T_total = T_symbol + T_cp                              │
│                                                           │
│  频域（64点FFT）：                                          │
│  ┌────────────────────────────────────────────────┐       │
│  │保护│  数据+导频  │DC│   数据+导频   │保护│       │
│  │ -32 ... -27│-26...-1│0│ 1...26 │27...31│       │
│  └────────────────────────────────────────────────┘       │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

### Day 27: 循环前缀

#### 核心概念

**1. CP的作用**

```
循环前缀（CP = Cyclic Prefix）：

定义：将OFDM符号末尾部分复制到开头

作用：
1. 抵抗多径时延扩展
2. 保持子载波正交性
3. 简化均衡器设计

原理：
在多径信道下，前一符号的延迟会干扰当前符号（ISI）
CP作为保护间隔，吸收多径时延
```

**2. CP长度设计**

```
CP长度选择原则：
T_cp ≥ 最大时延扩展

WiFi CP配置：
┌─────────────────────────────────────────┐
│ 模式      │ CP长度  │ 占比   │ 用途     │
├───────────┼─────────┼────────┼──────────┤
│ 标准      │ 0.8μs   │ 1/4    │ 室内     │
│ 短CP     │ 0.4μs   │ 1/8    │ 低时延   │
│ 长CP     │ 1.6μs   │ 1/2    │ 室外     │
└───────────┴─────────┴────────┴──────────┘

时延扩展典型值：
- 室内：50-200ns
- 室外：0.5-10μs
- 工业环境：可能更大
```

**3. CP的数学原理**

```
设信道冲激响应为 h(t)，时延扩展为 τ_max

无CP时：
y(t) = x(t)*h(t)
= x(t-t₁)·h₁ + x(t-t₂)·h₂ + ...

存在ISI：前一符号的延迟分量叠加到当前符号

有CP时：
接收信号在去除CP后：
y'[t] = x'[t]*h[t] (圆周卷积)

圆周卷积在频域：
Y[k] = X[k]·H[k]

这样只需要单抽头均衡器！
```

#### CP与同步的关系

```
┌─────────────────────────────────────────────────────────┐
│            CP 对同步的影响                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  定时同步：                                              │
│  - 定时误差 < CP长度：可正常解调                        │
│  - 定时误差 > CP长度：产生ISI和ICI                      │
│                                                         │
│  CP相关定时：                                            │
│  利用CP与数据末尾的相同特性                              │
│  C[n] = Σ r[m]·r*[m+T_symbol]                          │
│  在CP范围内产生相关峰                                    │
│                                                         │
│  AGC影响：                                               │
│  CP期间功率与数据相同                                    │
│  可用于功率估计                                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### Day 28: 子载波间隔

#### 核心概念

**1. 子载波间隔设计**

```
WiFi子载波间隔：Δf = 312.5 kHz（固定）

推导：
FFT点数 N = 64 (20MHz)
带宽 B = 20MHz
子载波间隔 Δf = B/N = 20MHz/64 = 312.5kHz

OFDM符号时长：
T_symbol = 1/Δf = 3.2μs

为什么选择312.5kHz？
- 足够小以抵抗频率选择性衰落
- 足够大以抵抗多普勒频移
- 满足正交性要求
- 硬件实现友好
```

**2. 不同标准的子载波间隔**

```
┌───────────────────────────────────────────────────────┐
│        不同通信标准的子载波间隔                        │
├───────────────┬─────────────┬────────────┬────────────┤
│ 标准          │ 子载波间隔  │ 符号时长   │ CP长度     │
├───────────────┼─────────────┼────────────┼────────────┤
│ WiFi 6 (20MHz)│ 312.5kHz    │ 3.2μs     │ 0.8/0.4μs  │
│ WiFi 7 (20MHz)│ 78.125kHz   │ 12.8μs    │ 可变       │
│ LTE           │ 15kHz       │ 66.7μs     │ 4.7/16.7μs │
│ 5G NR         │ 15-240kHz   │ 可变       │ 可变       │
└───────────────┴─────────────┴────────────┴────────────┘

WiFi 7 的改变：
- 子载波间隔减小到78.125kHz
- 符号时长增加到12.8μs
- 支持更大的覆盖范围
- 更好的多径抵抗能力
```

**3. 子载波间隔的影响**

```
子载波间隔 vs 性能：

小间隔优点：
- 更高的频谱效率
- 更长的符号时长
- 更好的多径抵抗

小间隔缺点：
- 对频偏更敏感
- 对相位噪声更敏感
- 对多普勒更敏感

大间隔优点：
- 抗频偏和相位噪声能力强
- 支持高速移动场景

大间隔缺点：
- 频谱效率降低
- CP开销相对增大
```

#### WiFi各代对比

```
┌─────────────────────────────────────────────────────────┐
│          WiFi 各代 PHY 特性对比                          │
├──────────────┬────────────┬────────────┬────────────────┤
│ 特性         │ 802.11n    │ 802.11ac   │ 802.11ax       │
├──────────────┼────────────┼────────────┼────────────────┤
│ 最大带宽     │ 40MHz      │ 160MHz     │ 160MHz         │
│ 子载波间隔   │ 312.5kHz   │ 312.5kHz   │ 78.125kHz      │
│ FFT点数(20M) │ 64         │ 64         │ 256            │
│ 有效子载波   │ 56         │ 56         │ 234            │
│ 最高调制     │ 64QAM      │ 256QAM     │ 1024QAM        │
│ 空间流数     │ 4          │ 8          │ 8              │
│ 最高速率     │ 600Mbps    │ 6.9Gbps    │ 9.6Gbps        │
└──────────────┴────────────┴────────────┴────────────────┘
```

---

### Day 29: 导频子载波

#### 核心概念

**1. 导频的作用**

```
导频子载波：已知数据的子载波

主要功能：
1. 相位噪声跟踪
2. 残余频偏补偿
3. 信道跟踪
4. 符号定时验证

导频 vs 数据子载波：
- 导频：位置固定，数值已知
- 数据：位置固定，数值未知
```

**2. WiFi导频图案**

```
WiFi 20MHz导频位置：

索引：  -21    -7     7      21
        │      │      │      │
        ▼      ▼      ▼      ▼
...────●──────●──────●──────●────...
        │      │      │      │
        导频   导频   导频   导频

导频序列（BPSK调制）：
p[n] ∈ {+1, -1}

不同标准：
- 802.11a/g: 4个导频
- 802.11n: 4个导频（20MHz），6个（40MHz）
- 802.11ac: 4个导频（20MHz），6个（40MHz），8个（80MHz+）
- 802.11ax: 更多导频，支持分布式RU
```

**3. 导频辅助估计**

```
相位估计：
利用导频估计公共相位误差（CPE）

φ_est = angle(Y_pilot / X_pilot)

其中：
- Y_pilot = 接收到的导频值
- X_pilot = 已知的导频值

残余频偏估计：
比较连续符号的导频相位变化

Δφ = angle(Y_pilot[n]·conj(Y_pilot[n-1]))
Δf = Δφ / (2π·T_symbol)

信道跟踪：
利用导频跟踪信道变化
适用于慢时变信道
```

#### 导频序列设计

```
┌─────────────────────────────────────────────────────────┐
│          WiFi 导频序列                                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  导频序列（Pilot Sequence）：                            │
│  通过伪随机序列生成，避免周期性干扰                       │
│                                                         │
│  生成多项式：                                            │
│  x⁷ + x⁴ + 1                                            │
│                                                         │
│  初始状态：0x7F                                          │
│                                                         │
│  序列长度：127（循环）                                   │
│                                                         │
│  作用：                                                  │
│  - 平衡正负导频，避免直流偏移                            │
│  - 随机化干扰，提高估计精度                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### Day 30-31: 复习与实践

#### FFT/IFFT实现

```python
import numpy as np
import matplotlib.pyplot as plt

class OFDMModem:
    """OFDM调制解调器"""
    
    def __init__(self, fft_size=64, cp_length=16):
        self.N = fft_size
        self.cp = cp_length
        
        # 子载波分配（WiFi 20MHz）
        self.data_indices = np.concatenate([
            np.arange(-26, -6), np.arange(-5, 0),
            np.arange(1, 6), np.arange(7, 27)
        ])
        self.pilot_indices = np.array([-21, -7, 7, 21])
        self.dc_index = 0
        
    def modulate(self, data_symbols):
        """OFDM调制"""
        # 创建频域符号
        X = np.zeros(self.N, dtype=complex)
        
        # 分配数据
        for i, idx in enumerate(self.data_indices):
            if i < len(data_symbols):
                X[idx % self.N] = data_symbols[i]
        
        # 插入导频
        pilot_values = np.array([1, 1, 1, -1])  # 简化
        for i, idx in enumerate(self.pilot_indices):
            X[idx % self.N] = pilot_values[i]
        
        # IDFT
        x = np.fft.ifft(X) * np.sqrt(self.N)
        
        # 添加CP
        x_cp = np.concatenate([x[-self.cp:], x])
        
        return x_cp, X
    
    def demodulate(self, rx_symbol):
        """OFDM解调"""
        # 去除CP
        x = rx_symbol[self.cp:]
        
        # DFT
        Y = np.fft.fft(x) / np.sqrt(self.N)
        
        # 提取导频相位
        pilot_rx = Y[self.pilot_indices % self.N]
        phase = np.angle(np.mean(pilot_rx / np.array([1, 1, 1, -1])))
        
        # 相位补偿
        Y_comp = Y * np.exp(-1j * phase)
        
        return Y_comp

# 测试
modem = OFDMModem()
data = np.exp(1j * 2 * np.pi * np.random.rand(52))  # 随机数据
tx, X_tx = modem.modulate(data)
rx, Y_rx = modem.demodulate(tx)

plt.figure(figsize=(10, 4))
plt.subplot(121)
plt.stem(np.abs(X_tx))
plt.title('Transmitted Spectrum')
plt.subplot(122)
plt.stem(np.abs(Y_rx))
plt.title('Received Spectrum')
plt.tight_layout()
plt.show()
```

---

## Week 10：信道估计与均衡

### Day 32: 信道模型

#### 核心概念

**1. 多径信道**

```
多径传播：
发射信号通过多条路径到达接收机

路径类型：
- 直射路径（LOS）
- 反射路径
- 折射路径
- 绕射路径

每条路径特性：
- 时延 τ_i
- 衰落 h_i
- 相位 φ_i
```

**2. 信道冲激响应**

```
信道模型：
h(t) = Σ h_i · δ(t - τ_i)

功率延迟谱（PDP）：
描述各径的功率分布

常见模型：
- 指数衰减：P(τ) = P₀·exp(-τ/τ_rms)
- Saleh-Valenzuela：簇模型

时延扩展：
τ_rms = √(Σ|τ_i - τ_mean|²·|h_i|² / Σ|h_i|²)
```

**3. WiFi信道模型**

```
TGn信道模型（802.11n）：

模型分类：
┌────────────────────────────────────────┐
│ 模型 │ 场景         │ 时延扩展 │ 备注  │
├──────┼──────────────┼──────────┼───────┤
│ A    │ 脉冲响应     │ 0ns      │ 测试  │
│ B    │ 住宅         │ 15ns     │ 小范围│
│ C    │ 小办公室     │ 30ns     │ 中等  │
│ D    │ 典型办公室   │ 50ns     │ 常用  │
│ E    │ 大办公室     │ 100ns    │ 大范围│
│ F    │ 大型室内     │ 150ns    │ 工厂等│
└──────┴──────────────┴──────────┴───────┘

TGax信道模型（802.11ax）：
在TGn基础上增加了：
- 室外场景
- 更多路径数
- 更精确的簇结构
```

---

### Day 33: LS信道估计

#### 核心概念

**1. 最小二乘估计**

```
LS信道估计原理：

接收信号：
Y[k] = H[k]·X[k] + N[k]

LS估计：
Ĥ_LS[k] = Y[k] / X[k] = H[k] + N[k]/X[k]

特点：
- 简单直接
- 受噪声影响大
- 仅在导频位置有效
```

**2. LTF-based信道估计**

```
利用LTF进行信道估计：

LTF结构：
- 2个长训练符号（相同）
- 可用于平均降噪

估计过程：
1. 提取两个LTF符号
2. 分别计算信道估计
3. 平均降低噪声

Ĥ[k] = (Y_LTF1[k] + Y_LTF2[k]) / (2·X_LTF[k])

噪声方差估计：
σ² = var(Y_LTF1 - Y_LTF2) / 2
```

**3. 信道插值**

```
LTF仅在某些子载波上有信息

需要插值得到所有子载波的信道估计：

方法：
1. 零填充 + IDFT插值
2. 线性插值
3. 样条插值
4. DFT插值（推荐）

DFT插值：
- 时域加窗抑制噪声
- 零填充后IDFT得到插值
- 利用信道的稀疏性
```

#### 信道估计算法

```python
def ls_channel_estimate(rx_ltf, tx_ltf):
    """LS信道估计"""
    # 简单除法
    H_ls = rx_ltf / tx_ltf
    return H_ls

def dft_interpolate(H_ls, N_full):
    """DFT插值"""
    N_pilot = len(H_ls)
    
    # 时域转换
    h_time = np.fft.ifft(H_ls)
    
    # 零填充
    h_padded = np.zeros(N_full, dtype=complex)
    h_padded[:N_pilot//2] = h_time[:N_pilot//2]
    h_padded[-N_pilot//2:] = h_time[-N_pilot//2:]
    
    # 加窗抑制噪声
    window = np.hamming(N_pilot)
    h_padded[:len(window)//2] *= window[:len(window)//2]
    h_padded[-len(window)//2:] *= window[-len(window)//2:]
    
    # 频域转换
    H_interp = np.fft.fft(h_padded)
    
    return H_interp
```

---

### Day 34: 信道平滑

#### 核心概念

**1. 噪声抑制**

```
LS估计的噪声问题：
Ĥ_LS[k] = H[k] + N[k]/X[k]

噪声方差较大时，估计精度下降

平滑方法：
1. 时域加窗
2. 频域平均
3. MMSE估计
```

**2. MMSE信道估计**

```
最小均方误差估计：

Ĥ_MMSE = R_HH · (R_HH + σ²·I)^(-1) · Ĥ_LS

其中：
- R_HH = 信道相关矩阵
- σ² = 噪声方差

优点：
- 最优估计（MMSE准则）
- 有效抑制噪声

缺点：
- 需要信道统计特性
- 计算复杂度高
```

**3. 简化MMSE**

```
LMMSE（线性MMSE）：
假设信道相关矩阵已知

实际实现：
- 预计算相关矩阵
- 低秩近似
- 对角近似

性能对比：
┌────────────────────────────────────┐
│ 方法     │ 复杂度 │ 性能 │ 备注   │
├──────────┼────────┼──────┼────────┤
│ LS       │ 低     │ 差   │ 基准   │
│ LS+平滑  │ 低     │ 中   │ 实用   │
│ MMSE     │ 高     │ 优   │ 复杂   │
│ LMMSE    │ 中     │ 较优 │ 折中   │
└──────────┴────────┴──────┴────────┘
```

---

### Day 35: 均衡器设计

#### 核心概念

**1. 单抽头均衡器**

```
OFDM的优势：
信道在频域表现为乘性

Y[k] = H[k]·X[k] + N[k]

单抽头均衡：
X̂[k] = Y[k] / H[k]

极其简单！
这是OFDM的核心优势
```

**2. ZF均衡**

```
迫零均衡（Zero-Forcing）：

X̂_ZF[k] = Y[k] / Ĥ[k]

优点：
- 完全消除信道影响
- 实现简单

缺点：
- 放大噪声（H小时）
- 可能导致噪声增强
```

**3. MMSE均衡**

```
最小均方误差均衡：

X̂_MMSE[k] = Ĥ*[k] / (|Ĥ[k]|² + σ²/σ_x²)

其中：
- σ² = 噪声方差
- σ_x² = 信号功率

优点：
- 考虑噪声影响
- 避免噪声过度放大
- 性能优于ZF

SNR增益：
MMSE比ZF有更好的SNR性能
尤其在信道深衰落点
```

#### 均衡器实现

```python
class OFDMEqualizer:
    """OFDM均衡器"""
    
    def __init__(self, method='mmse'):
        self.method = method
        
    def equalize(self, Y, H_est, noise_var=0.01, signal_var=1.0):
        """信道均衡"""
        if self.method == 'zf':
            # ZF均衡
            X_eq = Y / H_est
        elif self.method == 'mmse':
            # MMSE均衡
            H_conj = np.conj(H_est)
            denom = np.abs(H_est)**2 + noise_var/signal_var
            X_eq = Y * H_conj / denom
        else:
            raise ValueError(f"Unknown method: {self.method}")
        
        return X_eq
    
    def detect(self, X_eq, constellation):
        """符号检测（硬判决）"""
        detected = np.zeros(len(X_eq), dtype=complex)
        for i, x in enumerate(X_eq):
            # 最近邻检测
            distances = np.abs(x - constellation)
            detected[i] = constellation[np.argmin(distances)]
        return detected

# 测试
eq = OFDMEqualizer(method='mmse')
# ... 假设已有 Y 和 H_est
# X_eq = eq.equalize(Y, H_est)
```

---

## 本阶段总结

### 关键要点

1. **FFT/IFFT**是OFDM的核心变换
2. **子载波正交性**保证无ICI传输
3. **CP**抵抗多径，简化均衡
4. **导频**辅助相位跟踪和信道估计
5. **LS/MMSE均衡**恢复发送符号

### 与验证工作的联系

- FFT定点精度验证
- CP时序验证
- 信道估计算法验证
- 均衡器性能测试
- 导频检测覆盖率

