# Proposal: refine-theme-styling-v2

## Overview
根据 gemini-style-v2.txt 规范，调整前端界面的两个主题风格：
- **默认主题**：参考明亮简约风格（Light / Enterprise）
- **高科技主题**：参考高科技赛博风格（Tech / Cyberpunk）

## Motivation
当前的主题实现已经具备基本的样式系统，但需要进一步优化以符合 gemini-style-v2.txt 中定义的详细规范，包括：
1. 更精确的 CSS 变量定义和命名规范
2. Element Plus 组件的深度定制
3. 高科技主题的特殊效果（磨砂玻璃、发光、切角等）
4. 更好的字体系统和视觉层次

## Scope
此变更将更新以下内容：
- 更新 `frontend/src/assets/styles/themes.scss` 中的 CSS 变量定义
- 增强 Element Plus 组件的主题覆盖样式
- 优化主题切换的平滑过渡效果
- 确保所有 UI 组件符合两套主题的设计规范

## Out of Scope
- 不涉及主题切换机制的重构（Pinia store 保持不变）
- 不添加新的主题选项（仅优化现有的 light 和 tech 两个主题）
- 不修改组件的功能逻辑

## Affected Specs
- `ui-default-theme-styling` - 更新默认主题的样式规范
- `ui-theme-styling` - 更新高科技主题的样式规范

## Dependencies
无外部依赖变更，使用现有的 Vue 3 + Element Plus 技术栈。

## Risks
- 样式变更可能影响现有页面的视觉呈现，需要全面测试
- 高科技主题的特殊效果（如 backdrop-filter）在旧浏览器中可能需要降级方案
