// WebSocket连接
let ws = null
let config = null
let notificationHistory = []

// 插件安装时初始化
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed')
  loadConfig()
})

// 插件启动时加载配置
chrome.runtime.onStartup.addListener(() => {
  console.log('Extension started')
  loadConfig()
})

// 从storage加载配置
function loadConfig() {
  chrome.storage.sync.get(['serverUrl', 'umCode', 'soundEnabled'], (result) => {
    config = {
      serverUrl: result.serverUrl || '',
      umCode: result.umCode || '',
      soundEnabled: result.soundEnabled !== false
    }

    if (config.serverUrl && config.umCode) {
      connectWebSocket()
    }
  })
}

// 连接WebSocket
function connectWebSocket() {
  if (ws) {
    ws.close()
  }

  console.log('Connecting to WebSocket:', config.serverUrl)

  // 注意: Service Worker中无法直接使用socket.io
  // 需要使用原生WebSocket或提供HTTP轮询作为备选
  const wsUrl = config.serverUrl.replace('http', 'ws') + '/socket.io/?EIO=4&transport=websocket'

  ws = new WebSocket(wsUrl)

  ws.onopen = () => {
    console.log('WebSocket connected')
    updateBadge('✓', '#4caf50')

    // 发送认证
    const authMsg = JSON.stringify({
      type: 'auth',
      um_code: config.umCode
    })
    ws.send(authMsg)
  }

  ws.onclose = () => {
    console.log('WebSocket disconnected')
    updateBadge('✗', '#f44336')

    // 5秒后重连
    setTimeout(() => {
      if (config.serverUrl && config.umCode) {
        connectWebSocket()
      }
    }, 5000)
  }

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      handleNotification(data)
    } catch (e) {
      console.error('Parse message error:', e)
    }
  }
}

// 处理通知
function handleNotification(notification) {
  console.log('Notification received:', notification)

  // 保存到历史记录
  notificationHistory.unshift({
    ...notification,
    receivedAt: new Date().toISOString()
  })

  if (notificationHistory.length > 50) {
    notificationHistory = notificationHistory.slice(0, 50)
  }

  chrome.storage.local.set({ notificationHistory })

  // 显示Chrome通知
  showChromeNotification(notification)

  // 更新badge
  updateUnreadCount()
}

// 显示Chrome通知
function showChromeNotification(notification) {
  const notificationOptions = {
    type: 'basic',
    iconUrl: 'assets/icon128.png',
    title: notification.title || '新通知',
    message: notification.content || '',
    priority: 2
  }

  chrome.notifications.create(
    `notification_${Date.now()}`,
    notificationOptions,
    (notificationId) => {
      chrome.notifications.onClicked.addListener((clickedId) => {
        if (clickedId === notificationId && notification.task_id) {
          const taskUrl = `${config.serverUrl}/#/tasks/${notification.task_id}`
          chrome.tabs.create({ url: taskUrl })
          chrome.notifications.clear(clickedId)
        }
      })
    }
  )
}

// 更新badge
function updateBadge(text, color) {
  chrome.action.setBadgeText({ text })
  chrome.action.setBadgeBackgroundColor({ color })
}

// 更新未读数
function updateUnreadCount() {
  const unreadCount = notificationHistory.filter(n => !n.read).length
  if (unreadCount > 0) {
    updateBadge(unreadCount.toString(), '#ff6b6b')
  } else {
    updateBadge('', '#4caf50')
  }
}

// 监听来自popup的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GET_NOTIFICATIONS') {
    sendResponse({ notifications: notificationHistory })
  } else if (message.type === 'MARK_AS_READ') {
    const notification = notificationHistory.find(n => n.timestamp === message.timestamp)
    if (notification) {
      notification.read = true
      chrome.storage.local.set({ notificationHistory })
      updateUnreadCount()
    }
  } else if (message.type === 'UPDATE_CONFIG') {
    config = message.config
    chrome.storage.sync.set(config)
    connectWebSocket()
  } else if (message.type === 'GET_STATUS') {
    sendResponse({
      connected: ws && ws.readyState === WebSocket.OPEN,
      config
    })
  }
})
