# Change: 修复高科技主题下拉框白色背景问题

## Why
当前高科技主题下，任务列表界面的下拉框（el-select）底色显示为白色，与深色主题整体风格不协调。需要根据 gemini-style-v2.txt 规范调整下拉框及相关表单组件的样式，使其与高科技主题保持一致。

## What Changes
- 修复 el-select 组件在高科技主题下的背景色问题
- 完善 el-select-dropdown 弹出层的深色样式
- 统一 el-date-picker 日期选择器的高科技主题样式
- 补充 el-form-item 表单项标签的样式
- 增强分页组件的高科技主题样式

## Impact
- Affected specs: ui-theme-styling
- Affected code: `frontend/src/assets/styles/themes.scss`
