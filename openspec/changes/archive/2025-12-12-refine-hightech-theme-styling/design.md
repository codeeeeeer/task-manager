# Design: Refine Theme Styling

## Overview
本设计文档描述如何将现有的两种主题样式调整为符合 gemini-style.md 中定义的设计规范:
- 高科技主题 → "高科技赛博风"设计规范
- 默认主题 → "明亮简约风"设计规范

## Design Principles

### 1. 渐进式优化
- 保持现有主题切换机制不变
- 仅调整 CSS 变量和样式定义
- 不破坏现有功能和用户体验

### 2. 设计规范对齐
- 严格遵循 gemini-style.md 中的色彩系统定义
- 高科技主题: 实现辉光、磨砂玻璃等科技感视觉效果
- 默认主题: 实现清晰、简约、专业的视觉效果
- 确保所有 UI 元素符合各自风格定位

### 3. 组件一致性
- 统一所有 Element Plus 组件在两种主题下的样式
- 确保自定义组件与 Element Plus 组件视觉一致
- 维护良好的视觉层次和可读性

## Architecture

### 色彩系统调整

#### 高科技主题 - 当前实现
```scss
.theme-tech {
  --color-primary: #00ffff;
  --color-bg-body: #0a0e27;
  --color-bg-container: #1a1f3a;
  --color-bg-header: #0d1128;
  --color-bg-sidebar: #151a30;
  --color-text-primary: #e0e0e0;
  --color-text-secondary: #a0a0a0;
  --color-border: #2a3f5f;
}
```

#### 高科技主题 - 目标实现 (基于 gemini-style.md)
```scss
.theme-tech {
  // 背景色系统
  --color-bg-body: #0B1120;           // 深蓝黑 (规范要求)
  --color-bg-container: #1E293B;      // 深石板灰 (规范要求)
  --color-bg-header: #0B1120;         // 与全局背景一致
  --color-bg-sidebar: #1E293B;        // 与内容区域一致

  // 主色调系统
  --color-primary: #06B6D4;           // 霓虹蓝 (规范建议)
  --color-secondary: #8B5CF6;         // 电光紫 (辅助色)
  --color-danger: #F43F5E;            // 警示红 (规范要求)
  --color-hover: #22D3EE;             // 主色调亮化版本

  // 文字颜色系统
  --color-text-primary: #F8FAFC;      // 亮白 (规范要求)
  --color-text-secondary: #CBD5E1;    // 蓝灰 (规范要求)
  --color-text-highlight: #06B6D4;    // 数据高亮

  // 边框系统
  --color-border: #334155;            // 深灰蓝 (规范要求)
  --color-border-glow: rgba(6, 182, 212, 0.3); // 发光边框
}
```

#### 默认主题 - 目标实现 (基于 gemini-style.md)
```scss
.theme-light { // 或默认主题
  // 背景色系统
  --color-bg-body: #F3F4F6;           // 极浅灰 (规范要求)
  --color-bg-container: #FFFFFF;      // 纯白 (规范要求)
  --color-bg-header: #FFFFFF;         // 纯白
  --color-bg-sidebar: #FFFFFF;        // 纯白

  // 主色调系统
  --color-primary: #3B82F6;           // 标准蓝 (规范要求)
  --color-hover: #2563EB;             // 深蓝 (规范要求)

  // 文字颜色系统
  --color-text-primary: #111827;      // 近乎黑 (规范要求)
  --color-text-secondary: #374151;    // 深灰 (规范要求)
  --color-text-tertiary: #6B7280;     // 中灰 (规范要求)

  // 边框系统
  --color-border: #E5E7EB;            // 浅灰 (规范要求)
}
```

### 元素样式调整

#### 高科技主题 - 卡片 (Cards)
- **圆角**: 从 8px 调整为 2-4px (硬朗风格)
- **背景**: 添加半透明磨砂玻璃效果 `backdrop-filter: blur(10px)`
- **边框**: 1px 实线,激活时发光效果
- **阴影**: 增强辉光效果 `box-shadow: 0 0 15px rgba(6, 182, 212, 0.2)`

#### 默认主题 - 卡片 (Cards)
- **圆角**: 8px (中等圆角)
- **背景**: 纯白 `#FFFFFF`
- **边框**: 可选,浅灰色 `#E5E7EB`
- **阴影**: 轻微浮起 `box-shadow: 0 1px 3px rgba(0,0,0,0.1)`

#### 高科技主题 - 按钮 (Buttons)
- **形状**: 保持矩形,考虑添加切角设计 (可选)
- **辉光效果**: 增强 box-shadow,悬停时光晕增强
- **背景**: 半透明背景 + 边框发光
- **特效**: 悬停时背景色变亮,光晕扩散

