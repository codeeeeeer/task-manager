"""
定时任务调度服务
"""
from app import scheduler
from app.models.task import Task
from datetime import datetime


class SchedulerService:
    """定时任务业务逻辑服务"""

    @staticmethod
    def update_all_time_progress():
        """
        更新所有处理中任务的时间进度
        """
        from app import db, create_app
        from app.services.task_service import TaskService

        app = create_app()
        with app.app_context():
            print(f'[{datetime.now()}] 开始更新时间进度')

            tasks = Task.query.filter(
                Task.status.in_([TaskService.STATUS_PROCESSING]),
                Task.expected_start_time.isnot(None),
                Task.expected_end_time.isnot(None)
            ).all()

            for task in tasks:
                try:
                    task.time_progress = task.calculate_time_progress()
                except Exception as e:
                    print(f'更新时间进度失败 task_id={task.id}: {str(e)}')

            db.session.commit()
            print(f'[{datetime.now()}] 时间进度更新完成，共更新 {len(tasks)} 个任务')

    @staticmethod
    def check_task_warnings():
        """
        检查任务预警
        检查所有"处理中"状态的任务，如果时间进度超过阈值但处理进度不足，发送预警
        """
        from app import db, create_app
        from app.services.task_service import TaskService

        app = create_app()
        with app.app_context():
            print(f'[{datetime.now()}] 开始检查任务预警')

            # 查询处理中的任务
            processing_tasks = Task.query.filter(
                Task.status == TaskService.STATUS_PROCESSING,
                Task.expected_start_time.isnot(None),
                Task.expected_end_time.isnot(None)
            ).all()

            warning_count = 0
            for task in processing_tasks:
                try:
                    # 更新时间进度
                    time_progress = task.calculate_time_progress()
                    task.time_progress = time_progress
                    db.session.commit()

                    # 检查预警条件
                    warning_level = SchedulerService._check_warning_level(task)
                    if warning_level:
                        # TODO: 发送预警通知
                        print(f'任务预警: {task.title} - {warning_level}%剩余时间，当前进度{task.progress}%')
                        warning_count += 1

                except Exception as e:
                    print(f'检查任务预警失败 task_id={task.id}: {str(e)}')
                    db.session.rollback()

            print(f'[{datetime.now()}] 任务预警检查完成，发现 {warning_count} 个预警')

    @staticmethod
    def _check_warning_level(task):
        """
        检查预警级别
        :return: 20, 10, 5 或 None
        """
        time_progress = task.time_progress
        progress = task.progress

        # 时间进度95%，但处理进度<95%
        if time_progress >= 95 and progress < 95:
            return 5

        # 时间进度90%，但处理进度<90%
        if time_progress >= 90 and progress < 90:
            return 10

        # 时间进度80%，但处理进度<80%
        if time_progress >= 80 and progress < 80:
            return 20

        return None

    @staticmethod
    def reset_periodic_tasks():
        """
        重置周期任务
        检查所有"定时周期任务"类型的任务，如果已完成或关闭，根据周期重置
        """
        from app import db, create_app
        from app.services.task_service import TaskService
        from datetime import timedelta

        app = create_app()
        with app.app_context():
            print(f'[{datetime.now()}] 开始重置周期任务')

            # 查询所有定时周期任务
            periodic_tasks = Task.query.filter(
                Task.category == TaskService.CATEGORY_PERIODIC,
                Task.status.in_([TaskService.STATUS_COMPLETED, TaskService.STATUS_CLOSED])
            ).all()

            reset_count = 0
            for task in periodic_tasks:
                try:
                    # 检查是否到达周期时间点
                    if SchedulerService._should_reset_task(task):
                        # 重置任务状态
                        task.status = TaskService.STATUS_NEW
                        task.progress = 0
                        task.time_progress = 0
                        task.actual_start_time = None
                        task.actual_end_time = None

                        # 更新期望时间(简单示例：7天周期)
                        task.expected_start_time = datetime.now()
                        task.expected_end_time = datetime.now() + timedelta(days=7)

                        db.session.commit()

                        # TODO: 发送通知
                        print(f'周期任务已重置: {task.title}')
                        reset_count += 1

                except Exception as e:
                    print(f'重置任务失败 task_id={task.id}: {str(e)}')
                    db.session.rollback()

            print(f'[{datetime.now()}] 周期任务重置完成，共重置 {reset_count} 个任务')

    @staticmethod
    def _should_reset_task(task):
        """
        判断任务是否需要重置
        简化处理：如果任务完成后超过7天，则重置
        """
        if not task.actual_end_time:
            return False

        days_since_completion = (datetime.now() - task.actual_end_time).days
        return days_since_completion >= 7


    @staticmethod
    def calculate_task_statistics():
        """计算任务统计数据"""
        from app import create_app
        from app.services.task_service import TaskService

        app = create_app()
        with app.app_context():
            print(f'[{datetime.now()}] 开始计算任务统计')
            try:
                TaskService.calculate_full_statistics()
                print(f'[{datetime.now()}] 任务统计计算完成')
            except Exception as e:
                print(f'计算任务统计失败: {str(e)}')


def init_scheduler():
    """初始化定时任务"""

    # 1. 更新时间进度 - 每30分钟执行一次
    scheduler.add_job(
        func=SchedulerService.update_all_time_progress,
        trigger='interval',
        minutes=30,
        id='update_time_progress',
        replace_existing=True
    )

    # 2. 任务预警检测 - 每小时执行一次
    scheduler.add_job(
        func=SchedulerService.check_task_warnings,
        trigger='interval',
        hours=1,
        id='check_task_warnings',
        replace_existing=True
    )

    # 3. 周期任务重置 - 每天凌晨2点执行
    scheduler.add_job(
        func=SchedulerService.reset_periodic_tasks,
        trigger='cron',
        hour=2,
        minute=0,
        id='reset_periodic_tasks',
        replace_existing=True
    )

    # 4. 任务统计计算 - 每5分钟执行一次
    scheduler.add_job(
        func=SchedulerService.calculate_task_statistics,
        trigger='interval',
        minutes=5,
        id='calculate_task_statistics',
        replace_existing=True
    )

    # 启动调度器
    if not scheduler.running:
        scheduler.start()
        print('定时任务调度器已启动')
