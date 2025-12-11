"""
任务服务
"""
from app import db
from app.models.task import Task
from app.models.user import User
from app.models.task_transfer import TaskTransfer
from datetime import datetime, timezone
from sqlalchemy.orm import joinedload


class TaskService:
    """任务业务逻辑服务"""

    # 任务状态常量
    STATUS_NEW = '新建'
    STATUS_PENDING = '待响应'
    STATUS_PROCESSING = '处理中'
    STATUS_SUSPENDED = '挂起'
    STATUS_COMPLETED = '已完成'
    STATUS_CLOSED = '关闭'

    # 任务分类常量
    CATEGORY_VERSION = '版本任务'
    CATEGORY_URGENT = '紧急任务'
    CATEGORY_OTHER = '其他任务'
    CATEGORY_PERIODIC = '定时周期任务'
    CATEGORY_NORMAL = '普通任务'

    @staticmethod
    def create_task(title, category, description, creator_id, current_handler_id,
                    expected_start_time=None, expected_end_time=None):
        """创建任务"""
        # 验证用户存在
        creator = User.query.get(creator_id)
        handler = User.query.get(current_handler_id)

        if not creator or not handler:
            raise ValueError("创建人或处理人不存在")

        # 验证时间
        if expected_start_time and expected_end_time:
            if expected_end_time <= expected_start_time:
                raise ValueError("期望完成时间必须大于期望开始时间")

        task = Task(
            title=title,
            category=category,
            description=description,
            creator_id=creator_id,
            current_handler_id=current_handler_id,
            expected_start_time=expected_start_time,
            expected_end_time=expected_end_time,
            status=TaskService.STATUS_NEW
        )

        db.session.add(task)
        db.session.flush()  # 获取task.id

        # 创建初始流转记录
        transfer = TaskTransfer(
            task_id=task.id,
            operator_id=creator_id,
            target_user_id=current_handler_id,
            message='任务创建',
            transfer_type='创建'
        )
        db.session.add(transfer)

        # 更新统计
        try:
            TaskService.update_statistics_on_create(task)
        except Exception as e:
            print(f'更新统计失败: {str(e)}')

        db.session.commit()

        return task

    @staticmethod
    def get_task_by_id(task_id):
        """根据ID获取任务"""
        return Task.query.get(task_id)

    @staticmethod
    def transfer_task(task_id, operator_id, target_user_id, message=''):
        """流转任务"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError("任务不存在")

        # 权限检查
        operator = User.query.get(operator_id)
        target_user = User.query.get(target_user_id)

        if not operator or not target_user:
            raise ValueError("操作人或目标用户不存在")

        if not operator.is_admin and task.current_handler_id != operator_id:
            raise PermissionError("只有当前处理人或管理员可以流转任务")

        # 保存旧状态
        old_status = task.status

        # 更新任务
        task.current_handler_id = target_user_id
        task.status = TaskService.STATUS_PENDING

        # 创建流转记录
        transfer = TaskTransfer(
            task_id=task_id,
            operator_id=operator_id,
            target_user_id=target_user_id,
            message=message,
            transfer_type='流转'
        )
        db.session.add(transfer)

        # 更新统计
        try:
            TaskService.update_statistics_on_update(old_status, task.status)
        except Exception as e:
            print(f'更新统计失败: {str(e)}')

        db.session.commit()

        return task

    @staticmethod
    def respond_task(task_id, user_id):
        """响应任务"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError("任务不存在")

        if task.current_handler_id != user_id:
            raise PermissionError("只有当前处理人可以响应任务")

        if task.status not in [TaskService.STATUS_NEW, TaskService.STATUS_PENDING, TaskService.STATUS_SUSPENDED]:
            raise ValueError(f"任务当前状态({task.status})不允许响应")

        old_status = task.status
        task.status = TaskService.STATUS_PROCESSING
        if not task.actual_start_time:
            task.actual_start_time = datetime.now(timezone.utc)

        # 创建流转记录
        transfer = TaskTransfer(
            task_id=task_id,
            operator_id=user_id,
            target_user_id=user_id,
            message='响应任务',
            transfer_type='响应'
        )
        db.session.add(transfer)

        # 更新统计
        try:
            TaskService.update_statistics_on_update(old_status, task.status)
        except Exception as e:
            print(f'更新统计失败: {str(e)}')

        db.session.commit()

        return task

    @staticmethod
    def complete_task(task_id, user_id, message=''):
        """完成任务"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError("任务不存在")

        user = User.query.get(user_id)
        if not user.is_admin and task.current_handler_id != user_id:
            raise PermissionError("只有当前处理人或管理员可以完成任务")

        old_status = task.status
        task.status = TaskService.STATUS_COMPLETED
        task.progress = 100
        task.actual_end_time = datetime.now(timezone.utc)

        transfer = TaskTransfer(
            task_id=task_id,
            operator_id=user_id,
            target_user_id=task.current_handler_id,
            message=message,
            transfer_type='完成'
        )
        db.session.add(transfer)

        # 更新统计
        try:
            TaskService.update_statistics_on_update(old_status, task.status)
        except Exception as e:
            print(f'更新统计失败: {str(e)}')

        db.session.commit()

        return task

    @staticmethod
    def suspend_task(task_id, user_id, message=''):
        """挂起任务"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError("任务不存在")

        user = User.query.get(user_id)
        if not user.is_admin and task.current_handler_id != user_id:
            raise PermissionError("只有当前处理人或管理员可以挂起任务")

        if task.status != TaskService.STATUS_PROCESSING:
            raise ValueError(f"任务当前状态({task.status})不允许挂起")

        old_status = task.status
        task.status = TaskService.STATUS_SUSPENDED

        transfer = TaskTransfer(
            task_id=task_id,
            operator_id=user_id,
            target_user_id=task.current_handler_id,
            message=message,
            transfer_type='挂起'
        )
        db.session.add(transfer)

        # 更新统计
        try:
            TaskService.update_statistics_on_update(old_status, task.status)
        except Exception as e:
            print(f'更新统计失败: {str(e)}')

        db.session.commit()

        return task

    @staticmethod
    def close_task(task_id, user_id, message=''):
        """关闭任务"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError("任务不存在")

        user = User.query.get(user_id)
        if not user.is_admin and task.current_handler_id != user_id:
            raise PermissionError("只有当前处理人或管理员可以关闭任务")

        old_status = task.status
        task.status = TaskService.STATUS_CLOSED
        if not task.actual_end_time:
            task.actual_end_time = datetime.now(timezone.utc)

        transfer = TaskTransfer(
            task_id=task_id,
            operator_id=user_id,
            target_user_id=task.current_handler_id,
            message=message,
            transfer_type='关闭'
        )
        db.session.add(transfer)

        # 更新统计
        try:
            TaskService.update_statistics_on_update(old_status, task.status)
        except Exception as e:
            print(f'更新统计失败: {str(e)}')

        db.session.commit()

        return task

    @staticmethod
    def list_tasks(page=1, per_page=20, **filters):
        """获取任务列表"""
        query = Task.query

        # 搜索
        if 'search' in filters and filters['search']:
            search_pattern = f"%{filters['search']}%"
            query = query.filter(Task.title.ilike(search_pattern))

        # 筛选
        if 'creator_id' in filters and filters['creator_id']:
            query = query.filter(Task.creator_id == filters['creator_id'])

        if 'current_handler_id' in filters and filters['current_handler_id']:
            query = query.filter(Task.current_handler_id == filters['current_handler_id'])

        if 'status' in filters and filters['status']:
            query = query.filter(Task.status == filters['status'])

        if 'category' in filters and filters['category']:
            query = query.filter(Task.category == filters['category'])

        # 排序
        query = query.order_by(Task.created_at.desc())

        total = query.count()

        # 使用 joinedload 预加载关联的 creator 和 current_handler，避免 N+1 查询问题
        tasks = query.options(
            joinedload(Task.creator),
            joinedload(Task.current_handler)
        ).offset((page - 1) * per_page).limit(per_page).all()

        return {
            'tasks': [task.to_dict() for task in tasks],
            'total': total,
            'page': page,
            'per_page': per_page
        }

    @staticmethod
    def calculate_full_statistics():
        """执行全量统计"""
        from app.models.task_statistics import TaskStatistics
        from sqlalchemy import func

        # 统计总任务数
        total_count = Task.query.count()
        TaskStatistics.set_stat('overview', 'total', {'count': total_count})

        # 统计各状态任务数
        status_stats = db.session.query(
            Task.status, func.count(Task.id)
        ).group_by(Task.status).all()

        for status, count in status_stats:
            TaskStatistics.set_stat('status_distribution', status, {'count': count})

        # 统计各分类任务数
        category_stats = db.session.query(
            Task.category, func.count(Task.id)
        ).group_by(Task.category).all()

        for category, count in category_stats:
            TaskStatistics.set_stat('category_distribution', category, {'count': count})

        db.session.commit()

    @staticmethod
    def update_statistics_on_create(task):
        """任务创建时增量更新统计"""
        from app.models.task_statistics import TaskStatistics

        # 更新总数
        total_stat = TaskStatistics.get_stat('overview', 'total') or {'count': 0}
        total_stat['count'] += 1
        TaskStatistics.set_stat('overview', 'total', total_stat)

        # 更新状态统计
        status_stat = TaskStatistics.get_stat('status_distribution', task.status) or {'count': 0}
        status_stat['count'] += 1
        TaskStatistics.set_stat('status_distribution', task.status, status_stat)

        # 更新分类统计
        category_stat = TaskStatistics.get_stat('category_distribution', task.category) or {'count': 0}
        category_stat['count'] += 1
        TaskStatistics.set_stat('category_distribution', task.category, category_stat)

    @staticmethod
    def update_statistics_on_update(old_status, new_status):
        """任务状态更新时增量更新统计"""
        from app.models.task_statistics import TaskStatistics

        if old_status != new_status:
            # 旧状态-1
            old_stat = TaskStatistics.get_stat('status_distribution', old_status) or {'count': 0}
            old_stat['count'] = max(0, old_stat['count'] - 1)
            TaskStatistics.set_stat('status_distribution', old_status, old_stat)

            # 新状态+1
            new_stat = TaskStatistics.get_stat('status_distribution', new_status) or {'count': 0}
            new_stat['count'] += 1
            TaskStatistics.set_stat('status_distribution', new_status, new_stat)

    @staticmethod
    def update_statistics_on_delete(task):
        """任务删除时增量更新统计"""
        from app.models.task_statistics import TaskStatistics

        # 更新总数
        total_stat = TaskStatistics.get_stat('overview', 'total') or {'count': 0}
        total_stat['count'] = max(0, total_stat['count'] - 1)
        TaskStatistics.set_stat('overview', 'total', total_stat)

        # 更新状态统计
        status_stat = TaskStatistics.get_stat('status_distribution', task.status) or {'count': 0}
        status_stat['count'] = max(0, status_stat['count'] - 1)
        TaskStatistics.set_stat('status_distribution', task.status, status_stat)

        # 更新分类统计
        category_stat = TaskStatistics.get_stat('category_distribution', task.category) or {'count': 0}
        category_stat['count'] = max(0, category_stat['count'] - 1)
        TaskStatistics.set_stat('category_distribution', task.category, category_stat)

    @staticmethod
    def get_statistics_from_cache():
        """从统计表读取数据"""
        from app.models.task_statistics import TaskStatistics

        # 获取总数
        total_stat = TaskStatistics.get_stat('overview', 'total') or {'count': 0}

        # 获取各状态统计
        statuses = [TaskService.STATUS_NEW, TaskService.STATUS_PENDING, TaskService.STATUS_PROCESSING,
                   TaskService.STATUS_SUSPENDED, TaskService.STATUS_COMPLETED, TaskService.STATUS_CLOSED]
        status_stats = {}
        for status in statuses:
            stat = TaskStatistics.get_stat('status_distribution', status) or {'count': 0}
            status_stats[status] = stat['count']

        # 获取各分类统计
        categories = [TaskService.CATEGORY_VERSION, TaskService.CATEGORY_URGENT, TaskService.CATEGORY_NORMAL,
                     TaskService.CATEGORY_PERIODIC, TaskService.CATEGORY_OTHER]
        category_stats = {}
        for category in categories:
            stat = TaskStatistics.get_stat('category_distribution', category) or {'count': 0}
            category_stats[category] = stat['count']

        # 获取最后更新时间
        from app.models.task_statistics import TaskStatistics as TSModel
        last_update = TSModel.query.order_by(TSModel.updated_at.desc()).first()
        updated_at = last_update.updated_at.isoformat() if last_update else None

        return {
            'total': total_stat['count'],
            'status_distribution': status_stats,
            'category_distribution': category_stats,
            'updated_at': updated_at
        }

    @staticmethod
    def get_my_pending_tasks(user_id, limit=10):
        """获取用户待办任务"""
        tasks = Task.query.filter(
            Task.current_handler_id == user_id,
            Task.status.in_([TaskService.STATUS_PENDING, TaskService.STATUS_PROCESSING])
        ).options(
            joinedload(Task.creator),
            joinedload(Task.current_handler)
        ).order_by(Task.created_at.desc()).limit(limit).all()

        return [task.to_dict() for task in tasks]

    @staticmethod
    def get_urgent_tasks(hours=24):
        """获取紧急任务列表"""
        from datetime import timedelta

        now = datetime.now(timezone.utc)
        threshold = now + timedelta(hours=hours)

        # 查询即将到期或已逾期的任务
        tasks = Task.query.filter(
            Task.expected_end_time.isnot(None),
            Task.expected_end_time <= threshold,
            Task.status.in_([TaskService.STATUS_NEW, TaskService.STATUS_PENDING,
                           TaskService.STATUS_PROCESSING, TaskService.STATUS_SUSPENDED])
        ).options(
            joinedload(Task.creator),
            joinedload(Task.current_handler)
        ).order_by(Task.expected_end_time.asc()).all()

        # 添加紧急程度标识
        result = []
        for task in tasks:
            task_dict = task.to_dict()
            # 确保时间对象带时区信息
            end_time = task.expected_end_time.replace(tzinfo=timezone.utc) if task.expected_end_time.tzinfo is None else task.expected_end_time
            if end_time < now:
                task_dict['urgency'] = 'overdue'
                task_dict['overdue_days'] = (now - end_time).days
            else:
                task_dict['urgency'] = 'upcoming'
                task_dict['remaining_hours'] = int((end_time - now).total_seconds() / 3600)
            result.append(task_dict)

        return result
