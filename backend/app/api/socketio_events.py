"""
SocketIO事件处理
"""
from flask_socketio import emit, join_room, leave_room
from flask import request
from app import socketio
from flask_jwt_extended import decode_token
from app.services.user_service import UserService

# 存储用户连接
user_connections = {}  # {user_id: [sid1, sid2, ...]}


@socketio.on('connect')
def handle_connect(auth):
    """
    客户端连接
    :param auth: {'token': 'JWT_TOKEN'} 或 {'um_code': 'UM001'}
    """
    try:
        # 方式1: JWT认证
        if 'token' in auth:
            token = auth['token']
            payload = decode_token(token)
            user_id = int(payload['sub'])
        # 方式2: UM编号认证(用于客户端)
        elif 'um_code' in auth:
            user = UserService.get_user_by_um_code(auth['um_code'])
            if not user:
                return False
            user_id = user.id
        else:
            return False

        # 加入用户专属房间
        room = f'user_{user_id}'
        join_room(room)

        # 记录连接
        sid = request.sid
        if user_id not in user_connections:
            user_connections[user_id] = []
        user_connections[user_id].append(sid)

        print(f'User {user_id} connected, sid: {sid}')

        # 发送欢迎消息
        emit('connected', {'message': '连接成功', 'user_id': user_id})

        return True

    except Exception as e:
        print(f'Connection failed: {str(e)}')
        return False


@socketio.on('disconnect')
def handle_disconnect():
    """客户端断开连接"""
    sid = request.sid

    # 移除连接记录
    for user_id, sids in user_connections.items():
        if sid in sids:
            sids.remove(sid)
            print(f'User {user_id} disconnected, sid: {sid}')
            break


@socketio.on('ping')
def handle_ping():
    """心跳"""
    from datetime import datetime
    emit('pong', {'timestamp': datetime.utcnow().isoformat()})
