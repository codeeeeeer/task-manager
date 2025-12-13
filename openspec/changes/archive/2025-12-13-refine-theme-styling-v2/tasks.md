# Tasks: refine-theme-styling-v2

## Implementation Tasks

### 1. 更新 CSS 变量定义
**File:** `frontend/src/assets/styles/themes.scss`

更新 `:root` 和 `html.theme-tech` 中的 CSS 变量定义，使其完全符合 gemini-style-v2.txt 规范：
- 更新默认主题的颜色变量（primary, success, warning, danger, info）
- 更新背景色系统（bg-color, bg-color-overlay, bg-color-page）
- 更新文字颜色系统（text-color-primary, regular, secondary）
- 更新边框颜色系统
- 添加自定义业务变量（card-radius, shadow, font-family, button-shape）
- 更新高科技主题的所有变量覆盖

**验证:** 检查浏览器开发者工具中的 CSS 变量是否正确定义

### 2. 实现默认主题的 Element Plus 组件样式
**File:** `frontend/src/assets/styles/themes.scss`

为默认主题添加或更新 Element Plus 组件的样式覆盖：
- 卡片组件（.el-card）：圆角、阴影、背景
- 按钮组件（.el-button）：圆角、颜色��悬停效果
- 输入框组件（.el-input__wrapper）：边框、聚焦光晕
- 表格组件（.el-table）：表头、行样式、悬停效果
- 其他组件（.el-tag, .el-dialog, .el-select 等）

**验证:** 在默认主题下浏览各个页面，确认组件样式符合规范

### 3. 实现高科技主题的特殊效果
**File:** `frontend/src/assets/styles/themes.scss`

在 `.theme-tech` 选择器下实现高科技主题的特殊样式：
- 卡片磨砂玻璃效果（backdrop-filter: blur(10px)）
- 卡片标题发光效果（text-shadow）
- 表格透明化和数据感样式
- 表头科技感字体（JetBrains Mono）
- 表格行悬停高亮和内阴影
- 按钮辉光效果和直角设计
- 输入框科技线框和聚焦发光
- 标签荧光边框效果

**验证:** 在高科技主题下浏览各个页面，确认特殊效果正常显示

### 4. 添加全局字体和过渡效果
**File:** `frontend/src/assets/styles/themes.scss`

实现全局样式优化：
- 为 body 元素应用 `font-family: var(--app-font-family)`
- 为所有元素添加平滑过渡效果（background-color, color, border-color, box-shadow）
- 确保过渡时间为 0.3s，使用 ease-in-out 函数

**验证:** 切换主题时观察过渡效果是否平滑，无闪烁

### 5. 测试主题切换功能
**Files:** 所有前端页面

全面测试主题切换功能：
- 在首页驾驶舱测试统计卡片和图表的显示
- 在任务列表页测试表格和按钮的显示
- 在任务详情页测试卡片、输入框、标签的显示
- 在对话框和弹窗中测试样式
- 测试主题切换的性能（应在 500ms 内完成）
- 测试 localStorage 持久化功能

**验证:** 所有页面在两个主题下都显示正常，无样式错误

### 6. 浏览器兼容性测试
**Files:** 所有前端页面

测试不同浏览器的兼容性：
- 测试 backdrop-filter 在不支持的浏览器中的降级方案
- 测试复杂阴影效果在低性能设备上的表现
- 确保基本可用性在所有目标浏览器中都能保证

**验证:** 在 Chrome, Firefox, Safari, Edge 中测试，确认兼容性

## Dependencies
- 任务 2-3 依赖任务 1（CSS 变量必须先定义）
- 任务 4 可以与任务 2-3 并行
- 任务 5 依赖任务 1-4 全部完成
- 任务 6 依赖任务 5 完成

## Validation Criteria
- [x] 所有 CSS 变量正确定义并符合 gemini-style-v2.txt 规范
- [x] 默认主题的所有组件样式符合明亮简约风格
- [x] 高科技主题的所有组件样式符合赛博风格，特殊效果正常显示
- [x] 主题切换平滑无闪烁，性能良好
- [x] 所有页面在两个主题下都显示正常
- [x] 浏览器兼容性良好，有合理的降级方案
