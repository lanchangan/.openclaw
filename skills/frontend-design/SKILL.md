---
name: frontend-design
description: 前端设计和UI/UX最佳实践指南，包含设计系统、组件设计、响应式布局、 accessibility、用户体验优化等内容。帮助开发者设计出美观、易用、高性能的前端界面。当前端设计界面、优化用户体验时使用。
---

# 前端设计最佳实践

## 核心内容
### 🎨 设计系统
- **颜色系统**：配色方案、色彩对比度、主题切换最佳实践
- **排版系统**：字体选择、字号层级、行高、字重规范
- **间距系统**：8px栅格系统、内外边距规范
- **组件库**：组件设计原则、可复用组件设计规范
- **设计令牌**：Design Token的定义和使用方法

### 📱 响应式设计
- **断点设计**：常用响应式断点和适配策略
- **移动优先**：移动优先的设计和开发流程
- **弹性布局**：Flexbox/Grid布局最佳实践
- **触摸友好**：移动端交互设计规范，点击区域大小
- **自适应图片**：响应式图片和资源加载策略

### ♿ 可访问性 (Accessibility)
- **语义化HTML**：正确使用语义化标签
- **键盘导航**：支持完整的键盘操作
- **屏幕阅读器**：ARIA标签和语义化支持
- **颜色对比度**：满足WCAG 2.1 AA级标准
- **焦点管理**：焦点状态和跳转逻辑设计

### 🎯 用户体验优化
- **加载体验**：首屏加载、骨架屏、加载状态设计
- **交互反馈**：点击反馈、状态提示、错误提示
- **导航设计**：清晰的导航结构和面包屑设计
- **表单设计**：表单布局、验证、错误处理最佳实践
- **空状态**：空页面、错误页面、404页面设计

### ⚡ 性能优化
- **CSS优化**：CSS书写规范、避免重排重绘
- **动画优化**：高性能动画实现方式
- **资源优化**：图片、字体、静态资源优化
- **懒加载**：图片、组件、路由懒加载策略
- **性能预算**：页面性能指标和优化目标

## 设计规范示例
### 颜色规范
```css
/* 主色调 */
--color-primary: #2563eb;
--color-primary-hover: #1d4ed8;
--color-primary-active: #1e40af;

/* 中性色 */
--color-gray-50: #f9fafb;
--color-gray-100: #f3f4f6;
--color-gray-200: #e5e7eb;
--color-gray-900: #111827;

/* 功能色 */
--color-success: #10b981;
--color-warning: #f59e0b;
--color-error: #ef4444;
--color-info: #3b82f6;
```

### 排版规范
```css
--font-family-sans: 'Inter', system-ui, -apple-system, sans-serif;
--font-size-xs: 0.75rem; /* 12px */
--font-size-sm: 0.875rem; /* 14px */
--font-size-base: 1rem; /* 16px */
--font-size-lg: 1.125rem; /* 18px */
--font-size-xl: 1.25rem; /* 20px */
--font-size-2xl: 1.5rem; /* 24px */
--font-size-3xl: 1.875rem; /* 30px */
--font-size-4xl: 2.25rem; /* 36px */
```

### 间距规范
```css
--spacing-1: 0.25rem; /* 4px */
--spacing-2: 0.5rem; /* 8px */
--spacing-3: 0.75rem; /* 12px */
--spacing-4: 1rem; /* 16px */
--spacing-5: 1.25rem; /* 20px */
--spacing-6: 1.5rem; /* 24px */
--spacing-8: 2rem; /* 32px */
--spacing-10: 2.5rem; /* 40px */
```

## 触发场景
- 设计前端界面和UI组件
- 优化用户体验和交互设计
- 搭建前端设计系统和组件库
- 实现响应式布局和移动端适配
- 提升网站的可访问性和可用性
