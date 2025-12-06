"""
数据模型基类
"""
from app import db


class BaseModel(db.Model):
    """模型基类"""
    __abstract__ = True

    def save(self):
        """保存到数据库"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """从数据库删除"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        """根据ID获取"""
        return cls.query.get(id)
