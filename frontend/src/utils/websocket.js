import io from 'socket.io-client'
import { getToken } from './auth'
import { ElNotification } from 'element-plus'

class WebSocketClient {
  constructor() {
    this.socket = null
    this.connected = false
  }

  connect() {
    const serverUrl = import.meta.env.VITE_WS_URL || window.location.origin
    const token = getToken()

    if (!token) {
      console.log('No token, skip WebSocket connection')
      return
    }

    this.socket = io(serverUrl, {
      auth: { token },
      transports: ['websocket'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 10
    })

    this.setupEventHandlers()
  }

  setupEventHandlers() {
    this.socket.on('connect', () => {
      console.log('WebSocket connected')
      this.connected = true
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
      this.connected = false
    })

    this.socket.on('connected', (data) => {
      console.log('Server confirmed:', data)
    })

    this.socket.on('notification', (notification) => {
      this.handleNotification(notification)
    })

    // 心跳
    setInterval(() => {
      if (this.connected) {
        this.socket.emit('ping')
      }
    }, 30000)
  }

  handleNotification(notification) {
    const notificationTypes = {
      '新任务': 'info',
      '任务流转': 'info',
      '任务留言': 'info',
      '任务预警': 'warning',
      '任务完成': 'success'
    }

    ElNotification({
      title: notification.title,
      message: notification.content,
      type: notificationTypes[notification.type] || 'info',
      duration: 5000,
      onClick: () => {
        if (notification.task_id) {
          window.location.href = `/#/tasks/${notification.task_id}`
        }
      }
    })
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
      this.connected = false
    }
  }
}

export default new WebSocketClient()
