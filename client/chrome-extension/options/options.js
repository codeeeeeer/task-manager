document.addEventListener('DOMContentLoaded', () => {
  loadConfig()

  document.getElementById('configForm').addEventListener('submit', (e) => {
    e.preventDefault()
    saveConfig()
  })
})

function loadConfig() {
  chrome.storage.sync.get(['serverUrl', 'umCode', 'soundEnabled'], (result) => {
    // 如果没有配置过服务器地址，尝试使用自动配置
    let serverUrl = result.serverUrl || ''
    if (!serverUrl && typeof AUTO_CONFIG !== 'undefined' && AUTO_CONFIG.serverUrl) {
      serverUrl = AUTO_CONFIG.serverUrl
      // ��动保存到storage
      chrome.storage.sync.set({ serverUrl })
    }

    document.getElementById('serverUrl').value = serverUrl
    document.getElementById('umCode').value = result.umCode || ''
    document.getElementById('soundEnabled').checked = result.soundEnabled !== false
  })
}

function saveConfig() {
  const config = {
    serverUrl: document.getElementById('serverUrl').value.trim(),
    umCode: document.getElementById('umCode').value.trim(),
    soundEnabled: document.getElementById('soundEnabled').checked
  }

  if (!config.serverUrl || !config.umCode) {
    showMessage('请填写完整配置', 'error')
    return
  }

  chrome.runtime.sendMessage({
    type: 'UPDATE_CONFIG',
    config
  })

  showMessage('设置已保存', 'success')
}

function showMessage(text, type) {
  const messageEl = document.getElementById('message')
  messageEl.textContent = text
  messageEl.className = `message ${type}`
  messageEl.style.display = 'block'

  setTimeout(() => {
    messageEl.style.display = 'none'
  }, 3000)
}
