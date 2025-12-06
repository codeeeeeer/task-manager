"""
Flask应用初始化
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler
from config import config
import logging
from logging.handlers import RotatingFileHandler
import os

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()
scheduler = BackgroundScheduler()


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # 初始化SocketIO
    socketio_config = {
        'cors_allowed_origins': app.config['SOCKETIO_CORS_ALLOWED_ORIGINS'],
        'async_mode': 'eventlet'
    }
    if app.config['SOCKETIO_MESSAGE_QUEUE']:
        socketio_config['message_queue'] = app.config['SOCKETIO_MESSAGE_QUEUE']

    socketio.init_app(app, **socketio_config)

    # 配置日志
    setup_logging(app)

    # 注册蓝图
    register_blueprints(app)

    # 注册SocketIO事件处理
    register_socketio_handlers()

    # 初始化定时任务
    if not app.config.get('TESTING'):
        init_scheduler(app)

    # 创建上传目录
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app


def setup_logging(app):
    """配置日志"""
    if not app.debug and not app.testing:
        # 确保日志目录存在
        os.makedirs(os.path.dirname(app.config['LOG_FILE']), exist_ok=True)

        # 文件处理器
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))

        app.logger.addHandler(file_handler)
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.info('Task Manager startup')


def register_blueprints(app):
    """注册蓝图"""
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    from app.api.tasks import tasks_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')


def register_socketio_handlers():
    """注册SocketIO事件处理"""
    from app.api import socketio_events


def init_scheduler(app):
    """初始化定时任务"""
    with app.app_context():
        from app.services.scheduler_service import init_scheduler
        init_scheduler()
