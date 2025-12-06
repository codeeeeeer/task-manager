# Chrome插件设计文档

## 1. 插件概述

Chrome插件作为任务通知客户端，通过WebSocket与服务端保持连接，实时接收任务通知，并通过浏览器原生通知API提醒用户。

## 2. 技术架构

### 2.1 Manifest V3
使用Chrome Extension Manifest V3标准。

### 2.2 核心组件
- **Service Worker** (background.js): 后台常驻，管理WebSocket连接
- **Popup** (popup.html/js): 插件图标弹窗，显示最近通知和配置
- **Options Page** (options.html/js): 配置页面
- **Content Script**(可选): 注入到任务管理页面

## 3. 项目结构

```
chrome-extension/
├── manifest.json             # 插件配置文件
├── background.js             # Service Worker
├── popup/
│   ├── popup.html           # 弹窗页面
│   ├── popup.js             # 弹窗逻辑
│   └── popup.css            # 弹窗样式
├── options/
│   ├── options.html         # 配置页面
│   ├── options.js           # 配置逻辑
│   └── options.css          # 配置样式
├── libs/
│   └── socket.io.min.js     # Socket.IO客户端库
├── assets/
│   ├── icon16.png           # 图标 16x16
│   ├── icon48.png           # 图标 48x48
│   ├── icon128.png          # 图标 128x128
│   └── notification.mp3     # 提示音
└── README.md
```

## 4. Manifest配置

```json
{
  "manifest_version": 3,
  "name": "任务分发工具通知",
  "version": "1.0.0",
  "description": "实时接收任务通知",
  "permissions": [
    "notifications",
    "storage",
    "alarms"
  ],
  "host_permissions": [
    "http://*/*",
    "https://*/*",
    "ws://*/*",
    "wss://*/*"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "assets/icon16.png",
      "48": "assets/icon48.png",
      "128": "assets/icon128.png"
    }
  },
  "options_page": "options/options.html",
  "icons": {
    "16": "assets/icon16.png",
    "48": "assets/icon48.png",
    "128": "assets/icon128.png"
  }
}
```

## 5. Service Worker实现

```javascript
// background.js
importScripts('libs/socket.io.min.js');

let socket = null;
let config = null;
let reconnectTimer = null;
let notificationHistory = [];

// 插件安装时初始化
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
  loadConfig();
});

// 插件启动时加载配置
chrome.runtime.onStartup.addListener(() => {
  console.log('Extension started');
  loadConfig();
});

// 从storage加载配置
function loadConfig() {
  chrome.storage.sync.get(['serverUrl', 'umCode', 'soundEnabled'], (result) => {
    config = {
      serverUrl: result.serverUrl || '',
      umCode: result.umCode || '',
      soundEnabled: result.soundEnabled !== false
    };

    if (config.serverUrl && config.umCode) {
      connectWebSocket();
    }
  });
}

// 连接WebSocket
function connectWebSocket() {
  if (socket) {
    socket.disconnect();
  }

  console.log('Connecting to WebSocket:', config.serverUrl);

  socket = io(config.serverUrl, {
    auth: {
      um_code: config.umCode
    },
    transports: ['websocket'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 10
  });

  socket.on('connect', () => {
    console.log('WebSocket connected');
    updateBadge('✓', '#4caf50');
    clearReconnectTimer();
  });

  socket.on('disconnect', () => {
    console.log('WebSocket disconnected');
    updateBadge('✗', '#f44336');
    scheduleReconnect();
  });

  socket.on('connected', (data) => {
    console.log('Server confirmed:', data);
  });

  socket.on('notification', (notification) => {
    handleNotification(notification);
  });

  // 心跳
  socket.on('pong', () => {
    console.log('Pong received');
  });

  // 定时发送心跳
  chrome.alarms.create('heartbeat', { periodInMinutes: 0.5 });
}

// 处理通知
function handleNotification(notification) {
  console.log('Notification received:', notification);

  // 保存到历史记录
  notificationHistory.unshift({
    ...notification,
    receivedAt: new Date().toISOString()
  });

  // 只保留最近50条
  if (notificationHistory.length > 50) {
    notificationHistory = notificationHistory.slice(0, 50);
  }

  // 保存到storage
  chrome.storage.local.set({ notificationHistory });

  // 播放提示音
  if (config.soundEnabled) {
    playSound();
  }

  // 显示Chrome通知
  showChromeNotification(notification);

  // 更新badge显示未读数
  updateUnreadCount();
}

// 显示Chrome通知
function showChromeNotification(notification) {
  const notificationOptions = {
    type: 'basic',
    iconUrl: 'assets/icon128.png',
    title: notification.title,
    message: notification.content,
    priority: 2,
    requireInteraction: true  // 需要用户手动关闭
  };

  chrome.notifications.create(
    `notification_${Date.now()}`,
    notificationOptions,
    (notificationId) => {
      // 点击通知打开任务页面
      chrome.notifications.onClicked.addListener((clickedId) => {
        if (clickedId === notificationId && notification.task_id) {
          const taskUrl = `${config.serverUrl}/#/tasks/${notification.task_id}`;
          chrome.tabs.create({ url: taskUrl });
          chrome.notifications.clear(clickedId);
        }
      });
    }
  );
}

