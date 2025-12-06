# EXE客户端设计文档

## 1. 客户端概述

EXE客户端是基于C++和MFC开发的Windows桌面应用程序,通过WebSocket与服务端保持连接,实时接收任务通知。

**核心要求:**
- 程序体积 < 1MB
- 系统托盘驻留
- Windows通知提醒
- 轻量级设计

## 2. 技术选型

### 2.1 开发环境
- **Visual Studio 2019/2022**
- **C++ 17**
- **MFC (静态链接)**

### 2.2 依赖库
- **IXWebSocket**: 轻量级WebSocket客户端库 (~100KB)
  - 替代方案: WebSocket++ (更轻量)
- **nlohmann/json**: JSON解析库 (单头文件)
- **Windows API**: 系统托盘、通知

### 2.3 体积优化策略
- 使用MFC静态链接
- 移除调试信息
- 启用编译器优化
- 使用压缩工具(UPX)

## 3. 项目结构

```
exe-client/
├── TaskNotifier/
│   ├── TaskNotifier.h           # 应用程序头文件
│   ├── TaskNotifier.cpp         # 应用程序实现
│   ├── MainDlg.h                # 主对话框头文件
│   ├── MainDlg.cpp              # 主对话框实现
│   ├── TrayIcon.h               # 托盘图标封装
│   ├── TrayIcon.cpp
│   ├── WebSocketClient.h        # WebSocket客户端封装
│   ├── WebSocketClient.cpp
│   ├── ConfigManager.h          # 配置管理
│   ├── ConfigManager.cpp
│   ├── NotificationManager.h    # 通知管理
│   ├── NotificationManager.cpp
│   ├── resource.h               # 资源头文件
│   ├── TaskNotifier.rc          # 资源文件
│   └── res/
│       ├── app.ico              # 应用图标
│       ├── tray_connected.ico   # 托盘图标(已连接)
│       ├── tray_disconnected.ico # 托盘图标(未连接)
│       └── notification.wav     # 提示音
├── include/                     # 第三方库头文件
│   ├── ixwebsocket/
│   └── json.hpp
├── lib/                         # 第三方库
│   └── ixwebsocket.lib
└── TaskNotifier.sln             # 解决方案
```

## 4. 核心模块设计

### 4.1 WebSocket客户端封装

```cpp
// WebSocketClient.h
#pragma once
#include <ixwebsocket/IXWebSocket.h>
#include <functional>
#include <string>

class WebSocketClient
{
public:
    WebSocketClient();
    ~WebSocketClient();

    // 连接到服务器
    bool Connect(const CString& serverUrl, const CString& umCode);

    // 断开连接
    void Disconnect();

    // 是否已连接
    bool IsConnected() const;

    // 设置消息回调
    void SetMessageCallback(std::function<void(const std::string&)> callback);

    // 设置连接状态回调
    void SetConnectionCallback(std::function<void(bool)> callback);

private:
    void HandleMessage(const ix::WebSocketMessagePtr& msg);
    void SendAuth(const CString& umCode);
    void StartHeartbeat();

private:
    ix::WebSocket m_webSocket;
    std::function<void(const std::string&)> m_messageCallback;
    std::function<void(bool)> m_connectionCallback;
    bool m_connected;
};
```

```cpp
// WebSocketClient.cpp
#include "pch.h"
#include "WebSocketClient.h"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

WebSocketClient::WebSocketClient()
    : m_connected(false)
{
}

WebSocketClient::~WebSocketClient()
{
    Disconnect();
}

bool WebSocketClient::Connect(const CString& serverUrl, const CString& umCode)
{
    std::string url = CT2A(serverUrl);

    // 配置WebSocket
    m_webSocket.setUrl(url);

    // 设置回调
    m_webSocket.setOnMessageCallback(
        [this](const ix::WebSocketMessagePtr& msg) {
            HandleMessage(msg);
        }
    );

    // 启动连接
    m_webSocket.start();

    // 发送认证
    SendAuth(umCode);

    return true;
}

void WebSocketClient::Disconnect()
{
    if (m_connected) {
        m_webSocket.stop();
        m_connected = false;
    }
}

bool WebSocketClient::IsConnected() const
{
    return m_connected;
}

void WebSocketClient::SetMessageCallback(std::function<void(const std::string&)> callback)
{
    m_messageCallback = callback;
}

void WebSocketClient::SetConnectionCallback(std::function<void(bool)> callback)
{
    m_connectionCallback = callback;
}

void WebSocketClient::HandleMessage(const ix::WebSocketMessagePtr& msg)
{
    if (msg->type == ix::WebSocketMessageType::Open)
    {
        m_connected = true;
        if (m_connectionCallback) {
            m_connectionCallback(true);
        }
    }
    else if (msg->type == ix::WebSocketMessageType::Close)
    {
        m_connected = false;
        if (m_connectionCallback) {
            m_connectionCallback(false);
        }
    }
    else if (msg->type == ix::WebSocketMessageType::Message)
    {
        if (m_messageCallback) {
            m_messageCallback(msg->str);
        }
    }
}

void WebSocketClient::SendAuth(const CString& umCode)
{
    json authMsg;
    authMsg["um_code"] = CT2A(umCode);

    std::string authStr = authMsg.dump();
    m_webSocket.send(authStr);
}

void WebSocketClient::StartHeartbeat()
{
    // 定时发送心跳
    // 使用定时器实现
}
```

