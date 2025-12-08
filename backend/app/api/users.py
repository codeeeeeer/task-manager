"""
用户管理API
"""
from flask import Blueprint, request
from app.services.user_service import UserService
from app.utils.response import success_response, error_response, admin_required, login_required, get_current_user

users_bp = Blueprint('users', __name__)


@users_bp.route('/all', methods=['GET'])
@login_required
def get_all_users():
    """获取所有用户简单列表（用于下拉选择）"""
    try:
        from app.models.user import User
        users = User.query.filter_by(is_active=True).all()
        return success_response([{
            'id': u.id,
            'um_code': u.um_code,
            'name': u.name
        } for u in users])

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@users_bp.route('', methods=['GET'])
@login_required
def get_users():
    """获取用户列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')

        result = UserService.list_users(page, per_page, search)
        return success_response(result)

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@users_bp.route('/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """获取用户详情"""
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            return error_response('用户不存在', code=404, status_code=404)

        return success_response(user.to_dict())

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@users_bp.route('', methods=['POST'])
@admin_required
def create_user():
    """创建用户（管理员）"""
    try:
        data = request.get_json()
        um_code = data.get('um_code')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        is_admin = data.get('is_admin', False)

        if not all([um_code, name, email, password]):
            return error_response('请提供完整信息')

        user = UserService.create_user(um_code, name, email, password, is_admin)

        return success_response(user.to_dict(), message='用户创建成功')

    except ValueError as e:
        return error_response(str(e), code=409, status_code=409)
    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@users_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """更新用户信息（管理员）"""
    try:
        data = request.get_json()
        user = UserService.update_user(user_id, **data)

        return success_response(user.to_dict(), message='用户更新成功')

    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@users_bp.route('/<int:user_id>/change-password', methods=['POST'])
@login_required
def change_password(user_id):
    """修改密码"""
    try:
        current_user = get_current_user()

        # 只能修改自己的密码
        if current_user.id != user_id:
            return error_response('只能修改自己的密码', code=403, status_code=403)

        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not all([old_password, new_password]):
            return error_response('请提供完整信息')

        UserService.change_password(user_id, old_password, new_password)

        return success_response(message='密码修改成功')

    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        return error_response(str(e), code=500, status_code=500)
