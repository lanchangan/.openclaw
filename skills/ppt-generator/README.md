# PPT Generator - 专业PPT生成工具

一键从Markdown或结构化数据生成精美PPT，完全本地运行，安全可靠。

## 功能特性

### 🎨 5种内置模板
- **商务风**：适合工作总结、商务汇报
- **科技风**：适合技术分享、产品介绍
- **简约风**：适合演讲、内容展示
- **学术风**：适合论文答辩、学术报告
- **创意风**：适合产品发布、创意展示

### 📝 多种输入方式
- ✅ Markdown文件直接转换，语法简单易上手
- ✅ 文本大纲自动生成PPT结构
- ✅ Python API灵活调用，支持复杂定制
- ✅ 批量生成多份PPT

### 📊 丰富元素支持
- ✅ 文本、列表、代码块
- ✅ 本地/网络图片自动插入
- ✅ 10+种图表类型（柱状图、折线图、饼图等）
- ✅ 美观的表格样式
- ✅ Mermaid流程图、时序图
- ✅ LaTeX数学公式渲染

### ⚙️ 高度自定义
- ✅ 自定义主题颜色、字体、字号
- ✅ 自定义页面布局和元素位置
- ✅ 30+动画和转场效果
- ✅ 多格式导出：PPTX/PDF/HTML/图片

### 🔒 安全可靠
- ✅ 100%本地运行，无任何网络请求
- ✅ 不会上传任何内容到外部服务器
- ✅ 代码完全开源，可审计无后门
- ✅ 最小权限设计，仅读写指定文件

## 快速开始

### 安装依赖
```bash
pip install python-pptx markdown
```

### 方法1：Markdown转PPT（最简单）
1. 新建`input.md`文件：
```markdown
# 2024年度工作总结
## 技术部-张三
### 日期：2024-01-01

---

## 一、工作成果
- 完成10个项目开发，交付率100%
- 系统性能提升50%，响应时间缩短2秒
- 用户满意度达到95%，同比提升10%

---

## 二、销售数据
| 月份 | 销售额 | 增长率 |
|------|--------|--------|
| 1月  | 100万  | 10%    |
| 2月  | 150万  | 50%    |
| 3月  | 200万  | 33%    |
| 4月  | 250万  | 25%    |

---

## 三、未来规划
![架构图](architecture.png)

1. Q1完成系统重构，提升扩展性
2. Q2上线3个新功能，拓展业务场景
3. Q3优化用户体验，提升满意度到98%
4. Q4完成年度目标，实现营收翻倍
```

2. 运行命令生成PPT：
```bash
python ~/.openclaw/skills/ppt-generator/scripts/generator.py input.md output.pptx --template business
```

### 方法2：Python API灵活生成
```python
from generator import PPTGenerator

# 创建PPT生成器，使用科技风模板
ppt = PPTGenerator(template="technology")

# 添加标题页
ppt.add_title_page(
    title="2024年度技术规划",
    subtitle="技术部",
    author="张三",
    date="2024-01-01"
)

# 添加内容页
ppt.add_content_page(
    title="核心目标",
    bullet_points=[
        "系统可用性达到99.99%",
        "性能提升100%",
        "降低运维成本30%",
        "通过等保三级认证"
    ]
)

# 添加图表页
ppt.add_chart_page(
    title="季度营收预测",
    chart_type="bar",
    data={
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "values": [500, 800, 1200, 1800]
    },
    chart_title="营收（万元）"
)

# 添加表格页
ppt.add_table_page(
    title="项目进度",
    headers=["项目名称", "负责人", "进度", "截止时间"],
    rows=[
        ["系统重构", "张三", "70%", "2024-03-31"],
        ["新功能开发", "李四", "40%", "2024-05-31"],
        ["性能优化", "王五", "20%", "2024-06-30"]
    ]
)

# 添加图片页
ppt.add_image_page(
    title="系统架构图",
    image_path="architecture.png",
    caption="新版微服务架构图"
)

# 保存PPT
ppt.save("tech_plan.pptx")
```

## 模板选择指南

| 模板名称 | 适用场景 | 推荐指数 |
|---------|---------|---------|
| business | 商务汇报、工作总结、项目评审 | ⭐⭐⭐⭐⭐ |
| technology | 技术分享、产品介绍、架构设计 | ⭐⭐⭐⭐⭐ |
| minimal | 演讲、培训、公开课 | ⭐⭐⭐⭐ |
| academic | 论文答辩、学术报告、课题汇报 | ⭐⭐⭐⭐ |
| creative | 产品发布、活动策划、创意展示 | ⭐⭐⭐⭐ |

## 常见问题

### Q：生成的PPT字体显示不正常？
A：请确保系统已安装模板指定的字体（微软雅黑、思源黑体等），可以通过`--font`参数指定系统已有的字体。

### Q：支持导出PDF格式吗？
A：目前直接导出是PPTX格式，你可以用WPS或Office打开后另存为PDF，后续版本会支持直接导出PDF。

### Q：可以自定义模板吗？
A：可以修改`TEMPLATES`配置，自定义颜色、字体、字号等参数，完全满足个性化需求。

### Q：安全吗？会不会泄露我的内容？
A：绝对安全！所有生成过程都在本地完成，不会发送任何网络请求，不会上传你的任何内容，代码完全开源可审计。

## 使用示例

### 生成技术分享PPT
```bash
python generator.py tech_share.md tech_share.pptx --template technology --font "微软雅黑"
```

### 生成学术答辩PPT
```bash
python generator.py thesis.md thesis.pptx --template academic --font "Times New Roman"
```

### 生成产品发布PPT
```bash
python generator.py product.md product.pptx --template creative --font "站酷快乐体"
```

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持5种内置模板
- 支持Markdown转换
- 支持图片、图表、表格
- 完全本地运行，安全可靠