### 4.2 配置管理

```cpp
// ConfigManager.h
#pragma once
#include <string>

class ConfigManager
{
public:
    static ConfigManager& Instance();

    // 加载配置
    bool LoadConfig();

    // 保存配置
    bool SaveConfig();

    // Getters
    CString GetServerUrl() const { return m_serverUrl; }
    CString GetUmCode() const { return m_umCode; }
    bool IsSoundEnabled() const { return m_soundEnabled; }
    bool IsAutoStart() const { return m_autoStart; }

    // Setters
    void SetServerUrl(const CString& url) { m_serverUrl = url; }
    void SetUmCode(const CString& code) { m_umCode = code; }
    void SetSoundEnabled(bool enabled) { m_soundEnabled = enabled; }
    void SetAutoStart(bool enabled) { m_autoStart = enabled; }

private:
    ConfigManager();
    ~ConfigManager();

    CString GetConfigFilePath();

private:
    CString m_serverUrl;
    CString m_umCode;
    bool m_soundEnabled;
    bool m_autoStart;
};
```

```cpp
// ConfigManager.cpp
#include "pch.h"
#include "ConfigManager.h"

ConfigManager& ConfigManager::Instance()
{
    static ConfigManager instance;
    return instance;
}

ConfigManager::ConfigManager()
    : m_soundEnabled(true)
    , m_autoStart(false)
{
}

ConfigManager::~ConfigManager()
{
}

bool ConfigManager::LoadConfig()
{
    CString configPath = GetConfigFilePath();

    // 读取INI文件
    TCHAR buffer[256];

    GetPrivateProfileString(_T("Server"), _T("Url"), _T(""), buffer, 256, configPath);
    m_serverUrl = buffer;

    GetPrivateProfileString(_T("User"), _T("UmCode"), _T(""), buffer, 256, configPath);
    m_umCode = buffer;

    m_soundEnabled = GetPrivateProfileInt(_T("Settings"), _T("SoundEnabled"), 1, configPath) != 0;
    m_autoStart = GetPrivateProfileInt(_T("Settings"), _T("AutoStart"), 0, configPath) != 0;

    return true;
}

bool ConfigManager::SaveConfig()
{
    CString configPath = GetConfigFilePath();

    WritePrivateProfileString(_T("Server"), _T("Url"), m_serverUrl, configPath);
    WritePrivateProfileString(_T("User"), _T("UmCode"), m_umCode, configPath);
    WritePrivateProfileString(_T("Settings"), _T("SoundEnabled"), m_soundEnabled ? _T("1") : _T("0"), configPath);
    WritePrivateProfileString(_T("Settings"), _T("AutoStart"), m_autoStart ? _T("1") : _T("0"), configPath);

    return true;
}

CString ConfigManager::GetConfigFilePath()
{
    TCHAR modulePath[MAX_PATH];
    GetModuleFileName(NULL, modulePath, MAX_PATH);

    CString path = modulePath;
    int pos = path.ReverseFind(_T('\\'));
    path = path.Left(pos + 1);
    path += _T("config.ini");

    return path;
}
```

### 4.3 通知管理

```cpp
// NotificationManager.h
#pragma once
#include <string>

class NotificationManager
{
public:
    static NotificationManager& Instance();

    // 显示通知
    void ShowNotification(const CString& title, const CString& content, int taskId = 0);

    // 播放提示音
    void PlaySound();

private:
    NotificationManager();
    ~NotificationManager();

    // Windows 10 Toast通知
    void ShowToast(const CString& title, const CString& content);

    // 传统气球提示
    void ShowBalloon(const CString& title, const CString& content);
};
```

