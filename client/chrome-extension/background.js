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

// 轮询间隔ID
let pollingInterval = null

// 连接WebSocket (改用HTTP轮询)
function connectWebSocket() {
  if (pollingInterval) {
    clearInterval(pollingInterval)
  }

  console.log('Starting notification polling:', config.serverUrl)
  updateBadge('✓', '#4caf50')

  // 立即执行一次
  pollNotifications()

  // 每30秒轮询一次
  pollingInterval = setInterval(pollNotifications, 30000)
}

// 轮询通知
async function pollNotifications() {
  try {
    const response = await fetch(`${config.serverUrl}/api/users/notifications?um_code=${config.umCode}`)

    if (!response.ok) {
      throw new Error('Failed to fetch notifications')
    }

    const result = await response.json()

    if (result.code === 0 && result.data) {
      // 处理新通知
      const notifications = result.data
      notifications.forEach(notification => {
        // 检查是否已经处理过
        const exists = notificationHistory.find(n => n.id === notification.id)
        if (!exists) {
          handleNotification(notification)
        }
      })
    }

    updateBadge('✓', '#4caf50')
  } catch (error) {
    console.error('Polling error:', error)
    updateBadge('✗', '#f44336')
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
    const notification = notificationHistory.find(n => n.id === message.id)
    if (notification) {
      notification.read = true
      chrome.storage.local.set({ notificationHistory })
      updateUnreadCount()
      sendResponse({ success: true })
    }
  } else if (message.type === 'UPDATE_CONFIG') {
    config = message.config
    chrome.storage.sync.set(config)
    connectWebSocket()
  } else if (message.type === 'GET_STATUS') {
    sendResponse({
      connected: pollingInterval !== null,
      config
    })
  }
})
