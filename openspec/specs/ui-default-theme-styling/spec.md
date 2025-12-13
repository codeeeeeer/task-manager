# ui-default-theme-styling Specification

## Purpose
TBD - created by archiving change refine-hightech-theme-styling. Update Purpose after archive.
## Requirements
### Requirement: 色彩系统规范
系统SHALL实现符合 gemini-style-v2.txt 规范的默认主题色彩系统，使用标准化的 CSS 变量命名。

#### Scenario: CSS 变量定义
- **WHEN** 系统初始化默认主题（:root）
- **THEN** 系统定义以下 CSS 变量:
  - `--el-color-primary: #3b82f6` (品牌蓝)
  - `--el-color-success: #10b981`
  - `--el-color-warning: #f59e0b`
  - `--el-color-danger: #ef4444`
  - `--el-color-info: #6b7280`
  - `--el-bg-color: #f3f4f6` (全局背景)
  - `--el-bg-color-overlay: #ffffff` (卡片/弹窗背景)
  - `--el-bg-color-page: #f9fafb` (页面内容区)
  - `--el-text-color-primary: #111827`
  - `--el-text-color-regular: #374151`
  - `--el-text-color-secondary: #6b7280`
  - `--el-border-color: #e5e7eb`
  - `--el-border-color-light: #f3f4f6`

#### Scenario: 自定义业务变量
- **WHEN** 系统初始化默认主题
- **THEN** 系统定义以下自定义变量:
  - `--app-card-radius: 8px` (中等圆角)
  - `--app-shadow: 0 1px 3px rgba(0,0,0,0.1)` (轻微浮起)
  - `--app-font-family: 'Inter', system-ui, sans-serif`
  - `--app-button-shape: 6px` (按钮圆角)

### Requirement: 卡片元素样式
系统SHALL实现符合明亮简约风格的卡片样式,包括圆角、背景、边框和阴影效果。

#### Scenario: 卡片基础样式
- **WHEN** 卡片元素在默认主题下渲染
- **THEN** 系统应用以下样式:
  - 圆角: 8px (中等圆角)
  - 背景: 纯白 `#FFFFFF`
  - 边框: 可选,浅灰色 `#E5E7EB`
  - 阴影: `0 1px 3px rgba(0,0,0,0.1)` (轻微浮起)

#### Scenario: 卡片悬停状态
- **WHEN** 卡片处于悬停状态
- **THEN** 系统可选增强阴影效果:
  - 阴影增强为 `0 4px 6px rgba(0,0,0,0.1)`

### Requirement: 按钮元素样式
系统SHALL实现清晰简约的按钮样式,支持实心和描边两种类型。

#### Scenario: 实心按钮基础样式
- **WHEN** 实心按钮在默认主题下渲染
- **THEN** 系统应用以下样式:
  - 形状: 矩形,圆角 6px
  - 背景: 主色 `#3B82F6`
  - 文字颜色: 白色
  - 无边框

#### Scenario: 实心按钮悬停效果
- **WHEN** 用户悬停在实心按钮上
- **THEN** 系统应用悬停效果:
  - 背景色变为悬停色 `#2563EB`

#### Scenario: 描边按钮基础样式
- **WHEN** 描边按钮在默认主题下渲染
- **THEN** 系统应用以下样式:
  - 形状: 矩形,圆角 6px
  - 背景: 白色
  - 边框: 1px 实线,灰色 `#D1D5DB`
  - 文字颜色: 深灰 `#374151`

#### Scenario: 描边按钮悬停效果
- **WHEN** 用户悬停在描边按钮上
- **THEN** 系统应用悬停效果:
  - 边框颜色变为主色 `#3B82F6`
  - 文字颜色变为主色

### Requirement: 表格元素样式
系统SHALL实现清晰简约的表格样式,包括表头、行样式和分割线。

