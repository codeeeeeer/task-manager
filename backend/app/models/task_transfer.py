"""
任务流转记录模型
"""
from app import db
from app.models.base import BaseModel
from datetime import datetime


class TaskTransfer(BaseModel):
    """任务流转记录表"""
    __tablename__ = 'task_transfers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False, index=True, comment='任务ID')
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='操作人ID')
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='流转目标用户ID')
    message = db.Column(db.Text, comment='流转留言')
    transfer_type = db.Column(db.String(50), default='流转', nullable=False, comment='流转类型')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True, comment='创建时间')

    # 关系
    operator = db.relationship('User', foreign_keys=[operator_id])
    target_user = db.relationship('User', foreign_keys=[target_user_id])

    # 约束
    __table_args__ = (
        db.CheckConstraint("transfer_type IN ('创建', '流转', '响应', '挂起', '恢复', '完成', '关闭')", name='check_transfer_type'),
    )

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'operator_id': self.operator_id,
            'operator_name': self.operator.name if self.operator else None,
            'target_user_id': self.target_user_id,
            'target_user_name': self.target_user.name if self.target_user else None,
            'message': self.message,
            'transfer_type': self.transfer_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<TaskTransfer {self.id} - {self.transfer_type}>'
