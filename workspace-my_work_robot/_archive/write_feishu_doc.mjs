// 使用 Node.js 调用飞书文档 API 写入内容
const appId = 'cli_a9340a6fd922dcc6';
const appSecret = 'iEXatjRUBk8cCfedbOBlibZ6ZkYCJeN0';
const docToken = 'JZt7diQjuoWP1kxsay7coU7fnub';

async function main() {
  try {
    // 1. 获取 token
    console.log('Getting token...');
    const tokenRes = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ app_id: appId, app_secret: appSecret })
    });
    const tokenText = await tokenRes.text();
    console.log('Token response:', tokenText.substring(0, 100));
    const tokenData = JSON.parse(tokenText);
    const token = tokenData.tenant_access_token;
    console.log('Token obtained:', token.substring(0, 20) + '...');

    // 2. 创建 blocks
    const blocks = [
      { block_type: 2, heading2: { elements: [{ text_run: { content: 'WiFi PHY 学习计划（时域→频域）' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '专为芯片验证工程师设计 | 每日1小时 | 12周系统学习' } }] } },
      { block_type: 15, divider: {} },
      { block_type: 2, heading2: { elements: [{ text_run: { content: '第一阶段：时域基础（4周）' } }] } },
      { block_type: 3, heading3: { elements: [{ text_run: { content: 'Week 1-2：信号与系统基础' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '目标：建立时域分析的数学基础' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 1: 时域信号基础 - 周期信号、能量/功率信号' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 2: 线性系统响应 - 冲激响应、卷积运算' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 3: 相关函数 - 自相关、互相关、匹配滤波' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 4: 噪声模型 - AWGN、信噪比定义' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 5: 带限信号 - 采样定理回顾' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 6-7: 复习+实践' } }] } },
      { block_type: 3, heading3: { elements: [{ text_run: { content: 'Week 3-4：WiFi时域信号结构' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 8: PPDU帧结构' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 9: 短训练序列' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 10: 长训练序列' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 11: SIGNAL字段' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 12: 数据符号' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 13-14: 复习+实践' } }] } },
      { block_type: 15, divider: {} },
      { block_type: 2, heading2: { elements: [{ text_run: { content: '第二阶段：同步与定时（3周）' } }] } },
      { block_type: 3, heading3: { elements: [{ text_run: { content: 'Week 5-6：时域同步技术' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 15: 包检测' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 16: 符号定时' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 17: 载波频偏估计' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 18: 采样频偏' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 19: 相位噪声' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 20-21: 复习+实践' } }] } },
      { block_type: 3, heading3: { elements: [{ text_run: { content: 'Week 7：同步验证方法论' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 22: 同步测试向量' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 23: 时序检查' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 24: 覆盖率分析' } }] } },
      { block_type: 15, divider: {} },
      { block_type: 2, heading2: { elements: [{ text_run: { content: '第三阶段：频域基础（3周）' } }] } },
      { block_type: 3, heading3: { elements: [{ text_run: { content: 'Week 8-9：FFT与OFDM原理' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 25: DFT/FFT原理' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 26: OFDM调制' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 27: 循环前缀' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 28: 子载波间隔' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 29: 导频子载波' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 30-31: 复习+实践' } }] } },
      { block_type: 3, heading3: { elements: [{ text_run: { content: 'Week 10：信道估计与均衡' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 32: 信道模型' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 33: LS信道估计' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 34: 信道平滑' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 35: 均衡器设计' } }] } },
      { block_type: 15, divider: {} },
      { block_type: 2, heading2: { elements: [{ text_run: { content: '第四阶段：进阶主题（2周）' } }] } },
      { block_type: 3, heading3: { elements: [{ text_run: { content: 'Week 11：MIMO与波束成形' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 36: 空间复用' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 37: 信道探测' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 38: 波束成形' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 39: MU-MIMO' } }] } },
      { block_type: 3, heading3: { elements: [{ text_run: { content: 'Week 12：WiFi 7新特性' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 40: 320MHz带宽' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 41: 4096-QAM' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 42: Multi-RU' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Day 43-45: 总复习' } }] } },
      { block_type: 15, divider: {} },
      { block_type: 2, heading2: { elements: [{ text_run: { content: '学习建议' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '1. 理论与实践结合' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '2. 建立知识图谱' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '3. 关注验证视角' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '4. 记录问题' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '5. 定期回顾' } }] } },
      { block_type: 15, divider: {} },
      { block_type: 2, heading2: { elements: [{ text_run: { content: '推荐资源' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• 802.11-2020 标准' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• 802.11ax/y/z 修正案' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• Wireless Communications - Andrea Goldsmith' } }] } },
      { block_type: 4, paragraph: { elements: [{ text_run: { content: '• MATLAB WLAN Toolbox 文档' } }] } }
    ];

    // 3. 批量创建 blocks
    const url = `https://open.feishu.cn/open-apis/docx/v1/documents/${docToken}/blocks/${docToken}/children/batch_create`;
    
    console.log('Creating blocks...');
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ children: blocks, index: 0 })
    });
    
    const resultText = await res.text();
    console.log('Response:', resultText.substring(0, 500));
    const result = JSON.parse(resultText);
    
    if (result.code === 0) {
      console.log('\n✅ 文档内容写入成功！');
      console.log('文档链接: https://feishu.cn/docx/' + docToken);
    } else {
      console.log('\n❌ 写入失败:', result.msg);
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
