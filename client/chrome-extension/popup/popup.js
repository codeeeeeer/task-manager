document.addEventListener('DOMContentLoaded', () => {
  loadStatus()
  loadNotifications()

  document.getElementById('settingsBtn').addEventListener('click', () => {
    chrome.runtime.openOptionsPage()
  })

  document.getElementById('openWebBtn').addEventListener('click', () => {
    chrome.storage.sync.get(['serverUrl'], (result) => {
      if (result.serverUrl) {
        chrome.tabs.create({ url: result.serverUrl })
      }
    })
  })
})

function loadStatus() {
  chrome.runtime.sendMessage({ type: 'GET_STATUS' }, (response) => {
    const statusDot = document.querySelector('.status-dot')
    const statusText = document.querySelector('.status-text')

    if (response.connected) {
      statusDot.classList.add('connected')
      statusText.textContent = '已连接'
    } else {
      statusDot.classList.remove('connected')
      statusText.textContent = '未连接'
    }
  })
}

function loadNotifications() {
  chrome.runtime.sendMessage({ type: 'GET_NOTIFICATIONS' }, (response) => {
    const listEl = document.getElementById('notificationList')
    const notifications = response.notifications || []

    if (notifications.length === 0) {
      listEl.innerHTML = '<div class="empty">暂无待响应任务</div>'
      return
    }

    listEl.innerHTML = notifications.map((n, index) => `
      <div class="notification-item" data-index="${index}">
        <div class="notification-header">
          <div class="notification-title">${n.title}</div>
          <button class="respond-btn" data-id="${n.task_id}">响应</button>
        </div>
        <div class="notification-content">${n.content}</div>
        <div class="notification-time">${formatTime(n.receivedAt || n.timestamp)}</div>
      </div>
    `).join('')

    // 添加响应按钮点击事件
    document.querySelectorAll('.respond-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation()
        const taskId = parseInt(btn.dataset.id)
        respondToTask(taskId, btn)
      })
    })

    // 添加通知项点击事件（跳转到任务详情）
    document.querySelectorAll('.notification-item').forEach(item => {
      item.addEventListener('click', () => {
        const index = parseInt(item.dataset.index)
        const notification = notifications[index]
        if (notification.task_id) {
          chrome.storage.sync.get(['serverUrl'], (result) => {
            if (result.serverUrl) {
              chrome.tabs.create({ url: `${result.serverUrl}/#/tasks/${notification.task_id}` })
            }
          })
        }
      })
    })
  })
}


async function respondToTask(taskId, btnElement) {
  try {
    btnElement.disabled = true
    btnElement.textContent = '响应中...'

    const response = await chrome.runtime.sendMessage({
      type: 'RESPOND_TASK',
      taskId: taskId
    })

    if (response.success) {
      chrome.storage.sync.get(['serverUrl'], (result) => {
        if (result.serverUrl) {
          chrome.tabs.create({ url: `${result.serverUrl}/#/tasks/${taskId}` })
        }
      })
    } else {
      alert('响应失败: ' + (response.error || '未知错误'))
      btnElement.disabled = false
      btnElement.textContent = '响应'
    }
  } catch (error) {
    console.error('响应任务失败:', error)
    alert('响应失败: ' + error.message)
    btnElement.disabled = false
    btnElement.textContent = '响应'
  }
}

function formatTime(isoString) {
  const date = new Date(isoString)
  const now = new Date()
  const diff = (now - date) / 1000

  if (diff < 60) return '刚刚'
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`
  return date.toLocaleString('zh-CN')
}