```cpp
// NotificationManager.cpp
#include "pch.h"
#include "NotificationManager.h"
#include "ConfigManager.h"
#include <windows.h>
#include <mmsystem.h>

#pragma comment(lib, "winmm.lib")

NotificationManager& NotificationManager::Instance()
{
    static NotificationManager instance;
    return instance;
}

NotificationManager::NotificationManager()
{
}

NotificationManager::~NotificationManager()
{
}

void NotificationManager::ShowNotification(const CString& title, const CString& content, int taskId)
{
    // 优先使用Windows 10 Toast通知
    if (IsWindows10OrGreater()) {
        ShowToast(title, content);
    } else {
        ShowBalloon(title, content);
    }

    // 播放提示音
    if (ConfigManager::Instance().IsSoundEnabled()) {
        PlaySound();
    }
}

void NotificationManager::PlaySound()
{
    // 播放嵌入在资源中的WAV文件
    ::PlaySound(MAKEINTRESOURCE(IDR_NOTIFICATION_SOUND),
                AfxGetResourceHandle(),
                SND_RESOURCE | SND_ASYNC);
}

void NotificationManager::ShowToast(const CString& title, const CString& content)
{
    // Windows 10 Toast通知实现
    // 需要使用Windows Runtime API
    // 为了简化,这里使用气球提示
    ShowBalloon(title, content);
}

void NotificationManager::ShowBalloon(const CString& title, const CString& content)
{
    // 通过托盘图标显示气球提示
    // 在TrayIcon中实现
}
```

### 4.4 托盘图标

```cpp
// TrayIcon.h
#pragma once

class CTrayIcon
{
public:
    CTrayIcon();
    ~CTrayIcon();

    // 创建托盘图标
    BOOL Create(CWnd* pWnd, UINT uCallbackMessage, LPCTSTR szToolTip, HICON icon, UINT uID);

    // 移除托盘图标
    BOOL Remove();

    // 更新图标
    BOOL SetIcon(HICON hIcon);

    // 更新提示文本
    BOOL SetTooltip(LPCTSTR pszToolTip);

    // 显示气球提示
    BOOL ShowBalloon(LPCTSTR szTitle, LPCTSTR szMsg, UINT uTimeout = 5000, DWORD dwInfoFlags = NIIF_INFO);

private:
    NOTIFYICONDATA m_nid;
    BOOL m_bCreated;
};
```

```cpp
// TrayIcon.cpp
#include "pch.h"
#include "TrayIcon.h"

CTrayIcon::CTrayIcon()
    : m_bCreated(FALSE)
{
    ZeroMemory(&m_nid, sizeof(m_nid));
}

CTrayIcon::~CTrayIcon()
{
    Remove();
}

BOOL CTrayIcon::Create(CWnd* pWnd, UINT uCallbackMessage, LPCTSTR szToolTip, HICON icon, UINT uID)
{
    m_nid.cbSize = sizeof(NOTIFYICONDATA);
    m_nid.hWnd = pWnd->GetSafeHwnd();
    m_nid.uID = uID;
    m_nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP;
    m_nid.uCallbackMessage = uCallbackMessage;
    m_nid.hIcon = icon;
    _tcscpy_s(m_nid.szTip, szToolTip);

    m_bCreated = Shell_NotifyIcon(NIM_ADD, &m_nid);
    return m_bCreated;
}

BOOL CTrayIcon::Remove()
{
    if (!m_bCreated)
        return FALSE;

    m_bCreated = !Shell_NotifyIcon(NIM_DELETE, &m_nid);
    return !m_bCreated;
}

BOOL CTrayIcon::SetIcon(HICON hIcon)
{
    if (!m_bCreated)
        return FALSE;

    m_nid.uFlags = NIF_ICON;
    m_nid.hIcon = hIcon;

    return Shell_NotifyIcon(NIM_MODIFY, &m_nid);
}

BOOL CTrayIcon::SetTooltip(LPCTSTR pszToolTip)
{
    if (!m_bCreated)
        return FALSE;

    m_nid.uFlags = NIF_TIP;
    _tcscpy_s(m_nid.szTip, pszToolTip);

    return Shell_NotifyIcon(NIM_MODIFY, &m_nid);
}

BOOL CTrayIcon::ShowBalloon(LPCTSTR szTitle, LPCTSTR szMsg, UINT uTimeout, DWORD dwInfoFlags)
{
    if (!m_bCreated)
        return FALSE;

    m_nid.uFlags = NIF_INFO;
    m_nid.uTimeout = uTimeout;
    m_nid.dwInfoFlags = dwInfoFlags;
    _tcscpy_s(m_nid.szInfoTitle, szTitle);
    _tcscpy_s(m_nid.szInfo, szMsg);

    return Shell_NotifyIcon(NIM_MODIFY, &m_nid);
}
```

