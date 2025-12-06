"""
用户模型
"""
from app import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(BaseModel):
    """用户表"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    um_code = db.Column(db.String(50), unique=True, nullable=False, index=True, comment='用户UM编号')
    name = db.Column(db.String(100), nullable=False, comment='用户姓名')
    email = db.Column(db.String(255), unique=True, nullable=False, index=True, comment='邮箱')
    password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希')
    is_admin = db.Column(db.Boolean, default=False, comment='是否管理员')
    is_active = db.Column(db.Boolean, default=True, index=True, comment='是否激活')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    last_login_at = db.Column(db.DateTime, comment='最后登录时间')

    # 关系
    created_tasks = db.relationship('Task', foreign_keys='Task.creator_id', backref='creator', lazy='dynamic')
    handling_tasks = db.relationship('Task', foreign_keys='Task.current_handler_id', backref='current_handler', lazy='dynamic')

    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self, exclude_password=True):
        """转换为字典"""
        result = {
            'id': self.id,
            'um_code': self.um_code,
            'name': self.name,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }
        if not exclude_password:
            result['password_hash'] = self.password_hash
        return result

    def __repr__(self):
        return f'<User {self.um_code} - {self.name}>'
