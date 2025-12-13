# ui-theme-styling Spec Delta

## MODIFIED Requirements

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

## ADDED Requirements

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
