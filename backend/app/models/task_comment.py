"""
任务留言模型
"""
from app import db
from app.models.base import BaseModel
from datetime import datetime, timezone


class TaskComment(BaseModel):
    """任务留言表"""
    __tablename__ = 'task_comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False, index=True, comment='任务ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='留言人ID')
    content = db.Column(db.Text, nullable=False, comment='留言内容')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), comment='更新时间')
    is_deleted = db.Column(db.Boolean, default=False, comment='软删除标记')

    # 关系
    user = db.relationship('User')

    def to_dict(self):
        """转换为字典"""
        def format_datetime(dt):
            if not dt:
                return None
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()

        return {
            'id': self.id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'content': self.content,
            'created_at': format_datetime(self.created_at),
            'updated_at': format_datetime(self.updated_at),
            'is_deleted': self.is_deleted
        }

    def __repr__(self):
        return f'<TaskComment {self.id}>'