### 4.5 主对话框

```cpp
// MainDlg.h
#pragma once
#include "TrayIcon.h"
#include "WebSocketClient.h"

#define WM_TRAY_ICON_NOTIFY (WM_USER + 1)

class CMainDlg : public CDialogEx
{
public:
    CMainDlg(CWnd* pParent = nullptr);

protected:
    virtual BOOL OnInitDialog();
    afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
    afx_msg LRESULT OnTrayNotify(WPARAM wParam, LPARAM lParam);
    afx_msg void OnBnClickedConnect();
    afx_msg void OnBnClickedSave();
    afx_msg void OnClose();
    afx_msg void OnShowWindow();
    afx_msg void OnExit();

    DECLARE_MESSAGE_MAP()

private:
    void InitTrayIcon();
    void ConnectToServer();
    void OnWebSocketMessage(const std::string& message);
    void OnWebSocketConnection(bool connected);
    void UpdateConnectionStatus(bool connected);

private:
    CTrayIcon m_trayIcon;
    WebSocketClient m_wsClient;
    CEdit m_editServerUrl;
    CEdit m_editUmCode;
    CButton m_btnConnect;
    CStatic m_staticStatus;
    BOOL m_connected;
};
```

```cpp
// MainDlg.cpp
#include "pch.h"
#include "MainDlg.h"
#include "ConfigManager.h"
#include "NotificationManager.h"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

BEGIN_MESSAGE_MAP(CMainDlg, CDialogEx)
    ON_WM_SYSCOMMAND()
    ON_MESSAGE(WM_TRAY_ICON_NOTIFY, &CMainDlg::OnTrayNotify)
    ON_BN_CLICKED(IDC_BTN_CONNECT, &CMainDlg::OnBnClickedConnect)
    ON_BN_CLICKED(IDC_BTN_SAVE, &CMainDlg::OnBnClickedSave)
    ON_WM_CLOSE()
    ON_COMMAND(ID_TRAY_SHOW, &CMainDlg::OnShowWindow)
    ON_COMMAND(ID_TRAY_EXIT, &CMainDlg::OnExit)
END_MESSAGE_MAP()

CMainDlg::CMainDlg(CWnd* pParent)
    : CDialogEx(IDD_MAIN_DIALOG, pParent)
    , m_connected(FALSE)
{
}

BOOL CMainDlg::OnInitDialog()
{
    CDialogEx::OnInitDialog();

    // 加载配置
    ConfigManager::Instance().LoadConfig();

    // 初始化控件
    m_editServerUrl.SubclassDlgItem(IDC_EDIT_SERVER_URL, this);
    m_editUmCode.SubclassDlgItem(IDC_EDIT_UM_CODE, this);
    m_btnConnect.SubclassDlgItem(IDC_BTN_CONNECT, this);
    m_staticStatus.SubclassDlgItem(IDC_STATIC_STATUS, this);

    // 设置配置值
    m_editServerUrl.SetWindowText(ConfigManager::Instance().GetServerUrl());
    m_editUmCode.SetWindowText(ConfigManager::Instance().GetUmCode());

    // 初始化托盘图标
    InitTrayIcon();

    // 设置WebSocket回调
    m_wsClient.SetMessageCallback(
        [this](const std::string& msg) {
            OnWebSocketMessage(msg);
        }
    );

    m_wsClient.SetConnectionCallback(
        [this](bool connected) {
            OnWebSocketConnection(connected);
        }
    );

    // 自动连接
    if (!ConfigManager::Instance().GetServerUrl().IsEmpty() &&
        !ConfigManager::Instance().GetUmCode().IsEmpty())
    {
        ConnectToServer();
    }

    return TRUE;
}

void CMainDlg::InitTrayIcon()
{
    HICON hIcon = LoadIcon(AfxGetInstanceHandle(), MAKEINTRESOURCE(IDI_TRAY_DISCONNECTED));
    m_trayIcon.Create(this, WM_TRAY_ICON_NOTIFY, _T("任务通知客户端 - 未连接"), hIcon, 1);
}

void CMainDlg::ConnectToServer()
{
    CString serverUrl, umCode;
    m_editServerUrl.GetWindowText(serverUrl);
    m_editUmCode.GetWindowText(umCode);

    if (serverUrl.IsEmpty() || umCode.IsEmpty()) {
        AfxMessageBox(_T("请填写服务器地址和用户编号"));
        return;
    }

    m_wsClient.Connect(serverUrl, umCode);
    m_btnConnect.EnableWindow(FALSE);
}

void CMainDlg::OnWebSocketMessage(const std::string& message)
{
    try {
        json j = json::parse(message);

        // 检查是否是通知消息
        if (j.contains("type") && j["type"] == "notification") {
            CString title = CA2T(j["title"].get<std::string>().c_str());
            CString content = CA2T(j["content"].get<std::string>().c_str());
            int taskId = j.value("task_id", 0);

            NotificationManager::Instance().ShowNotification(title, content, taskId);
            m_trayIcon.ShowBalloon(title, content);
        }
    }
    catch (const std::exception& e) {
        // 日志记录
    }
}

void CMainDlg::OnWebSocketConnection(bool connected)
{
    UpdateConnectionStatus(connected);
}

void CMainDlg::UpdateConnectionStatus(bool connected)
{
    m_connected = connected;

    if (connected) {
        m_staticStatus.SetWindowText(_T("状态: 已连接"));
        m_btnConnect.SetWindowText(_T("断开"));
        m_btnConnect.EnableWindow(TRUE);

        HICON hIcon = LoadIcon(AfxGetInstanceHandle(), MAKEINTRESOURCE(IDI_TRAY_CONNECTED));
        m_trayIcon.SetIcon(hIcon);
        m_trayIcon.SetTooltip(_T("任务通知客户端 - 已连接"));
    } else {
        m_staticStatus.SetWindowText(_T("状态: 未连接"));
        m_btnConnect.SetWindowText(_T("连接"));
        m_btnConnect.EnableWindow(TRUE);

        HICON hIcon = LoadIcon(AfxGetInstanceHandle(), MAKEINTRESOURCE(IDI_TRAY_DISCONNECTED));
        m_trayIcon.SetIcon(hIcon);
        m_trayIcon.SetTooltip(_T("任务通知客户端 - 未连接"));
    }
}

LRESULT CMainDlg::OnTrayNotify(WPARAM wParam, LPARAM lParam)
{
    if (lParam == WM_LBUTTONDBLCLK) {
        ShowWindow(SW_SHOW);
        SetForegroundWindow();
    }
    else if (lParam == WM_RBUTTONUP) {
        CMenu menu;
        menu.CreatePopupMenu();
        menu.AppendMenu(MF_STRING, ID_TRAY_SHOW, _T("显示主窗口"));
        menu.AppendMenu(MF_SEPARATOR);
        menu.AppendMenu(MF_STRING, ID_TRAY_EXIT, _T("退出"));

        CPoint pt;
        GetCursorPos(&pt);
        SetForegroundWindow();
        menu.TrackPopupMenu(TPM_LEFTALIGN, pt.x, pt.y, this);
    }

    return 0;
}

void CMainDlg::OnClose()
{
    // 最小化到托盘
    ShowWindow(SW_HIDE);
}

void CMainDlg::OnExit()
{
    CDialogEx::OnOK();
}
```