// 播放提示音
function playSound() {
  // Service Worker中无法直接播放音频
  // 可以通过发送消息给popup或content script来播放
  chrome.runtime.sendMessage({ type: 'PLAY_SOUND' });
}

// 更新badge
function updateBadge(text, color) {
  chrome.action.setBadgeText({ text });
  chrome.action.setBadgeBackgroundColor({ color });
}

// 更新未读数
function updateUnreadCount() {
  const unreadCount = notificationHistory.filter(n => !n.read).length;
  if (unreadCount > 0) {
    updateBadge(unreadCount.toString(), '#ff6b6b');
  } else {
    updateBadge('', '#4caf50');
  }
}

// 定时重连
function scheduleReconnect() {
  clearReconnectTimer();
  reconnectTimer = setTimeout(() => {
    if (config.serverUrl && config.umCode) {
      connectWebSocket();
    }
  }, 5000);
}

function clearReconnectTimer() {
  if (reconnectTimer) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }
}

// 心跳定时器
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'heartbeat' && socket && socket.connected) {
    socket.emit('ping');
  }
});

// 监听来自popup的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GET_NOTIFICATIONS') {
    sendResponse({ notifications: notificationHistory });
  } else if (message.type === 'MARK_AS_READ') {
    const notification = notificationHistory.find(n => n.timestamp === message.timestamp);
    if (notification) {
      notification.read = true;
      chrome.storage.local.set({ notificationHistory });
      updateUnreadCount();
    }
  } else if (message.type === 'UPDATE_CONFIG') {
    config = message.config;
    chrome.storage.sync.set(config);
    connectWebSocket();
  } else if (message.type === 'GET_STATUS') {
    sendResponse({
      connected: socket ? socket.connected : false,
      config
    });
  }
});
```

## 6. Popup页面

```html
<!-- popup/popup.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>任务通知</title>
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div class="container">
    <div class="header">
      <h3>任务通知</h3>
      <div class="status" id="status">
        <span class="status-dot"></span>
        <span class="status-text">未连接</span>
      </div>
    </div>

    <div class="notification-list" id="notificationList">
      <!-- 通知列表动态生成 -->
    </div>

    <div class="footer">
      <button id="settingsBtn">设置</button>
      <button id="openWebBtn">打开控制台</button>
    </div>
  </div>

  <script src="popup.js"></script>
</body>
</html>
```

```javascript
// popup/popup.js
document.addEventListener('DOMContentLoaded', () => {
  loadStatus();
  loadNotifications();

  document.getElementById('settingsBtn').addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });

  document.getElementById('openWebBtn').addEventListener('click', () => {
    chrome.storage.sync.get(['serverUrl'], (result) => {
      if (result.serverUrl) {
        chrome.tabs.create({ url: result.serverUrl });
      }
    });
  });
});

function loadStatus() {
  chrome.runtime.sendMessage({ type: 'GET_STATUS' }, (response) => {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');

    if (response.connected) {
      statusDot.classList.add('connected');
      statusText.textContent = '已连接';
    } else {
      statusDot.classList.remove('connected');
      statusText.textContent = '未连接';
    }
  });
}

function loadNotifications() {
  chrome.runtime.sendMessage({ type: 'GET_NOTIFICATIONS' }, (response) => {
    const listEl = document.getElementById('notificationList');
    const notifications = response.notifications || [];

    if (notifications.length === 0) {
      listEl.innerHTML = '<div class="empty">暂无通知</div>';
      return;
    }

    listEl.innerHTML = notifications.slice(0, 10).map(n => `
      <div class="notification-item ${n.read ? 'read' : 'unread'}" data-timestamp="${n.timestamp}">
        <div class="notification-title">${n.title}</div>
        <div class="notification-content">${n.content}</div>
        <div class="notification-time">${formatTime(n.receivedAt)}</div>
      </div>
    `).join('');

    // 点击通知跳转
    document.querySelectorAll('.notification-item').forEach(item => {
      item.addEventListener('click', () => {
        const timestamp = item.dataset.timestamp;
        chrome.runtime.sendMessage({
          type: 'MARK_AS_READ',
          timestamp
        });
      });
    });
  });
}

