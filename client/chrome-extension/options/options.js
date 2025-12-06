document.addEventListener('DOMContentLoaded', () => {
  loadConfig()

  document.getElementById('configForm').addEventListener('submit', (e) => {
    e.preventDefault()
    saveConfig()
  })
})

function loadConfig() {
  chrome.storage.sync.get(['serverUrl', 'umCode', 'soundEnabled'], (result) => {
    document.getElementById('serverUrl').value = result.serverUrl || ''
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
