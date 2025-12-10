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

// Service Worker启动时立即加载配置
loadConfig()

// 从storage加载配置
function loadConfig() {
  chrome.storage.sync.get(['serverUrl', 'umCode', 'soundEnabled'], (result) => {
    config = {
      serverUrl: result.serverUrl || '',
      umCode: result.umCode || '',
      soundEnabled: result.soundEnabled !== false
    }

    console.log('Config loaded:', config)

    if (config.serverUrl && config.umCode) {
      connectWebSocket()
    } else {
      console.log('Config incomplete, please set serverUrl and umCode in options')
    }
  })
}

// 加载历史通知
chrome.storage.local.get(['notificationHistory'], (result) => {
  if (result.notificationHistory) {
    notificationHistory = result.notificationHistory
    updateUnreadCount()
  }
})

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

  // 每10秒轮询一次
  pollingInterval = setInterval(pollNotifications, 10000)
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
      const pendingTasks = result.data
      const previousHistory = [...notificationHistory]

      // 更新待响应任务列表（替换而不是追加）
      notificationHistory = pendingTasks.map(task => ({
        ...task,
        receivedAt: task.timestamp
      }))

      // 为新任务显示Chrome通知
      pendingTasks.forEach(task => {
        const existedBefore = previousHistory.find(n => n.id === task.id)
        if (!existedBefore) {
          showChromeNotification(task)
        }
      })

      chrome.storage.local.set({ notificationHistory })
      updateUnreadCount()
    }

    updateBadge('✓', '#4caf50')
  } catch (error) {
    console.error('Polling error:', error)
    updateBadge('✗', '#f44336')
  }
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
  const unreadCount = notificationHistory.length
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
  } else if (message.type === 'UPDATE_CONFIG') {
    config = message.config
    chrome.storage.sync.set(config)
    connectWebSocket()
  } else if (message.type === 'GET_STATUS') {
    sendResponse({
      connected: pollingInterval !== null,
      config
    })
  } else if (message.type === 'RESPOND_TASK') {
    respondTask(message.taskId).then(result => {
      sendResponse(result)
    })
    return true
  }
})

// 响应任务
async function respondTask(taskId) {
  try {
    const response = await fetch(
      `${config.serverUrl}/api/tasks/${taskId}/respond-by-umcode?um_code=${config.umCode}`,
      { method: 'POST' }
    )

    const result = await response.json()

    if (result.code === 0) {
      pollNotifications()
      return { success: true }
    } else {
      return { success: false, error: result.message }
    }
  } catch (error) {
    console.error('响应任务失败:', error)
    return { success: false, error: error.message }
  }
}
