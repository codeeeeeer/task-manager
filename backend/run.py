"""
应用启动文件
"""
import os
from dotenv import load_dotenv
from app import create_app, socketio

# 加载环境变量
load_dotenv()

# 创建应用实例
app = create_app(os.getenv('FLASK_ENV', 'production'))


if __name__ == '__main__':
    # 使用SocketIO运行
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
