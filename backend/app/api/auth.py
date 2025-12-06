"""
认证API
"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.services.user_service import UserService
from app.utils.response import success_response, error_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return error_response('请提供邮箱和密码')

        # 认证用户
        user = UserService.authenticate(email, password)
        if not user:
            return error_response('邮箱或密码错误', code=401, status_code=401)

        # 生成JWT Token
        access_token = create_access_token(identity=str(user.id))

        return success_response({
            'token': access_token,
            'user': user.to_dict()
        }, message='登录成功')

    except Exception as e:
        return error_response(str(e), code=500, status_code=500)


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册（暂时开放，实际应该由管理员创建）"""
    try:
        data = request.get_json()
        um_code = data.get('um_code')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not all([um_code, name, email, password]):
            return error_response('请提供完整信息')

        user = UserService.create_user(um_code, name, email, password)

        return success_response(user.to_dict(), message='注册成功')

    except ValueError as e:
        return error_response(str(e), code=409, status_code=409)
    except Exception as e:
        return error_response(str(e), code=500, status_code=500)
