## ADDED Requirements

### Requirement: 默认按钮高科技样式
系统SHALL为高科技主题的默认按钮（el-button--default）实现深色背景和霓虹边框效果。

#### Scenario: 默认按钮基础样式
- **WHEN** `.theme-tech .el-button--default` 渲染
- **THEN** 系统应用:
  - `background-color: rgba(15, 23, 42, 0.6)` (半透明深色)
  - `border: 1px solid var(--el-border-color)` (低透明度青色边框)
  - `color: var(--el-text-color-primary)` (发光白)

#### Scenario: 默认按钮悬停效果
- **WHEN** 用户悬停在 `.theme-tech .el-button--default` 上
- **THEN** 系统应用:
  - `border-color: var(--el-color-primary)` (霓虹青边框)
  - `color: var(--el-color-primary)` (霓虹青文字)
  - `box-shadow: 0 0 8px rgba(6, 182, 212, 0.4)` (发光效果)

## MODIFIED Requirements

### Requirement: 输入框元素样式
系统SHALL实现高科技风格的输入框样式,包括背景、边框和聚焦状态的光影效果。

#### Scenario: 输入框基础样式
- **WHEN** 输入框在高科技主题下渲染
- **THEN** 系统应用以下样式:
  - 背景色: `rgba(15, 23, 42, 0.6)` (半透明深色)
  - 边框: 1px 实线,颜色 `var(--el-border-color)` (低透明度青色)
  - 文字颜色: `var(--el-text-color-regular)` (蓝灰)
  - 阴影: `0 0 0 1px var(--el-border-color) inset`

#### Scenario: 输入框聚焦效果
- **WHEN** 用户聚焦在输入框上
- **THEN** 系统应用聚焦效果:
  - 边框颜色变为主色调 `var(--el-color-primary)`
  - 阴影增强为 `0 0 0 1px var(--el-color-primary) inset, 0 0 10px rgba(6, 182, 212, 0.2)` (扩散光影)

#### Scenario: 下拉框和选择器样式
- **WHEN** 下拉框或选择器在高科技主题下渲染
- **THEN** 系统应用深色背景样式，使用增强的 CSS 选择器确保覆盖默认样式:
  - 背景色: `rgba(15, 23, 42, 0.6) !important` (半透明深色)
  - 边框: `0 0 0 1px var(--el-border-color) inset !important`
  - 圆角: 0 (直角)
- **AND** 选择器需要同时覆盖 `.el-select .el-input .el-input__wrapper` 路径

#### Scenario: 下拉选项样式
- **WHEN** 下拉选项在高科技主题下渲染
- **THEN** 系统应用以下样式:
  - 文字颜色: `var(--el-text-color-regular)` (蓝灰)
- **WHEN** 用户悬停在下拉选项上
- **THEN** 背景色变为 `rgba(6, 182, 212, 0.1)` (低透明度青色)
- **WHEN** 下拉选项被选中
- **THEN** 系统应用:
  - 背景色: `rgba(6, 182, 212, 0.2)` (半透明青色)
  - 文字颜色: `var(--el-color-primary)` (霓虹青)
