"""
任务管理API
"""
from flask import Blueprint, request, send_file
from app.services.task_service import TaskService
from app.utils.response import success_response, error_response, login_required, get_current_user
from app.models.task_transfer import TaskTransfer
from app.models.task_comment import TaskComment
from app.models.task_attachment import TaskAttachment
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from app import db

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


@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """更新任务"""
    try:
        current_user = get_current_user()
        task = TaskService.get_task_by_id(task_id)

        if not task:
            return error_response('任务不存在', code=404, status_code=404)

        if not current_user.is_admin and task.current_handler_id != current_user.id:
            return error_response('只有当前处理人或管理员可以编辑任务', code=403, status_code=403)

        data = request.get_json()
        if 'description' in data:
            task.description = data['description']
        if 'progress' in data:
            task.progress = data['progress']

        from app import db
        db.session.commit()

        return success_response(task.to_dict(include_details=True), message='任务更新成功')

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


@tasks_bp.route('/<int:task_id>/respond-by-umcode', methods=['POST'])
def respond_task_by_umcode(task_id):
    """响应任务（供Chrome插件使用）"""
    try:
        from app.services.user_service import UserService
        um_code = request.args.get('um_code')
        if not um_code:
            return error_response('缺少um_code参数')

        user = UserService.get_user_by_um_code(um_code)
        if not user:
            return error_response('用户不存在', code=404, status_code=404)

        task = TaskService.respond_task(task_id, user.id)

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


@tasks_bp.route('/<int:task_id>/suspend', methods=['POST'])
@login_required
def suspend_task(task_id):
    """挂起任务"""
    try:
        current_user = get_current_user()
        data = request.get_json() or {}
        message = data.get('message', '')

        task = TaskService.suspend_task(task_id, current_user.id, message)

        return success_response(task.to_dict(), message='任务已挂起')

    except PermissionError as e:
        return error_response(str(e), code=403, status_code=403)
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/close', methods=['POST'])
@login_required
def close_task(task_id):
    """关闭任务"""
    try:
        current_user = get_current_user()
        data = request.get_json() or {}
        message = data.get('message', '')

        task = TaskService.close_task(task_id, current_user.id, message)

        return success_response(task.to_dict(), message='任务已关闭')

    except PermissionError as e:
        return error_response(str(e), code=403, status_code=403)
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/attachments', methods=['GET'])
@login_required
def get_attachments(task_id):
    """获取任务附件列表"""
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return error_response('任务不存在', code=404, status_code=404)

        attachments = TaskAttachment.query.filter_by(task_id=task_id).order_by(TaskAttachment.created_at.desc()).all()
        return success_response([a.to_dict() for a in attachments])

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/attachments', methods=['POST'])
@login_required
def upload_attachment(task_id):
    """上传任务附件"""
    try:
        current_user = get_current_user()
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return error_response('任务不存在', code=404, status_code=404)

        if 'file' not in request.files:
            return error_response('没有上传文件')

        file = request.files['file']
        if file.filename == '':
            return error_response('文件名为空')

        original_filename = file.filename
        import uuid
        safe_filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        upload_dir = os.path.join('uploads', 'tasks', str(task_id))
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, safe_filename)
        file.save(file_path)

        file_size = os.path.getsize(file_path)
        file_type = os.path.splitext(original_filename)[1]

        attachment = TaskAttachment(
            task_id=task_id,
            file_name=original_filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            uploaded_by=current_user.id
        )
        attachment.save()

        return success_response(attachment.to_dict(), message='文件上传成功')

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/attachments/<int:attachment_id>', methods=['DELETE'])
@login_required
def delete_attachment(task_id, attachment_id):
    """删除任务附件"""
    try:
        current_user = get_current_user()
        attachment = TaskAttachment.query.get(attachment_id)

        if not attachment or attachment.task_id != task_id:
            return error_response('附件不存在', code=404, status_code=404)

        task = TaskService.get_task_by_id(task_id)
        if not current_user.is_admin and task.current_handler_id != current_user.id:
            return error_response('只有当前处理人或管理员可以删除附件', code=403, status_code=403)

        if os.path.exists(attachment.file_path):
            os.remove(attachment.file_path)

        db.session.delete(attachment)
        db.session.commit()

        return success_response(message='附件删除成功')

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/<int:task_id>/attachments/<int:attachment_id>/download', methods=['GET'])
@login_required
def download_attachment(task_id, attachment_id):
    """下载任务附件"""
    try:
        attachment = TaskAttachment.query.get(attachment_id)

        if not attachment or attachment.task_id != task_id:
            return error_response('附件不存在', code=404, status_code=404)

        file_path = os.path.abspath(attachment.file_path)
        if not os.path.exists(file_path):
            return error_response('文件不存在', code=404, status_code=404)

        return send_file(file_path, as_attachment=True, download_name=attachment.file_name)

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@tasks_bp.route('/download-client', methods=['GET'])
def download_client():
    """下载Chrome插件客户端"""
    try:
        import zipfile
        import tempfile
        import shutil
        from pathlib import Path

        # Chrome插件源码路径
        client_path = Path(__file__).parent.parent.parent.parent / 'client' / 'chrome-extension'

        if not client_path.exists():
            return error_response('客户端文件不存在', code=404, status_code=404)

        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        temp_client_path = Path(temp_dir) / 'chrome-extension'

        # 复制插件文件到临时目��
        shutil.copytree(client_path, temp_client_path)

        # 获取服务器地址（从请求头或配置中）
        server_url = request.host_url.rstrip('/')

        # 创建配置文件
        config_content = f"""// 自动生成的配置文件
const AUTO_CONFIG = {{
  serverUrl: '{server_url}'
}};
"""
        config_file = temp_client_path / 'auto-config.js'
        config_file.write_text(config_content, encoding='utf-8')

        # 创建临时zip文件
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')

        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in temp_client_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(temp_client_path.parent)
                    zipf.write(file_path, arcname)

        # 清理临时目录
        shutil.rmtree(temp_dir)

        return send_file(temp_zip.name, as_attachment=True, download_name='task-manager-chrome-extension.zip')

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)