#### Scenario: 表格表头样式
- **WHEN** 表格在默认主题下渲染
- **THEN** 系统应用以下表头样式:
  - 背景色: `#F9FAFB` (浅灰色)
  - 文字颜色: `#111827` (近乎黑)
  - 文字加粗

#### Scenario: 表格行样式
- **WHEN** 表格行在默认主题下渲染
- **THEN** 系统应用以下样式:
  - 背景色: `#FFFFFF` (白色)
  - 文字颜色: `#374151` (深灰)
  - 底部边框: 1px 实线,颜色 `#E5E7EB` (细分割线)

#### Scenario: 表格斑马纹样式(可选)
- **WHEN** 表格启用斑马纹样式
- **THEN** 偶数行背景色为 `#F9FAFB` (极浅灰)

#### Scenario: 表格行悬停效果
- **WHEN** 用户悬停在表格行上
- **THEN** 系统应用悬停效果:
  - 背景色变为 `#F3F4F6` (浅灰)

### Requirement: 输入框元素样式
系统SHALL实现清晰简约的输入框样式,包括背景、边框和聚焦状态。

#### Scenario: 输入框基础样式
- **WHEN** 输入框在默认主题下渲染
- **THEN** 系统应用以下样式:
  - 背景色: `#FFFFFF` (白色)
  - 边框: 1px 实线,颜色 `#D1D5DB` (浅灰)
  - 文字颜色: `#111827` (近乎黑)
  - 圆角: 6px

#### Scenario: 输入框聚焦效果
- **WHEN** 用户聚焦在输入框上
- **THEN** 系统应用聚焦效果:
  - 边框颜色变为主色 `#3B82F6`
  - 添加淡蓝色光晕 (Ring): `0 0 0 3px rgba(59, 130, 246, 0.1)`

#### Scenario: 下拉框和选择器样式
- **WHEN** 下拉框或选择器在默认主题下渲染
- **THEN** 系统应用与输入框一致的样式
- **WHEN** 下拉菜单展开
- **THEN** 下拉菜单背景为白色,边框为浅灰,带有轻微阴影

### Requirement: 标签和链接样式
系统SHALL实现清晰简约的标签和链接样式。

#### Scenario: 标签基础样式
- **WHEN** 标签在默认主题下渲染
- **THEN** 系统应用以下样式:
  - 背景: 浅色 (根据标签类型)
  - 边框: 可选,1px 实线
  - 文字颜色: 深色
  - 圆角: 4px

#### Scenario: 链接样式
- **WHEN** 链接在默认主题下渲染
- **THEN** 系统应用以下样式:
  - 文字颜色: 主色 `#3B82F6`
  - 可选下划线
- **WHEN** 用户悬停在链接上
- **THEN** 文字颜色变为悬停色 `#2563EB`,下划线显示

### Requirement: 首页驾驶舱样式
系统SHALL为首页驾驶舱实现清晰简约的视觉效果。

#### Scenario: 统计卡片样式
- **WHEN** 首页统计卡片在默认主题下渲染
- **THEN** 系统应用以下样式:
  - 背景: 纯白 `#FFFFFF`
  - 边框: 可选,浅灰色
  - 阴影: `0 1px 3px rgba(0,0,0,0.1)` (轻微浮起)
  - 统计数值: 大号字体,深色,加粗
  - 统计标签: 中灰色,中等字重

#### Scenario: 统计卡片悬停效果
- **WHEN** 用户悬停在统计卡片上
- **THEN** 系统可选增强阴影效果:
  - 阴影增强为 `0 4px 6px rgba(0,0,0,0.1)`

#### Scenario: 图表容器样式
- **WHEN** 图表容器在默认主题下渲染
- **THEN** 系统应用与卡片一致的样式
- **AND** 图表使用主色调作为主要颜色
- **AND** 图表背景为白色

### Requirement: 对话框和弹窗样式
系统SHALL实现清晰简约的对话框和弹窗样式。

