# Implementation Tasks

## 1. 数据库迁移
- [x] 1.1 创建数据库迁移文件，定义 `task_statistics` 表结构
- [x] 1.2 添加字段：id, stat_type, stat_key, stat_value (JSON/TEXT), updated_at
- [x] 1.3 创建唯一索引：`(stat_type, stat_key)`
- [x] 1.4 执行迁移，创建统计表
- [x] 1.5 编写初始化脚本，填充初始统计数据

## 2. 统计数据模型
- [x] 2.1 在 `backend/app/models/` 中创建 `task_statistics.py`，定义 TaskStatistics 模型
- [x] 2.2 实现模型方法：`get_stat(stat_type, stat_key)`, `set_stat(stat_type, stat_key, value)`
- [x] 2.3 实现 JSON 序列化和反序列化方法

## 3. 统计服务层
- [x] 3.1 在 `backend/app/services/task_service.py` 中添加 `calculate_full_statistics()` 方法，执行全量统计
- [x] 3.2 添加 `update_statistics_on_create(task)` 方法，任务创建时增量更新统计
- [x] 3.3 添加 `update_statistics_on_update(old_task, new_task)` 方法，任务更新时增量更新统计
- [x] 3.4 添加 `update_statistics_on_delete(task)` 方法，任务删除时增量更新统计
- [x] 3.5 添加 `get_statistics_from_cache()` 方法，从统计表读取数据
- [x] 3.6 添加 `get_my_pending_tasks(user_id, limit=10)` 方法，实时查询用户待办任务
- [x] 3.7 添加 `get_urgent_tasks(hours=24)` 方法，实时查询紧急任务列表

## 4. 定时任务
- [x] 4.1 在 `backend/app/services/scheduler_service.py` 中添加 `schedule_statistics_job()` 方法
- [x] 4.2 配置定时任务，每5分钟执行一次 `calculate_full_statistics()`
- [x] 4.3 添加错误处理和日志记录
- [x] 4.4 在应用启动时注册定时任务

## 5. 任务变更钩子
- [x] 5.1 在 `backend/app/api/tasks.py` 的 `create_task()` 中调用 `update_statistics_on_create()`
- [x] 5.2 在 `update_task()` 中调用 `update_statistics_on_update()`
- [x] 5.3 在任务删除接口中调用 `update_statistics_on_delete()`
- [x] 5.4 确保统计更新在同一数据库事务中执行

## 6. 后端API开发
- [x] 6.1 在 `backend/app/api/tasks.py` 中添加 `GET /api/tasks/statistics` 接口，调用 `get_statistics_from_cache()`
- [x] 6.2 添加 `GET /api/tasks/my-pending` 接口，调用 `get_my_pending_tasks()`
- [x] 6.3 添加 `GET /api/tasks/urgent` 接口，调用 `get_urgent_tasks()`
- [x] 6.4 确保所有新接口都使用 `@login_required` 装饰器进行权限控制

## 7. 前端API集成
- [x] 7.1 在 `frontend/src/api/task.js` 中添加 `getTaskStatistics()` 方法
- [x] 7.2 在 `frontend/src/api/task.js` 中添加 `getMyPendingTasks()` 方法
- [x] 7.3 在 `frontend/src/api/task.js` 中添加 `getUrgentTasks()` 方法

## 8. 前端首页组件开发
- [x] 8.1 重构 `frontend/src/views/Home.vue`，添加驾驶舱布局结构
- [x] 8.2 创建任务统计概览卡片组件，展示总任务数、待响应、处理中、已完成数量
- [x] 8.3 集成图表库（如 ECharts 或 Chart.js），创建任务状态分布图表组件
- [x] 8.4 创建任务分类分布统计组件
- [x] 8.5 创建我的待办任务列表组件，支持点击跳转到任务详情
- [x] 8.6 创建紧急任务提醒组件，使用颜色标识（红色=已逾期，橙色=即将到期）
- [x] 8.7 实现图表交互功能，点击状态跳转到任务列表页面并自动筛选

## 9. 实时更新集成
- [x] 9.1 在 `frontend/src/views/Home.vue` 中监听 SocketIO 任务变更事件
- [x] 9.2 当收到任务状态变更通知时，自动刷新统计数据

## 10. 样式和用户体验优化
- [x] 10.1 使用 Element Plus 卡片组件和栅格布局，确保响应式设计
- [x] 10.2 添加数据加载状态（loading）和空状态提示
- [x] 10.3 优化颜色方案，确保与现有高科技风格一致
- [x] 10.4 添加骨架屏或加载动画，提升用户体验

## 11. 测试和验证
- [x] 11.1 测试统计表的数据一致性，验证增量更新和全量统计的准确性
- [x] 11.2 测试定时任务是否正常执行，查看日志确认每5分钟触发一次
- [x] 11.3 测试后端API接口，验证统计数据准确性和性能（响应时间<100ms）
- [x] 11.4 测试前端页面在不同屏幕尺寸下的显示效果
- [x] 11.5 测试实时更新功能，验证WebSocket推送是否正常工作
- [x] 11.6 测试权限控制，确保未登录用户无法访问统计API
- [x] 11.7 测试边界情况（无任务、大量任务、网络错误、统计表为空等）
- [x] 11.8 性能测试：模拟大量任务数据，验证统计查询性能
