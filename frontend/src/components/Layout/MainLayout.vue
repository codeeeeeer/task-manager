<template>
  <div class="layout">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>任务分发工具</h1>
          <div class="user-info">
            <el-button @click="toggleTheme" size="small" class="theme-btn">
              {{ themeStore.currentTheme === 'light' ? '🌙 高科技' : '☀️ 默认' }}
            </el-button>
            <span>{{ userInfo?.name }}</span>
            <el-button @click="handleLogout" type="danger" size="small">退出</el-button>
          </div>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu :default-active="currentRoute" router>
            <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/tasks">
              <el-icon><List /></el-icon>
              <span>任务列表</span>
            </el-menu-item>
            <el-menu-item index="/users" v-if="userInfo?.is_admin">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
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
import { HomeFilled, List, User } from '@element-plus/icons-vue'

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

  .el-header {
    background-color: var(--color-bg-header);
    color: var(--color-text-header);
    display: flex;
    align-items: center;

    .header-content {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;

      h1 {
        font-size: 20px;
        margin: 0;
      }

      .user-info {
        display: flex;
        align-items: center;
        gap: 10px;

        .theme-btn {
          background-color: rgba(255, 255, 255, 0.2);
          border: 1px solid rgba(255, 255, 255, 0.3);
          color: var(--color-text-header);

          &:hover {
            background-color: rgba(255, 255, 255, 0.3);
          }
        }
      }
    }
  }

  .el-aside {
    background-color: var(--color-bg-sidebar);
    border-right: 1px solid var(--color-border);
  }

  .el-main {
    background-color: var(--color-bg-body);
  }
}
</style>
