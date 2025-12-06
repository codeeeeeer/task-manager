"""
API响应工具
"""
from flask import jsonify
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.services.user_service import UserService


def success_response(data=None, message='success', code=0):
    """成功响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    })


def error_response(message='error', code=400, status_code=400):
    """错误响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': None
    }), status_code


def login_required(fn):
    """登录认证装饰器"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    """管理员权限装饰器"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        user = UserService.get_user_by_id(user_id)
        if not user or not user.is_admin:
            return error_response('需要管理员权限', code=403, status_code=403)
        return fn(*args, **kwargs)
    return wrapper


def get_current_user():
    """获取当前登录用户"""
    user_id = int(get_jwt_identity())
    return UserService.get_user_by_id(user_id)