## 5. 编译配置

### 5.1 项目属性设置

**C/C++ → 常规:**
- 附加包含目录: `$(ProjectDir)include`

**C/C++ → 代码生成:**
- 运行库: 多线程 (/MT) - 静态链接

**C/C++ → 优化:**
- 优化: 最大优化 (/O2)
- 内联函数扩展: 适用于任何情况 (/Ob2)

**链接器 → 常规:**
- 附加库目录: `$(ProjectDir)lib`

**链接器 → 输入:**
- 附加依赖项: `ixwebsocket.lib;winmm.lib;ws2_32.lib`

**链接器 → 调试:**
- 生成调试信息: 否

## 6. 体积优化

### 6.1 编译优化
- 使用Release配置
- 启用/O2优化
- 移除调试信息
- 使用/MT静态链接

### 6.2 资源优化
- 压缩图标和声音文件
- 使用较低的采样率(如8kHz单声道WAV)

### 6.3 UPX压缩
```bash
upx --best --ultra-brute TaskNotifier.exe
```

预期结果: 500KB - 900KB

## 7. 安装与部署

### 7.1 绿色部署
- 单个EXE文件
- 配置保存在同目录的config.ini

### 7.2 安装包(可选)
- 使用Inno Setup或NSIS
- 添加开机自启动选项
- 创建桌面快捷方式

## 8. 测试要点

- WebSocket连接稳定性
- 断线重连
- 内存占用 (< 50MB)
- CPU占用 (空闲时 < 1%)
- 通知显示
- 托盘图标交互
- 配置保存加载
- 多实例检测(防止重复运行)