function formatTime(isoString) {
  const date = new Date(isoString);
  const now = new Date();
  const diff = (now - date) / 1000; // 秒

  if (diff < 60) return '刚刚';
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`;
  return date.toLocaleString('zh-CN');
}
```

## 7. Options配置页

```html
<!-- options/options.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>插件设置</title>
  <link rel="stylesheet" href="options.css">
</head>
<body>
  <div class="container">
    <h2>任务通知插件设置</h2>

    <form id="configForm">
      <div class="form-group">
        <label for="serverUrl">服务器地址</label>
        <input
          type="text"
          id="serverUrl"
          placeholder="http://192.168.1.100:5000"
          required
        />
        <small>例如: http://192.168.1.100:5000</small>
      </div>

      <div class="form-group">
        <label for="umCode">用户编号(UM编号)</label>
        <input
          type="text"
          id="umCode"
          placeholder="UM001"
          required
        />
      </div>

      <div class="form-group">
        <label>
          <input type="checkbox" id="soundEnabled" checked />
          启用提示音
        </label>
      </div>

      <button type="submit" class="btn-primary">保存设置</button>
    </form>

    <div id="message" class="message"></div>
  </div>

  <script src="options.js"></script>
</body>
</html>
```

```javascript
// options/options.js
document.addEventListener('DOMContentLoaded', () => {
  loadConfig();

  document.getElementById('configForm').addEventListener('submit', (e) => {
    e.preventDefault();
    saveConfig();
  });
});

function loadConfig() {
  chrome.storage.sync.get(['serverUrl', 'umCode', 'soundEnabled'], (result) => {
    document.getElementById('serverUrl').value = result.serverUrl || '';
    document.getElementById('umCode').value = result.umCode || '';
    document.getElementById('soundEnabled').checked = result.soundEnabled !== false;
  });
}

function saveConfig() {
  const config = {
    serverUrl: document.getElementById('serverUrl').value.trim(),
    umCode: document.getElementById('umCode').value.trim(),
    soundEnabled: document.getElementById('soundEnabled').checked
  };

  // 验证
  if (!config.serverUrl || !config.umCode) {
    showMessage('请填写完整配置', 'error');
    return;
  }

  // 保存并通知background
  chrome.runtime.sendMessage({
    type: 'UPDATE_CONFIG',
    config
  });

  showMessage('设置已保存', 'success');
}

function showMessage(text, type) {
  const messageEl = document.getElementById('message');
  messageEl.textContent = text;
  messageEl.className = `message ${type}`;
  messageEl.style.display = 'block';

  setTimeout(() => {
    messageEl.style.display = 'none';
  }, 3000);
}
```

## 8. 样式设计

```css
/* popup/popup.css */
body {
  width: 350px;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
  font-size: 14px;
}

.container {
  padding: 0;
}

.header {
  padding: 15px;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h3 {
  margin: 0;
  color: #fff;
}

.status {
  display: flex;
  align-items: center;
  gap: 5px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ccc;
}

.status-dot.connected {
  background: #4caf50;
}

.status-text {
  color: #fff;
  font-size: 12px;
}

.notification-list {
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.notification-item:hover {
  background: #f5f5f5;
}

.notification-item.unread {
  background: #fff5f5;
}

.notification-title {
  font-weight: 600;
  margin-bottom: 5px;
}

.notification-content {
  color: #666;
  font-size: 13px;
  margin-bottom: 5px;
}

.notification-time {
  color: #999;
  font-size: 11px;
}

.empty {
  padding: 40px 20px;
  text-align: center;
  color: #999;
}

.footer {
  padding: 10px 15px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
}

.footer button {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: #ff6b6b;
  color: #fff;
}

.footer button:hover {
  background: #ff5252;
}
```

## 9. 打包与发布

### 9.1 打包
将整个chrome-extension文件夹打包为.zip文件

### 9.2 开发者模式安装
1. 打开Chrome浏览器
2. 进入 `chrome://extensions/`
3. 启用"开发者模式"
4. 点击"加载已解压的扩展程序"
5. 选择chrome-extension文件夹

### 9.3 Chrome Web Store发布(可选)
- 需要注册Chrome开发者账号
- 上传.zip包
- 填写插件信息和截图
- 提交审核

## 10. 测试要点

- WebSocket连接稳定性
- 断线重连机制
- 通知接收和显示
- 配置保存和加载
- 跨域请求权限
- 性能和内存占用
