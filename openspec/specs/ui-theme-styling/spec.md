# ui-theme-styling Specification

## Purpose
TBD - created by archiving change refine-hightech-theme-styling. Update Purpose after archive.
## Requirements
### Requirement: 色彩系统规范
系统SHALL实现符合 gemini-style-v2.txt 规范的高科技主题色彩系统，使用霓虹青作为核心色调。

#### Scenario: CSS 变量定义
- **WHEN** 系统切换到高科技主题（html.theme-tech）
- **THEN** 系统覆盖以下 CSS 变量:
  - `--el-color-primary: #06b6d4` (霓虹青)
  - `--el-color-success: #4ade80`
  - `--el-color-warning: #facc15`
  - `--el-color-danger: #f43f5e`
  - `--el-color-primary-light-3: rgba(6, 182, 212, 0.5)`
  - `--el-color-primary-light-7: rgba(6, 182, 212, 0.2)`
  - `--el-color-primary-light-9: rgba(6, 182, 212, 0.1)`
  - `--el-bg-color: #0b1120` (深空黑蓝)
  - `--el-bg-color-overlay: rgba(30, 41, 59, 0.8)` (半透明，配合磨砂)
  - `--el-bg-color-page: #0f172a`
  - `--el-text-color-primary: #f8fafc` (发光白)
  - `--el-text-color-regular: #cbd5e1` (蓝灰)
  - `--el-text-color-secondary: #94a3b8`
  - `--el-border-color: rgba(6, 182, 212, 0.3)` (低透明度青色)
  - `--el-border-color-light: rgba(6, 182, 212, 0.1)`
  - `--el-border-color-lighter: rgba(6, 182, 212, 0.05)`

#### Scenario: 自定义业务变量覆盖
- **WHEN** 系统切换到高科技主题
- **THEN** 系统覆盖以下自定义变量:
  - `--app-card-radius: 2px` (硬朗切角)
  - `--app-shadow: 0 0 15px rgba(6, 182, 212, 0.15)` (霓虹光晕)
  - `--app-font-family: 'JetBrains Mono', 'Roboto', monospace` (科技感字体)
  - `--app-button-shape: 0px` (直角按钮)

### Requirement: 卡片元素样式
系统SHALL实现符合高科技赛博风格的卡片样式,包括圆角、背景、边框和阴影效果。

#### Scenario: 卡片基础样式
- **WHEN** 卡片元素在高科技主题下渲染
- **THEN** 系统应用以下样式:
  - 圆角: 2-4px (硬朗风格)
  - 背景: 半透明深色 `rgba(30, 41, 59, 0.8)`
  - 边框: 1px 实线,颜色 `#334155`
  - 阴影: `0 0 15px rgba(6, 182, 212, 0.2)` (辉光效果)

#### Scenario: 卡片磨砂玻璃效果
- **WHEN** 浏览器支持 backdrop-filter 属性
- **THEN** 系统在卡片上应用磨砂玻璃效果:
  - `backdrop-filter: blur(10px)`
  - `-webkit-backdrop-filter: blur(10px)`

#### Scenario: 卡片激活状态
- **WHEN** 卡片处于激活或悬停状态
- **THEN** 系统增强边框发光效果:
  - 边框颜色变为主色调 `#06B6D4`
  - 阴影增强为 `0 0 20px rgba(6, 182, 212, 0.4)`

### Requirement: 按钮元素样式
系统SHALL实现带有辉光效果的高科技风格按钮,支持悬停和激活状态的视觉反馈。

#### Scenario: 按钮基础样式
- **WHEN** 按钮在高科技主题下渲染
- **THEN** 系统应用以下样式:
  - 形状: 矩形,圆角 4px
  - 背景: 半透明 `rgba(6, 182, 212, 0.2)`
  - 边框: 1px 实线,颜色为主色调
  - 阴影: `0 0 10px rgba(6, 182, 212, 0.5)` (辉光效果)

#### Scenario: 按钮悬停效果
- **WHEN** 用户悬停在按钮上
- **THEN** 系统增强视觉效果:
  - 背景色变亮为 `rgba(6, 182, 212, 0.3)`
  - 边框颜色变为悬停色 `#22D3EE`
  - 阴影增强为 `0 0 15px rgba(6, 182, 212, 0.7)`

