# ui-default-theme-styling Spec Delta

## MODIFIED Requirements

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

## ADDED Requirements

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
