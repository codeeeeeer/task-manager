"""
用户服务
"""
from app import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from datetime import datetime


class UserService:
    """用户业务逻辑服务"""

    @staticmethod
    def authenticate(email, password):
        """
        用户认证
        :param email: 邮箱
        :param password: 密码
        :return: User对象或None
        """
        user = User.query.filter_by(email=email, is_active=True).first()
        if user and user.check_password(password):
            # 更新最后登录时间
            user.last_login_at = datetime.utcnow()
            db.session.commit()
            return user
        return None

    @staticmethod
    def create_user(um_code, name, email, password, is_admin=False):
        """
        创建用户
        :return: User对象
        :raises: ValueError
        """
        try:
            user = User(
                um_code=um_code,
                name=name,
                email=email,
                is_admin=is_admin
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()
            error_msg = str(e.orig)
            if 'um_code' in error_msg:
                raise ValueError(f"用户编号 {um_code} 已存在")
            elif 'email' in error_msg:
                raise ValueError(f"邮箱 {email} 已被注册")
            else:
                raise ValueError("创建用户失败")

    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        return User.query.filter_by(id=user_id, is_active=True).first()

    @staticmethod
    def get_user_by_um_code(um_code):
        """根据UM编号获取用户"""
        return User.query.filter_by(um_code=um_code, is_active=True).first()

    @staticmethod
    def update_user(user_id, **kwargs):
        """
        更新用户信息
        :param user_id: 用户ID
        :param kwargs: 要更新的字段
        :return: User对象
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        allowed_fields = ['name', 'email', 'is_admin', 'is_active']
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(user, key, value)

        try:
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("更新失败，邮箱可能已被使用")

    @staticmethod
    def change_password(user_id, old_password, new_password):
        """修改密码"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        if not user.check_password(old_password):
            raise ValueError("原密码错误")

        user.set_password(new_password)
        db.session.commit()
        return True

    @staticmethod
    def list_users(page=1, per_page=20, search=None, is_admin=None):
        """
        获取用户列表
        """
        query = User.query.filter_by(is_active=True)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (User.name.ilike(search_pattern)) |
                (User.email.ilike(search_pattern)) |
                (User.um_code.ilike(search_pattern))
            )

        if is_admin is not None:
            query = query.filter_by(is_admin=is_admin)

        total = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            'users': [user.to_dict() for user in users],
            'total': total,
            'page': page,
            'per_page': per_page
        }