#### Scenario: 不同类型按钮的颜色
- **WHEN** 按钮类型为 success
- **THEN** 系统使用绿色系: 背景 `rgba(0, 255, 150, 0.2)`, 边框 `#00ff96`
- **WHEN** 按钮类型为 danger
- **THEN** 系统使用红色系: 背景 `rgba(255, 0, 100, 0.2)`, 边框 `#ff0064`

### Requirement: 表格元素样式
系统SHALL实现高科技风格的表格样式,包括表头荧光条、行样式和边框效果。

#### Scenario: 表格表头样式
- **WHEN** 表格在高科技主题下渲染
- **THEN** 系统应用以下表头样式:
  - 背景色: `#0d1128` (深色)
  - 文字颜色: `#06B6D4` (主色调)
  - 底部边框: 2px 实线,颜色为主色调 (荧光条效果)
  - 文字加粗

#### Scenario: 表格行样式
- **WHEN** 表格行在高科技主题下渲染
- **THEN** 系统应用以下样式:
  - 背景色: `#1E293B` (深色)
  - 文字颜色: `#CBD5E1` (蓝灰)
  - 底部边框: 1px 实线,颜色 `#334155` (低透明度)

#### Scenario: 表格行悬停效果
- **WHEN** 用户悬停在表格行上
- **THEN** 系统应用悬停效果:
  - 背景色变为 `rgba(6, 182, 212, 0.05)`
  - 轻微发光效果

#### Scenario: 表格整体边框
- **WHEN** 表格在高科技主题下渲染
- **THEN** 系统应用整体边框:
  - 外边框: 1px 实线,颜色 `#334155`
  - 阴影: `0 0 15px rgba(6, 182, 212, 0.1)`

### Requirement: 输入框元素样式
系统SHALL实现高科技风格的输入框样式,包括背景、边框和聚焦状态的光影效果。

#### Scenario: 输入框基础样式
- **WHEN** 输入框在高科技主题下渲染
- **THEN** 系统应用以下样式:
  - 背景色: `#0F172A` (深色)
  - 边框: 1px 实线,颜色 `#334155` (深灰)
  - 文字颜色: `#CBD5E1` (蓝灰)
  - 阴影: `0 0 5px rgba(6, 182, 212, 0.2)`

#### Scenario: 输入框聚焦效果
- **WHEN** 用户聚焦在输入框上
- **THEN** 系统应用聚焦效果:
  - 边框颜色变为主色调 `#06B6D4`
  - 阴影增强为 `0 0 10px rgba(6, 182, 212, 0.5)` (扩散光影)
  - 添加外发光效果

#### Scenario: 下拉框和选择器样式
- **WHEN** 下拉框或选择器在高科技主题下渲染
- **THEN** 系统应用与输入框一致的样式
- **WHEN** 下拉菜单展开
- **THEN** 下拉菜单背景为 `#1a1f3a`,边框为 `#2a3f5f`,带有发光阴影

### Requirement: 标签和链接样式
系统SHALL实现高科技风格的标签和链接样式,包括发光效果和悬停状态。

#### Scenario: 标签基础样式
- **WHEN** 标签在高科技主题下渲染
- **THEN** 系统应用以下样式:
  - 背景: `rgba(6, 182, 212, 0.1)` (半透明)
  - 边框: 1px 实线,颜色为主色调
  - 文字颜色: 主色调
  - 阴影: `0 0 5px rgba(6, 182, 212, 0.3)`

#### Scenario: 链接文字发光效果
- **WHEN** 链接在高科技主题下渲染
- **THEN** 系统应用文字发光效果:
  - 文字颜色: 主色调 `#06B6D4`
  - 文字阴影: `0 0 5px rgba(6, 182, 212, 0.5)`
- **WHEN** 用户悬停在链接上
- **THEN** 文字颜色变为悬停色 `#22D3EE`,发光效果增强

### Requirement: 首页驾驶舱特殊样式
系统SHALL为首页驾驶舱实现增强的高科技视觉效果,包括统计卡片和图表容器的特殊样式。

#### Scenario: 统计卡片样式
- **WHEN** 首页统计卡片在高科技主题下渲染
- **THEN** 系统应用以下样式:
  - 背景: 半透明磨砂玻璃效果
  - 边框: 1px 实线,带有发光效果
  - 统计数值: 大号字体,主色调,带有文字发光
  - 统计标签: 蓝灰色,中等字重

