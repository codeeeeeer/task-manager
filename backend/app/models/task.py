"""
任务模型
"""
from app import db
from app.models.base import BaseModel
from datetime import datetime, timezone


class Task(BaseModel):
    """任务表"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False, comment='任务标题')
    category = db.Column(db.String(50), nullable=False, comment='任务分类')
    description = db.Column(db.Text, comment='任务详情描述')
    status = db.Column(db.String(50), nullable=False, default='新建', index=True, comment='任务状态')
    progress = db.Column(db.Integer, default=0, comment='处理进度(0-100)')
    time_progress = db.Column(db.Integer, default=0, comment='时间进度(0-100)')

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True, comment='创建人ID')
    current_handler_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True, comment='当前处理人ID')

    expected_start_time = db.Column(db.DateTime, comment='期望开始时间')
    expected_end_time = db.Column(db.DateTime, index=True, comment='期望完成时间')
    actual_start_time = db.Column(db.DateTime, comment='实际开始时间')
    actual_end_time = db.Column(db.DateTime, comment='实际完成时间')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), comment='更新时间')

    # 关系
    transfers = db.relationship('TaskTransfer', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('TaskComment', backref='task', lazy='dynamic', cascade='all, delete-orphan')

    # 约束
    __table_args__ = (
        db.CheckConstraint('progress >= 0 AND progress <= 100', name='check_progress_range'),
        db.CheckConstraint('time_progress >= 0 AND time_progress <= 100', name='check_time_progress_range'),
        db.CheckConstraint("category IN ('版本任务', '紧急任务', '其他任务', '定时周期任务', '普通任务')", name='check_category'),
    )

    def calculate_time_progress(self):
        """计算时间进度"""
        try:
            if not self.expected_start_time or not self.expected_end_time:
                return 0

            now = datetime.now(timezone.utc)

            # 确保时间对象都带时区信息
            start_time = self.expected_start_time.replace(tzinfo=timezone.utc) if self.expected_start_time.tzinfo is None else self.expected_start_time
            end_time = self.expected_end_time.replace(tzinfo=timezone.utc) if self.expected_end_time.tzinfo is None else self.expected_end_time

            if now < start_time:
                return 0
            elif now > end_time:
                return 100
            else:
                total_duration = (end_time - start_time).total_seconds()
                if total_duration <= 0:
                    return 0
                elapsed_duration = (now - start_time).total_seconds()
                return int((elapsed_duration / total_duration) * 100)
        except Exception:
            return 0

    def to_dict(self, include_details=False):
        """转换为字典"""
        from app.models.user import User

        def format_datetime(dt):
            """格式化datetime为ISO字符串，确保带UTC时区信息"""
            if not dt:
                return None
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()

        result = {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'status': self.status,
            'progress': self.progress,
            'time_progress': self.calculate_time_progress(),
            'creator_id': self.creator_id,
            'creator_name': self.creator.name if self.creator else None,
            'current_handler_id': self.current_handler_id,
            'current_handler_name': self.current_handler.name if self.current_handler else None,
            'expected_start_time': format_datetime(self.expected_start_time),
            'expected_end_time': format_datetime(self.expected_end_time),
            'created_at': format_datetime(self.created_at),
            'updated_at': format_datetime(self.updated_at),
        }

        if include_details:
            result.update({
                'description': self.description,
                'actual_start_time': format_datetime(self.actual_start_time),
                'actual_end_time': format_datetime(self.actual_end_time),
            })

        return result

    def __repr__(self):
        return f'<Task {self.id} - {self.title}>'
