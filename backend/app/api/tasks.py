"""
任务管理API
"""
from flask import Blueprint, request
from app.services.task_service import TaskService
from app.utils.response import success_response, error_response, login_required, get_current_user
from app.models.task_transfer import TaskTransfer
from app.models.task_comment import TaskComment
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('', methods=['GET'])
@login_required
def get_tasks():
    """获取任务列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        filters = {
            'search': request.args.get('search', ''),
            'status': request.args.get('status', ''),
            'category': request.args.get('category', ''),
            'current_handler_id': request.args.get('current_handler_id', type=int),
            'creator_id': request.args.get('creator_id', type=int)
        }

        # 移除空值
        filters = {k: v for k, v in filters.items() if v}

        result = TaskService.list_tasks(page, per_page, **filters)
        return success_response(result)

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    """获取任务详情"""
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return error_response('任务不存在', code=404, status_code=404)

        return success_response(task.to_dict(include_details=True))

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('', methods=['POST'])
@login_required
def create_task():
    """创建任务"""
    try:
        current_user = get_current_user()
        data = request.get_json()

        title = data.get('title')
        category = data.get('category')
        description = data.get('description', '')
        current_handler_id = data.get('current_handler_id')
        expected_start_time = data.get('expected_start_time')
        expected_end_time = data.get('expected_end_time')

        if not all([title, category, current_handler_id]):
            return error_response('请提供完整信息')

        # 解析时间
        if expected_start_time:
            expected_start_time = datetime.fromisoformat(expected_start_time.replace('Z', '+00:00'))
        if expected_end_time:
            expected_end_time = datetime.fromisoformat(expected_end_time.replace('Z', '+00:00'))

        task = TaskService.create_task(
            title=title,
            category=category,
            description=description,
            creator_id=current_user.id,
            current_handler_id=current_handler_id,
            expected_start_time=expected_start_time,
            expected_end_time=expected_end_time
        )

        return success_response(task.to_dict(include_details=True), message='任务创建成功')

    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/transfer', methods=['POST'])
@login_required
def transfer_task(task_id):
    """流转任务"""
    try:
        current_user = get_current_user()
        data = request.get_json()

        target_user_id = data.get('target_user_id')
        message = data.get('message', '')

        if not target_user_id:
            return error_response('请指定流转目标用户')

        task = TaskService.transfer_task(task_id, current_user.id, target_user_id, message)

        return success_response(task.to_dict(), message='任务流转成功')

    except PermissionError as e:
        return error_response(str(e), code=403, status_code=403)
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/respond', methods=['POST'])
@login_required
def respond_task(task_id):
    """响应任务"""
    try:
        current_user = get_current_user()
        task = TaskService.respond_task(task_id, current_user.id)

        return success_response(task.to_dict(), message='任务已响应')

    except PermissionError as e:
        return error_response(str(e), code=403, status_code=403)
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_task(task_id):
    """完成任务"""
    try:
        current_user = get_current_user()
        data = request.get_json() or {}
        message = data.get('message', '')

        task = TaskService.complete_task(task_id, current_user.id, message)

        return success_response(task.to_dict(), message='任务已完成')

    except PermissionError as e:
        return error_response(str(e), code=403, status_code=403)
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/transfers', methods=['GET'])
@login_required
def get_task_transfers(task_id):
    """获取任务流转记录"""
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return error_response('任务不存在', code=404, status_code=404)

        transfers = TaskTransfer.query.filter_by(task_id=task_id).order_by(TaskTransfer.created_at.asc()).all()

        return success_response([t.to_dict() for t in transfers])

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/comments', methods=['GET'])
@login_required
def get_task_comments(task_id):
    """获取任务留言"""
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return error_response('任务不存在', code=404, status_code=404)

        comments = TaskComment.query.filter_by(task_id=task_id, is_deleted=False)\
            .order_by(TaskComment.created_at.asc()).all()

        return success_response([c.to_dict() for c in comments])

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/comments', methods=['POST'])
@login_required
def create_comment(task_id):
    """创建任务留言"""
    try:
        current_user = get_current_user()
        data = request.get_json()

        content = data.get('content')
        if not content:
            return error_response('留言内容不能为空')

        task = TaskService.get_task_by_id(task_id)
        if not task:
            return error_response('任务不存在', code=404, status_code=404)

        comment = TaskComment(
            task_id=task_id,
            user_id=current_user.id,
            content=content
        )
        comment.save()

        return success_response(comment.to_dict(), message='留言成功')

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)