#### Scenario: 统计卡片悬停效果
- **WHEN** 用户悬停在统计卡片上
- **THEN** 系统增强视觉效果:
  - 边框发光增强
  - 整体阴影扩散
  - 轻微的缩放或位移动画 (可选)

#### Scenario: 图表容器样式
- **WHEN** 图表容器在高科技主题下渲染
- **THEN** 系统应用与卡片一致的样式
- **AND** 图表使用主色调作为主要颜色
- **AND** 图表背景透明,融入卡片背景

### Requirement: 对话框和弹窗样式
系统SHALL实现高科技风格的对话框和弹窗样式,包括边框发光和标题样式。

#### Scenario: 对话框基础样式
- **WHEN** 对话框在高科技主题下显示
- **THEN** 系统应用以下样式:
  - 背景: `#1E293B` (深石板灰)
  - 边框: 1px 实线,颜色 `#334155`
  - 阴影: `0 0 30px rgba(6, 182, 212, 0.3)` (强发光)

#### Scenario: 对话框标题样式
- **WHEN** 对话框标题在高科技主题下渲染
- **THEN** 系统应用以下样式:
  - 文字颜色: 主色调 `#06B6D4`
  - 文字阴影: `0 0 10px rgba(6, 182, 212, 0.5)` (发光效果)
  - 底部边框: 1px 实线,颜色 `#334155`

#### Scenario: 对话框内容样式
- **WHEN** 对话框内容在高科技主题下渲染
- **THEN** 文字颜色为 `#CBD5E1` (蓝灰)
- **AND** 所有表单元素应用高科技主题样式

### Requirement: 加载和骨架屏样式
系统SHALL实现高科技风格的加载动画和骨架屏样式。

#### Scenario: 加载遮罩样式
- **WHEN** 加载遮罩在高科技主题下显示
- **THEN** 系统应用以下样式:
  - 背景: `rgba(10, 14, 39, 0.8)` (半透明深色)
  - 加载图标颜色: 主色调
  - 加载图标发光: `drop-shadow(0 0 5px #06B6D4)`

#### Scenario: 骨架屏样式
- **WHEN** 骨架屏在高科技主题下显示
- **THEN** 系统应用以下样式:
  - 骨架颜色: `rgba(6, 182, 212, 0.1)`
  - 动画颜色: `rgba(6, 182, 212, 0.2)`
  - 保持脉冲动画效果

### Requirement: 浏览器兼容性降级
系统SHALL为不支持现代 CSS 特性的浏览器提供降级方案,确保基本可用性。

#### Scenario: backdrop-filter 不支持时的降级
- **WHEN** 浏览器不支持 backdrop-filter 属性
- **THEN** 系统使用纯色背景 `#1E293B` 替代磨砂玻璃效果
- **AND** 保持其他样式不变

#### Scenario: 复杂阴影效果降级
- **WHEN** 浏览器性能较差或不支持多层阴影
- **THEN** 系统简化阴影效果,使用单层阴影
- **AND** 保持基本的视觉层次

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

### Requirement: 卡片元素磨砂玻璃效果
系统SHALL为高科技主题的卡片实现磨砂玻璃效果和霓虹发光。

#### Scenario: 卡片磨砂玻璃样式
- **WHEN** `.theme-tech .el-card` 渲染
- **THEN** 系统应用:
  - `background: var(--el-bg-color-overlay)`
  - `backdrop-filter: blur(10px)`
  - `border: 1px solid var(--el-border-color)`
  - `box-shadow: var(--app-shadow)`
  - `color: var(--el-text-color-primary)`

#### Scenario: 卡片标题发光效果
- **WHEN** `.theme-tech .el-card__header` 渲染
- **THEN** 系统应用:
  - `border-bottom: 1px solid var(--el-border-color)`
  - `text-transform: uppercase`
  - `letter-spacing: 1px`
  - `text-shadow: 0 0 5px rgba(6, 182, 212, 0.5)`

### Requirement: 表格透明化与数据感
系统SHALL为高科技主题的表格实现透明背景和数据感样式。

