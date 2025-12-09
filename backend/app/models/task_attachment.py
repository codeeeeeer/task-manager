"""
任务附件模型
"""
from app.models.base import BaseModel
from app import db
from datetime import datetime, timezone


class TaskAttachment(BaseModel):
    """任务附件"""
    __tablename__ = 'task_attachments'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # 文件大小(字节)
    file_type = db.Column(db.String(50))  # 文件类型/扩展名
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), comment='创建时间')

    # 关系
    task = db.relationship('Task', backref=db.backref('attachments', lazy='dynamic'))
    uploader = db.relationship('User', foreign_keys=[uploaded_by])

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'uploaded_by': self.uploaded_by,
            'uploader_name': self.uploader.name if self.uploader else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
