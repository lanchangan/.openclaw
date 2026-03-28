---
name: vercel-react-best-practices
description: Vercel + React开发最佳实践指南，包含项目搭建、性能优化、部署配置、错误处理等完整的开发规范。帮助开发者快速构建高质量的React应用并部署到Vercel。当开发React项目、部署到Vercel时使用。
---

# Vercel + React 最佳实践

## 核心内容
### 🏗️ 项目搭建
- **项目初始化**：推荐使用Next.js框架，Vercel原生支持
- **目录结构**：标准的React项目目录结构规范
- **依赖管理**：推荐的依赖包和版本管理策略
- **类型安全**：TypeScript配置最佳实践

### ⚡ 性能优化
- **代码分割**：路由级和组件级代码分割策略
- **静态生成**：SSG/ISR/SSR的使用场景和最佳实践
- **图片优化**：使用next/image组件优化图片加载
- **缓存策略**：Vercel Edge Network缓存配置
- **Bundle分析**：减少包体积的优化技巧

### 🚀 部署配置
- **Vercel配置**：vercel.json配置文件最佳实践
- **环境变量**：环境变量管理和安全配置
- **构建优化**：构建命令配置和缓存优化
- **预览部署**：PR预览部署的配置和使用
- **自定义域名**：域名绑定和HTTPS配置

### 🔧 开发流程
- **代码规范**：ESLint + Prettier配置
- **测试策略**：单元测试、集成测试、E2E测试最佳实践
- **CI/CD流程**：自动化构建、测试、部署流程
- **错误监控**：Sentry集成和错误处理策略
- **性能监控**：Core Web Vitals监控和优化

### 📈 生产环境最佳实践
- **安全配置**：CSP、XSS防护、安全头设置
- **SEO优化**：元数据配置、结构化数据、站点地图
- **国际化**：多语言支持最佳实践
- **A/B测试**：Vercel Edge Functions实现A/B测试
- **灰度发布**：增量发布和回滚策略

## 项目模板
推荐的Next.js项目结构：
```
your-app/
├── app/                    # App Router目录
│   ├── layout.tsx         # 根布局
│   ├── page.tsx           # 首页
│   └── api/               # API路由
├── components/            # 公共组件
├── lib/                   # 工具库
├── public/                # 静态资源
├── next.config.js         # Next.js配置
├── vercel.json            # Vercel配置
└── package.json
```

## 部署配置示例
`vercel.json`配置：
```json
{
  "buildCommand": "next build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "installCommand": "npm install",
  "regions": ["sin1"],
  "env": {
    "NODE_ENV": "production"
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" }
      ]
    }
  ]
}
```

## 触发场景
- 开发React/Next.js项目
- 需要部署应用到Vercel平台
- 想要优化React应用的性能
- 学习React开发最佳实践
- 搭建标准化的React开发流程
