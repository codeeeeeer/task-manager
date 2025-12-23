# Change: 修复高科技主题下拉框和默认按钮白色背景

## Why
根据截图反馈，高科技主题下：
1. 下拉框（el-select）仍显示白色背景，与深色主题不协调
2. "重置"按钮（el-button--default）显示白色背景，与其他按钮风格不一致

需要增强 CSS 选择器优先级，确保样式正确覆盖 Element Plus 默认样式。

## What Changes
- 增强 el-select 组件的 CSS 选择器优先级，确保深色背景生效
- 添加 el-button--default 默认按钮的高科技主题样式

## Impact
- Affected specs: ui-theme-styling
- Affected code: `frontend/src/assets/styles/themes.scss`