#### Scenario: 表格透明化样式
- **WHEN** `.theme-tech .el-table` 渲染
- **THEN** 系统应用以下 CSS 变量:
  - `--el-table-bg-color: transparent`
  - `--el-table-tr-bg-color: transparent`
  - `--el-table-header-bg-color: rgba(6, 182, 212, 0.05)`
  - `--el-table-border: 1px solid var(--el-border-color)`
  - `--el-table-text-color: var(--el-text-color-regular)`
  - `--el-table-header-text-color: var(--el-color-primary)`

#### Scenario: 表头科技感字体
- **WHEN** `.theme-tech .el-table th.el-table__cell` 渲染
- **THEN** 系统应用:
  - `font-family: 'JetBrains Mono', monospace`
  - `font-weight: bold`
  - `letter-spacing: 1px`

#### Scenario: 表格行悬停高亮
- **WHEN** 用户悬停在 `.theme-tech .el-table__body tr` 上
- **THEN** 系统应用:
  - `background-color: rgba(6, 182, 212, 0.1) !important`
  - `box-shadow: inset 0 0 10px rgba(6, 182, 212, 0.2)`

### Requirement: 按钮辉光与直角设计
系统SHALL为高科技主题的按钮实现辉光效果和直角设计。

#### Scenario: 按钮基础样式
- **WHEN** `.theme-tech .el-button` 渲染
- **THEN** 系统应用:
  - `border-radius: var(--app-button-shape)` (0px)
  - `text-transform: uppercase`
  - `letter-spacing: 1px`
  - `transition: all 0.3s ease`

#### Scenario: 主按钮辉光效果
- **WHEN** `.theme-tech .el-button--primary` 渲染
- **THEN** 系统应用:
  - `box-shadow: 0 0 8px rgba(6, 182, 212, 0.4)`
  - `border: 1px solid var(--el-color-primary)`
  - `background: rgba(6, 182, 212, 0.2)` (半透明背景)

#### Scenario: 主按钮悬停增强
- **WHEN** 用户悬停在 `.theme-tech .el-button--primary` 上
- **THEN** 系统应用:
  - `background: rgba(6, 182, 212, 0.4)`
  - `box-shadow: 0 0 15px rgba(6, 182, 212, 0.6)`
  - `text-shadow: 0 0 2px #fff`

### Requirement: 输入框科技线框
系统SHALL为高科技主题的输入框实现科技感线框和聚焦发光。

#### Scenario: 输入框基础样式
- **WHEN** `.theme-tech .el-input__wrapper` 渲染
- **THEN** 系统应用:
  - `background-color: rgba(15, 23, 42, 0.6)`
  - `box-shadow: 0 0 0 1px var(--el-border-color) inset`
  - `border-radius: 0`

#### Scenario: 输入框聚焦发光
- **WHEN** `.theme-tech .el-input__wrapper.is-focus` 渲染
- **THEN** 系统应用:
  - `box-shadow: 0 0 0 1px var(--el-color-primary) inset, 0 0 10px rgba(6, 182, 212, 0.2)`

### Requirement: 标签荧光效果
系统SHALL为高科技主题的标签实现荧光边框和发光效果。

#### Scenario: 标签基础样式
- **WHEN** `.theme-tech .el-tag` 渲染
- **THEN** 系统应用:
  - `border-radius: 0`
  - `border-width: 1px`
  - `background-color: transparent`

#### Scenario: 成功标签荧光
- **WHEN** `.theme-tech .el-tag--success` 渲染
- **THEN** 系统应用:
  - `border-color: var(--el-color-success)`
  - `color: var(--el-color-success)`
  - `box-shadow: 0 0 5px rgba(74, 222, 128, 0.3)`

#### Scenario: 警告标签荧光
- **WHEN** `.theme-tech .el-tag--warning` 渲染
- **THEN** 系统应用:
  - `border-color: var(--el-color-warning)`
  - `color: var(--el-color-warning)`
  - `box-shadow: 0 0 5px rgba(250, 204, 21, 0.3)`

### Requirement: 全局过渡效果
系统SHALL为所有元素添加平滑的主题切换过渡效果。

#### Scenario: 全局过渡动画
- **WHEN** 任何元素在主题切换时渲染
- **THEN** 系统应用:
  - `transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out, border-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out`

