"""
任务统计模型
"""
from app import db
from datetime import datetime, timezone
import json


class TaskStatistics(db.Model):
    """任务统计表"""
    __tablename__ = 'task_statistics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stat_type = db.Column(db.String(50), nullable=False, comment='统计类型')
    stat_key = db.Column(db.String(50), nullable=True, comment='统计键')
    stat_value = db.Column(db.Text, nullable=False, comment='统计值JSON')
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), comment='更新时间')

    __table_args__ = (
        db.UniqueConstraint('stat_type', 'stat_key', name='uq_stat_type_key'),
        db.Index('idx_stat_type_key', 'stat_type', 'stat_key'),
    )

    @staticmethod
    def get_stat(stat_type, stat_key=None):
        """获取统计数据"""
        stat = TaskStatistics.query.filter_by(stat_type=stat_type, stat_key=stat_key).first()
        if stat:
            return json.loads(stat.stat_value)
        return None

    @staticmethod
    def set_stat(stat_type, stat_key, value):
        """设置统计数据"""
        stat = TaskStatistics.query.filter_by(stat_type=stat_type, stat_key=stat_key).first()
        if stat:
            stat.stat_value = json.dumps(value, ensure_ascii=False)
            stat.updated_at = datetime.now(timezone.utc)
        else:
            stat = TaskStatistics(
                stat_type=stat_type,
                stat_key=stat_key,
                stat_value=json.dumps(value, ensure_ascii=False),
                updated_at=datetime.now(timezone.utc)
            )
            db.session.add(stat)

    def __repr__(self):
        return f'<TaskStatistics {self.stat_type}:{self.stat_key}>'
