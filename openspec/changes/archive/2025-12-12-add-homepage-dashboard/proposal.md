# Change: 添加首页任务概览驾驶舱

## Why
当前首页仅显示欢迎信息，用户需要进入任务列表页面才能了解任务整体情况。添加驾驶舱可以让用户在首页快速了解关键任务指标和状态分布，提升工作效率和决策能力。

## What Changes
- 在首页添加任务统计概览卡片，展示关键指标（总任务数、待响应任务数、处理中任务数、已完成任务数）
- 添加任务状态分布图表（饼图或柱状图）
- 添加任务分类分布统计
- 添加我的待办任务列表（当前用户作为处理人的待响应和处理中任务）
- 添加紧急任务提醒（即将到期或已逾期的任务）
- 后端新增统计数据API接口

## Impact
- Affected specs: task-dashboard (新增)
- Affected code:
  - 后端: `backend/app/api/tasks.py` (新增统计接口)
  - 后端: `backend/app/services/task_service.py` (新增统计服务方法)
  - 前端: `frontend/src/views/Home.vue` (重构首页组件)
  - 前端: `frontend/src/api/task.js` (新增统计API调用)