#### 默认主题 - 按钮 (Buttons)
- **形状**: 矩形,圆角 6px
- **实心按钮**: 主色背景,白色文字,无边框
- **描边按钮**: 白色背景,灰色边框,深灰文字
- **特效**: 悬停时背景色加深

#### 高科技主题 - 表格 (Tables)
- **表头**: 深色背景 + 底部青色荧光条
- **行样式**: 深色背景,文字轻微发光
- **边框**: 使用低透明度实线或虚线
- **悬停**: 行悬停时背景色变化 + 轻微发光

#### 默认主题 - 表格 (Tables)
- **表头**: 浅灰色背景 `#F9FAFB`,加粗深色文字
- **行样式**: 白色背景,底部细分割线
- **斑马纹**: 可选,偶数行极浅灰
- **悬停**: 行悬停时背景色变为浅灰

#### 高科技主题 - 输入框 (Inputs)
- **背景**: 深色 `#0F172A` (规范要求)
- **边框**: 默认深灰,聚焦时高亮青色 + 扩散光影
- **文字**: 考虑使用等宽字体增加科技感 (可选)

#### 默认主题 - 输入框 (Inputs)
- **背景**: 白色 `#FFFFFF`
- **边框**: 浅灰 `#D1D5DB`,聚焦时变蓝 + 淡蓝色光晕 (Ring)
- **文字**: 近乎黑 `#111827`

### 特殊效果实现

#### 磨砂玻璃效果
```scss
.el-card {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
```

#### 辉光效果增强
```scss
.glow-effect {
  box-shadow:
    0 0 5px rgba(6, 182, 212, 0.3),
    0 0 10px rgba(6, 182, 212, 0.2),
    0 0 15px rgba(6, 182, 212, 0.1);
}

.glow-effect:hover {
  box-shadow:
    0 0 10px rgba(6, 182, 212, 0.5),
    0 0 20px rgba(6, 182, 212, 0.3),
    0 0 30px rgba(6, 182, 212, 0.2);
}
```

#### 文字发光效果
```scss
.text-glow {
  text-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
}
```

## Implementation Strategy

### Phase 1: 色彩系统更新
1. 更新高科技主题 CSS 变量定义
2. 更新默认主题 CSS 变量定义
3. 调整主色调和背景色
4. 验证所有页面在两种主题下的色彩一致性

### Phase 2: 核心元素样式优化
1. 优化高科技主题元素样式 (卡片、按钮、表格、输入框)
2. 优化默认主题元素样式 (卡片、按钮、表格、输入框)
3. 确保两种主题的视觉风格差异明显

### Phase 3: 特殊效果增强
1. 高科技主题: 添加磨砂玻璃效果、增强辉光效果、添加文字发光效果
2. 默认主题: 优化阴影效果、优化聚焦光晕效果
3. 优化动画过渡效果

### Phase 4: 组件全面覆盖
1. 验证所有 Element Plus 组件在两种主题下的样式
2. 调整自定义组件样式
3. 确保首页驾驶舱在两种主题下样式完美呈现

## Trade-offs

### 性能 vs 视觉效果
- **Trade-off**: backdrop-filter 和多层 box-shadow 可能影响渲染性能
- **决策**: 优先视觉效果,因为管理后台通常不会有大量元素同时渲染
- **缓解**: 合理使用 will-change 属性优化动画性能

### 可读性 vs 科技感
- **Trade-off**: 过强的辉光效果可能影响文字可读性
- **决策**: 在保证可读性的前提下适度增强科技感
- **缓解**: 使用 `#F8FAFC` 亮白色作为主要文字颜色,确保对比度

### 浏览器兼容性 vs 视觉效果
- **Trade-off**: backdrop-filter 在某些旧浏览器中不支持
- **决策**: 优先现代浏览器体验,提供降级方案
- **缓解**: 使用 `@supports` 检测,不支持时使用纯色背景

## Testing Strategy

### 视觉回归测试
- 在不同页面切换主题,验证两种主题的样式一致性
- 测试所有 Element Plus 组件在高科技主题和默认主题下的表现
- 验证响应式布局在不同屏幕尺寸下的效果
- 确保两种主题的视觉风格差异符合设计规范

### 浏览器兼容性测试
- Chrome (主要目标浏览器)
- Firefox
- Safari
- Edge

### 性能测试
- 使用 Chrome DevTools 监控渲染性能
- 确保页面加载和交互流畅度不受影响

## Future Enhancements
- 考虑添加主题自定义功能,允许用户选择主色调
- 探索更多赛博朋克风格的动画效果
- 考虑添加粒子效果或网格背景增强科技感