#### Scenario: 对话框基础样式
- **WHEN** 对话框在默认主题下显示
- **THEN** 系统应用以下样式:
  - 背景: `#FFFFFF` (纯白)
  - 边框: 可选,浅灰色
  - 阴影: `0 10px 25px rgba(0,0,0,0.1)` (轻微浮起)
  - 圆角: 8px

#### Scenario: 对话框标题样式
- **WHEN** 对话框标题在默认主题下渲染
- **THEN** 系统应用以下样式:
  - 文字颜色: `#111827` (近乎黑)
  - 文字加粗
  - 底部边框: 1px 实线,颜色 `#E5E7EB`

#### Scenario: 对话框内容样式
- **WHEN** 对话框内容在默认主题下渲染
- **THEN** 文字颜色为 `#374151` (深灰)
- **AND** 所有表单元素应用默认主题样式

### Requirement: 加载和骨架屏样式
系统SHALL实现清晰简约的加载动画和骨架屏样式。

#### Scenario: 加载遮罩样式
- **WHEN** 加载遮罩在默认主题下显示
- **THEN** 系统应用以下样式:
  - 背景: `rgba(255, 255, 255, 0.8)` (半透明白色)
  - 加载图标颜色: 主色调 `#3B82F6`

#### Scenario: 骨架屏样式
- **WHEN** 骨架屏在默认主题下显示
- **THEN** 系统应用以下样式:
  - 骨架颜色: `#E5E7EB` (浅灰)
  - 动画颜色: `#F3F4F6` (极浅灰)
  - 保持脉冲动画效果

### Requirement: 主题切换平滑过渡
系统SHALL在主题切换时提供平滑的视觉过渡效果。

#### Scenario: 主题切换动画
- **WHEN** 用户切换主题
- **THEN** 系统应用 CSS transition 实现平滑过渡:
  - 过渡属性: background-color, color, border-color, box-shadow
  - 过渡时间: 0.3s
  - 过渡函数: ease-in-out

#### Scenario: 主题切换性能
- **WHEN** 用户切换主题
- **THEN** 主题切换MUST在 500ms 内完成
- **AND** 不应出现明显的页面闪烁或卡顿

### Requirement: 字体系统规范
系统SHALL使用专业的字体系统以提升可读性和视觉层次。

#### Scenario: 全局字体应用
- **WHEN** body 元素渲染
- **THEN** 系统应用字体:
  - `font-family: var(--app-font-family)`
  - 平滑过渡: `transition: background-color 0.3s, color 0.3s`

### Requirement: Element Plus 组件样式覆盖
系统SHALL对 Element Plus 组件进行样式覆盖以符合默认主题规范。

#### Scenario: 卡片组件样式
- **WHEN** `.el-card` 在默认主题下渲染
- **THEN** 系统应用:
  - 圆角使用 `var(--app-card-radius)`
  - 阴影使用 `var(--app-shadow)`
  - 背景使用 `var(--el-bg-color-overlay)`

#### Scenario: 按钮组件样式
- **WHEN** `.el-button` 在默认主题下渲染
- **THEN** 系统应用:
  - 圆角使用 `var(--app-button-shape)`
  - 主按钮背景使用 `var(--el-color-primary)`
  - 悬停时背景变为 `#2563EB`

#### Scenario: 输入框组件样式
- **WHEN** `.el-input__wrapper` 在默认主题下渲染
- **THEN** 系统应用:
  - 背景色为白色
  - 边框颜色为 `#d1d5db`
  - 聚焦时边框颜色变为主色，添加光晕 `0 0 0 3px rgba(59, 130, 246, 0.1)`

#### Scenario: 表格组件样式
- **WHEN** `.el-table` 在默认主题下渲染
- **THEN** 系统应用:
  - 表头背景为 `#f9fafb`
  - 行背景为白色
  - 边框颜色为 `var(--el-border-color)`
  - 悬停行背景为 `#f3f4f6`

