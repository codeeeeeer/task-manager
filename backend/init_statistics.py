"""
初始化统计数据脚本
"""
from app import create_app, db
from app.services.task_service import TaskService

def init_statistics():
    """初始化统计数据"""
    app = create_app()
    with app.app_context():
        print('开始初始化统计数据...')
        try:
            TaskService.calculate_full_statistics()
            print('统计数据初始化完成！')
        except Exception as e:
            print(f'初始化失败: {str(e)}')
            db.session.rollback()

if __name__ == '__main__':
    init_statistics()
