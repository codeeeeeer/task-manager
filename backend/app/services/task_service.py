"""
任务服务
"""
from app import db
from app.models.task import Task
from app.models.user import User
from app.models.task_transfer import TaskTransfer
from datetime import datetime, timezone


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

        task.status = TaskService.STATUS_SUSPENDED

        transfer = TaskTransfer(
            task_id=task_id,
            operator_id=user_id,
            target_user_id=task.current_handler_id,
            message=message,
            transfer_type='挂起'
        )
        db.session.add(transfer)
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
        tasks = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            'tasks': [task.to_dict() for task in tasks],
            'total': total,
            'page': page,
            'per_page': per_page
        }
