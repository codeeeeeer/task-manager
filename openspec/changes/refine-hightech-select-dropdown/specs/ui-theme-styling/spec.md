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
- **THEN** 系统应用与输入框一致的样式:
  - 背景色: `rgba(15, 23, 42, 0.6)` (半透明深色)
  - 边框: `0 0 0 1px var(--el-border-color) inset`
  - 圆角: 0 (直角)
- **WHEN** 下拉菜单展开
- **THEN** 下拉菜单应用以下样式:
  - 背景: `#1a1f3a` (深蓝灰)
  - 边框: `1px solid rgba(6, 182, 212, 0.3)` (低透明度青色)
  - 阴影: `0 0 15px rgba(6, 182, 212, 0.3)` (霓虹光晕)

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

## ADDED Requirements

### Requirement: 日期选择器高科技样式
系统SHALL为高科技主题的日期选择器实现深色背景和霓虹发光效果。

#### Scenario: 日期选择器输入框样式
- **WHEN** 日期选择器在高科技主题下渲染
- **THEN** 系统应用与输入框一致的样式:
  - 背景色: `rgba(15, 23, 42, 0.6)`
  - 边框: `0 0 0 1px var(--el-border-color) inset`
  - 圆角: 0

#### Scenario: 日期选择器弹出面板样式
- **WHEN** 日期选择器弹出面板在高科技主题下显示
- **THEN** 系统应用以下样式:
  - 背景: `#1a1f3a` (深蓝灰)
  - 边框: `1px solid rgba(6, 182, 212, 0.3)`
  - 阴影: `0 0 15px rgba(6, 182, 212, 0.3)`

#### Scenario: 日期选择器表头样式
- **WHEN** 日期选择器表头在高科技主题下渲染
- **THEN** 系统应用:
  - 文字颜色: `var(--el-color-primary)` (霓虹青)
  - 按钮颜色: `var(--el-text-color-regular)`

#### Scenario: 日期单元格样式
- **WHEN** 日期单元格在高科技主题下渲染
- **THEN** 系统应用:
  - 文字颜色: `var(--el-text-color-regular)` (蓝灰)
- **WHEN** 用户悬停在日期单元格上
- **THEN** 背景色变为 `rgba(6, 182, 212, 0.1)`
- **WHEN** 日期单元格被选中
- **THEN** 系统应用:
  - 背景色: `var(--el-color-primary)` (霓虹青)
  - 文字颜色: `#fff`
  - 阴影: `0 0 10px rgba(6, 182, 212, 0.5)`

### Requirement: 分页组件高科技样式增强
系统SHALL为高科技主题的分页组件实现完整的深色样式和霓虹效果。

#### Scenario: 分页按钮和页码样式
- **WHEN** 分页组件在高科技主题下渲染
- **THEN** 系统应用以下样式:
  - 背景色: `rgba(15, 23, 42, 0.6)` (半透明深色)
  - 边框: `1px solid var(--el-border-color)`
  - 文字颜色: `var(--el-text-color-primary)` (发光白)

#### Scenario: 分页悬停效果
- **WHEN** 用户悬停在分页按钮或页码上
- **THEN** 系统应用:
  - 文字颜色: `var(--el-color-primary)` (霓虹青)
  - 边框颜色: `var(--el-color-primary)`
  - 阴影: `0 0 5px rgba(6, 182, 212, 0.5)`

#### Scenario: 分页激活状态
- **WHEN** 页码处于激活状态
- **THEN** 系统应用:
  - 文字颜色: `var(--el-color-primary)` (霓虹青)
  - 边框颜色: `var(--el-color-primary)`
  - 阴影: `0 0 10px rgba(6, 182, 212, 0.5)`

#### Scenario: 分页输入框和下拉框样式
- **WHEN** 分页组件的输入框或下拉框在高科技主题下渲染
- **THEN** 系统应用与全局输入框一致的深色样式
