<template>
  <div class="layout" :class="{ 'theme-tech': themeStore.currentTheme === 'tech' }">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo-section">
            <div class="logo-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h1 class="app-title">
              {{ themeStore.currentTheme === 'tech' ? 'TASK_CORE' : '任务分发工具' }}
            </h1>
          </div>

          <div class="header-actions">
            <!-- 主题切换 -->
            <div class="theme-switcher">
              <button class="theme-btn" @click="toggleTheme" :title="themeStore.currentTheme === 'light' ? '切换到高科技模式' : '切换到明亮模式'">
                <span class="theme-icon light-icon" :class="{ active: themeStore.currentTheme === 'light' }">☀️</span>
                <span class="theme-icon tech-icon" :class="{ active: themeStore.currentTheme === 'tech' }">🌙</span>
              </button>
            </div>

            <!-- 用户信息 -->
            <div class="user-section">
              <el-dropdown trigger="click">
                <div class="user-avatar-wrapper">
                  <div class="user-avatar">
                    {{ userInfo?.name?.charAt(0) || 'U' }}
                  </div>
                  <span class="user-name">{{ userInfo?.name }}</span>
                  <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
                </div>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="handleLogout">
                      <el-icon><SwitchButton /></el-icon>
                      退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </div>
      </el-header>

      <el-container class="main-container">
        <!-- 侧边栏 -->
        <el-aside width="220px" class="app-sidebar">
          <el-menu :default-active="currentRoute" router class="sidebar-menu">
            <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>
              <span>{{ themeStore.currentTheme === 'tech' ? 'DASHBOARD' : '首页' }}</span>
            </el-menu-item>
            <el-menu-item index="/tasks">
              <el-icon><List /></el-icon>
              <span>{{ themeStore.currentTheme === 'tech' ? 'TASK_LIST' : '任务列表' }}</span>
            </el-menu-item>
            <el-menu-item index="/users" v-if="userInfo?.is_admin">
              <el-icon><User /></el-icon>
              <span>{{ themeStore.currentTheme === 'tech' ? 'USER_MGMT' : '用户管理' }}</span>
            </el-menu-item>
          </el-menu>

          <!-- 侧边栏底部状态 -->
          <div class="sidebar-footer">
            <div class="status-indicator">
              <span class="status-dot"></span>
              <span class="status-text">{{ themeStore.currentTheme === 'tech' ? 'SYSTEM ONLINE' : '系统在线' }}</span>
            </div>
          </div>
        </el-aside>

        <!-- 主内容区 -->
        <el-main class="app-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useThemeStore } from '@/store/theme'
import { HomeFilled, List, User, ArrowDown, SwitchButton } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const userInfo = computed(() => authStore.userInfo)
const currentRoute = computed(() => route.path)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const toggleTheme = () => {
  themeStore.toggleTheme()
}
</script>

<style scoped lang="scss">
.layout {
  height: 100vh;
  background: var(--el-bg-color);
}

// ==================== 顶部导航栏 ====================
.app-header {
  height: 64px;
  background: var(--el-bg-color-overlay);
  border-bottom: 1px solid var(--el-border-color);
  padding: 0 24px;
  display: flex;
  align-items: center;
  box-shadow: var(--app-shadow);
  position: relative;
  z-index: 100;

  .header-content {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo-section {
    display: flex;
    align-items: center;
    gap: 12px;

    .logo-icon {
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--el-color-primary);

      svg {
        width: 28px;
        height: 28px;
      }
    }

    .app-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--el-text-color-primary);
      margin: 0;
      letter-spacing: 0.5px;
    }
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 20px;
  }
}

// 主题切换按钮
.theme-switcher {
  .theme-btn {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    border: 1px solid var(--el-border-color);
    background: var(--el-bg-color-page);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;

    &:hover {
      border-color: var(--el-color-primary);
      box-shadow: 0 0 0 3px var(--el-color-primary-light-9);
    }

    .theme-icon {
      position: absolute;
      font-size: 20px;
      transition: all 0.3s ease;
      opacity: 0;
      transform: scale(0.5) rotate(-180deg);

      &.active {
        opacity: 1;
        transform: scale(1) rotate(0deg);
      }
    }
  }
}

// 用户区域
.user-section {
  .user-avatar-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      background: var(--el-color-primary-light-9);
    }

    .user-avatar {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: var(--app-gradient-primary);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 14px;
    }

    .user-name {
      font-size: 14px;
      font-weight: 500;
      color: var(--el-text-color-primary);
    }

    .dropdown-icon {
      color: var(--el-text-color-secondary);
      font-size: 12px;
    }
  }
}

// ==================== 主容器 ====================
.main-container {
  height: calc(100vh - 64px);
}

// ==================== 侧边栏 ====================
.app-sidebar {
  background: var(--el-bg-color-overlay);
  border-right: 1px solid var(--el-border-color);
  display: flex;
  flex-direction: column;
  padding: 16px 0;

  .sidebar-menu {
    flex: 1;
    padding: 0 8px;
  }

  .sidebar-footer {
    padding: 16px;
    border-top: 1px solid var(--el-border-color);

    .status-indicator {
      display: flex;
      align-items: center;
      gap: 8px;

      .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--el-color-success);
        animation: pulse 2s infinite;
      }

      .status-text {
        font-size: 12px;
        color: var(--el-text-color-secondary);
        font-weight: 500;
      }
    }
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

// ==================== 主内容区 ====================
.app-main {
  background: var(--el-bg-color);
  padding: 24px;
  overflow-y: auto;
}

// ==================== 高科技主题特殊样式 ====================
.theme-tech {
  .app-header {
    background: rgba(30, 41, 59, 0.95);
    backdrop-filter: blur(12px);
    border-bottom-color: var(--el-border-color);

    .logo-icon {
      color: var(--el-color-primary);
      filter: drop-shadow(0 0 8px rgba(6, 182, 212, 0.5));
    }

    .app-title {
      font-family: var(--app-font-mono);
      letter-spacing: 2px;
      text-transform: uppercase;
      text-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
    }
  }

  .theme-switcher .theme-btn {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 0;

    &:hover {
      box-shadow: var(--app-glow-primary);
    }
  }

  .user-section {
    .user-avatar-wrapper {
      border-radius: 0;

      &:hover {
        background: rgba(6, 182, 212, 0.1);
      }

      .user-avatar {
        border-radius: 0;
        background: var(--app-gradient-primary);
        box-shadow: var(--app-glow-primary);
      }

      .user-name {
        font-family: var(--app-font-mono);
        letter-spacing: 1px;
      }
    }
  }

  .app-sidebar {
    background: rgba(30, 41, 59, 0.95);
    backdrop-filter: blur(12px);

    .sidebar-footer {
      .status-dot {
        box-shadow: 0 0 10px rgba(74, 222, 128, 0.5);
      }

      .status-text {
        font-family: var(--app-font-mono);
        letter-spacing: 1px;
        text-transform: uppercase;
      }
    }
  }

  .app-main {
    background: var(--el-bg-color);
  }
}
</style>
