"""
数据库初始化脚本
创建管理员账户
"""
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # 检查是否已有管理员
    existing_admin = User.query.filter_by(um_code='UM001').first()
    if existing_admin:
        print('管理员账户已存在!')
        print(f'UM编号: {existing_admin.um_code}')
        print(f'姓名: {existing_admin.name}')
        print(f'邮箱: {existing_admin.email}')
    else:
        # 创建管理员
        admin = User(
            um_code='UM001',
            name='系统管理员',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')

        db.session.add(admin)
        db.session.commit()

        print('✓ 管理员账户创建成功!')
        print(f'UM编号: {admin.um_code}')
        print(f'姓名: {admin.name}')
        print(f'邮箱: {admin.email}')
        print(f'密码: admin123')
        print('\n请登录后立即修改密码!')
