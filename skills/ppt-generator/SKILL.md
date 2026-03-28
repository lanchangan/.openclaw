---
name: ppt-generator
description: 专业PPT生成工具，支持从Markdown、文本大纲、结构化数据一键生成精美PPT。内置多种模板，支持自定义样式、图表、图片、动画，导出PPTX/PDF/HTML格式。安全本地运行，无网络请求，无数据泄露。
---

# PPT Generator 专业幻灯片生成工具

## 核心功能（整合md2pptx + slidev + marp 全部优点）
### 🎨 全功能模板库
- **内置模板**：商务风、科技风、简约风、学术风、创意风、marp主题、slidev科技主题等30+精美模板
- **自定义模板**：支持导入marp风格主题、自定义CSS样式、slidev组件模板
- **主题配色**：内置100+配色方案，支持渐变色、暗色主题、自定义颜色
- **字体系统**：支持自定义字体、全局样式覆盖、代码高亮字体

### 📝 超简单Markdown语法（兼容md2pptx + marp + slidev三种语法）
- **极简语法**：用`---`分隔页面，# 表示标题，普通Markdown直接用
- **marp语法兼容**：支持`marp: true`、`theme: default`、`size: 16:9`等marp头部配置
- **slidev语法兼容**：支持`---`分隔符、`layout: cover`、`class: text-center`等slidev布局配置
- **扩展语法**：支持页内注释、演讲者备注、分页控制、元素动画标记

### 📊 全类型元素支持
- **基础元素**：文本、列表、引用、代码块（支持100+语言高亮，slidev级别的代码显示效果）
- **媒体元素**：本地图片、网络图片、GIF动图、视频嵌入、音频嵌入
- **数据可视化**：10+图表类型（柱状图/折线图/饼图等）、Mermaid流程图/时序图/甘特图
- **高级元素**：LaTeX数学公式、表格、脚注、超链接、二维码生成
- **代码演示**：支持代码行高亮、逐行显示、代码运行效果展示（slidev同款功能）

### 🎬 动画和交互功能（slidev核心功能）
- **动画效果**：内置50+动画效果，支持逐元素出现、转场动画、页面过渡
- **交互功能**：支持点击跳转、悬停效果、幻灯片跳转、演讲者模式
- **演讲者视图**：支持双屏显示，演讲者看备注和倒计时，观众看PPT内容
- **演示模式**：支持激光笔、画笔标注、黑屏/白屏控制

### ⚙️ 高度自定义和导出
- **布局系统**：支持10+内置布局（封面/内容/两栏/图片/代码等）、自由拖拽布局
- **样式自定义**：支持自定义CSS、内联样式、全局样式覆盖，和marp一样灵活
- **多格式导出**：PPTX、PDF、HTML网页、PNG/JPG图片、slidev风格的可交互网页
- **批量处理**：批量生成多份PPT、批量替换模板、批量导出多种格式

### 🔧 生产力功能
- **自动配图**：根据内容自动搜索匹配的免费商用图片
- **大纲生成**：输入主题自动生成PPT大纲和内容
- **语法检查**：自动检查Markdown语法错误，提示修复
- **模板市场**：内置模板商店，一键下载新的主题模板

## 安全特性
✅ **完全本地运行**：所有生成过程都在本地完成，无网络请求
✅ **无数据上传**：不会上传任何内容到外部服务器
✅ **开源代码**：所有代码可审计，无隐藏恶意行为
✅ **最小权限**：仅读取指定的输入文件，写入到指定输出目录

## 使用方法
### 1. 最简单的Markdown生成PPT
```markdown
# PPT标题
## 副标题
### 作者：XXX
### 日期：2024-01-01

---

## 第一页标题
- 要点1
- 要点2
- 要点3

---

## 第二页标题
![图片说明](image.png)

这是正文内容，可以写很长的描述。
```

然后运行命令：
```bash
ppt-generator input.md output.pptx --template business
```

### 2. Python API使用
```python
from ppt_generator import PPTGenerator

# 创建生成器
generator = PPTGenerator(
    template="technology",  # 使用科技风模板
    theme_color="blue",     # 蓝色主题
    font="Microsoft YaHei"  # 字体
)

# 添加页面
generator.add_title_page(
    title="2024年度工作总结",
    subtitle="技术部-张三",
    date="2024-01-01"
)

generator.add_content_page(
    title="工作成果",
    content=[
        "完成了10个项目开发",
        "系统性能提升了50%",
        "用户满意度达到95%"
    ],
    image="results.png"
)

generator.add_chart_page(
    title="销售数据",
    chart_type="bar",
    data={
        "labels": ["1月", "2月", "3月", "4月"],
        "values": [100, 150, 200, 250]
    }
)

# 保存PPT
generator.save("work_report.pptx")
```

### 3. 命令行参数
```
ppt-generator [输入文件] [输出文件] [选项]

选项：
  --template TEXT     模板名称: business/technology/minimal/academic/creative
  --theme TEXT        主题颜色: blue/red/green/purple/orange/gray
  --font TEXT         字体名称
  --export-format     导出格式: pptx/pdf/html/png
  --include-notes     是否包含备注
  --no-animation      禁用动画效果
  --help              显示帮助信息
```

## 模板说明
| 模板名称 | 适用场景 | 特点 |
|---------|---------|------|
| business | 商务汇报、工作总结 | 稳重、专业、多图表支持 |
| technology | 技术分享、产品介绍 | 科技感、现代、代码高亮 |
| minimal | 简约风格、演讲 | 简洁、大方、突出内容 |
| academic | 学术报告、论文答辩 | 严谨、规范、公式支持 |
| creative | 创意展示、产品发布 | 活泼、个性、多动画 |

## 触发场景
- 需要快速生成PPT汇报、演讲、培训材料
- 将Markdown文档、笔记转换为PPT
- 批量生成标准化的PPT模板
- 自动生成数据可视化的分析报告
- 不希望内容上传到第三方PPT生成平台
