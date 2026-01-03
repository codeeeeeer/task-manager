<template>
  <div class="login-page" :class="{ 'theme-tech': isTechTheme }">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-gradient"></div>
      <div class="bg-pattern"></div>
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>

    <!-- 登录卡片 -->
    <div class="login-wrapper">
      <div class="login-card">
        <!-- Logo 区域 -->
        <div class="logo-section">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h1 class="app-name">{{ isTechTheme ? 'TASK_CORE' : '任务分发工具' }}</h1>
          <p class="app-desc">{{ isTechTheme ? 'ENTERPRISE TASK MANAGEMENT SYSTEM' : '企业级任务管理系统' }}</p>
        </div>

        <!-- 登录表单 -->
        <el-form :model="loginForm" :rules="rules" ref="formRef" class="login-form">
          <el-form-item prop="email">
            <el-input
              v-model="loginForm.email"
              :placeholder="isTechTheme ? 'EMAIL_ADDRESS' : '请输入邮箱'"
              size="large"
            >
              <template #prefix>
                <el-icon><Message /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              :placeholder="isTechTheme ? 'PASSWORD' : '请输入密码'"
              size="large"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-button
            type="primary"
            size="large"
            @click="handleLogin"
            :loading="loading"
            class="login-btn"
          >
            {{ loading ? (isTechTheme ? 'AUTHENTICATING...' : '登录中...') : (isTechTheme ? 'LOGIN' : '登录') }}
          </el-button>
        </el-form>

        <!-- 主题切换 -->
        <div class="theme-toggle">
          <button class="toggle-btn" @click="toggleTheme">
            <span class="toggle-icon">{{ isTechTheme ? '☀️' : '🌙' }}</span>
            <span class="toggle-text">{{ isTechTheme ? 'LIGHT MODE' : '高科技模式' }}</span>
          </button>
        </div>
      </div>

      <!-- 底部版权 -->
      <div class="footer-info">
        <span>{{ isTechTheme ? '© 2024 TASK_CORE SYSTEM' : '© 2024 任务分发工具' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useThemeStore } from '@/store/theme'
import { ElMessage } from 'element-plus'
import { Message, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const isTechTheme = computed(() => themeStore.currentTheme === 'tech')

const loginForm = ref({
  email: '',
  password: ''
})

const rules = {
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const loading = ref(false)
const formRef = ref(null)

const handleLogin = async () => {
  await formRef.value.validate()
  loading.value = true

  try {
    await authStore.login(loginForm.value)
    ElMessage.success(isTechTheme.value ? 'ACCESS GRANTED' : '登录成功')
    router.push('/')
  } catch (error) {
    ElMessage.error(error.message || (isTechTheme.value ? 'ACCESS DENIED' : '登录失败'))
  } finally {
    loading.value = false
  }
}

const toggleTheme = () => {
  themeStore.toggleTheme()
}

onMounted(() => {
  themeStore.initTheme()
})
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: var(--el-bg-color);
}

// ==================== 背景装饰 ====================
.bg-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;

  .bg-gradient {
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, #dbeafe 0%, #fef3c7 50%, #fce7f3 100%);
    opacity: 0.6;
  }

  .bg-pattern {
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle at 1px 1px, rgba(59, 130, 246, 0.1) 1px, transparent 0);
    background-size: 40px 40px;
  }

  .floating-shapes {
    position: absolute;
    inset: 0;

    .shape {
      position: absolute;
      border-radius: 50%;
      opacity: 0.4;
      animation: float 20s infinite ease-in-out;

      &.shape-1 {
        width: 300px;
        height: 300px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        top: -100px;
        right: -100px;
        animation-delay: 0s;
      }

      &.shape-2 {
        width: 200px;
        height: 200px;
        background: linear-gradient(135deg, #10b981, #06b6d4);
        bottom: -50px;
        left: -50px;
        animation-delay: -5s;
      }

      &.shape-3 {
        width: 150px;
        height: 150px;
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        top: 50%;
        left: 10%;
        animation-delay: -10s;
      }
    }
  }
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(20px, -20px) rotate(5deg); }
  50% { transform: translate(-10px, 10px) rotate(-5deg); }
  75% { transform: translate(15px, 15px) rotate(3deg); }
}

// ==================== 登录卡片 ====================
.login-wrapper {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.login-card {
  width: 420px;
  padding: 48px 40px;
  background: var(--el-bg-color-overlay);
  border-radius: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
  border: 1px solid var(--el-border-color-light);

  .logo-section {
    text-align: center;
    margin-bottom: 40px;

    .logo-icon {
      width: 64px;
      height: 64px;
      margin: 0 auto 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--el-color-primary);

      svg {
        width: 48px;
        height: 48px;
      }
    }

    .app-name {
      font-size: 24px;
      font-weight: 700;
      color: var(--el-text-color-primary);
      margin: 0 0 8px;
    }

    .app-desc {
      font-size: 13px;
      color: var(--el-text-color-secondary);
      margin: 0;
      letter-spacing: 0.5px;
    }
  }

  .login-form {
    :deep(.el-form-item) {
      margin-bottom: 20px;
    }

    :deep(.el-input__wrapper) {
      padding: 4px 16px;
      height: 48px;
    }

    :deep(.el-input__inner) {
      height: 40px;
    }
  }

  .login-btn {
    width: 100%;
    height: 48px;
    font-size: 15px;
    font-weight: 600;
    margin-top: 8px;
  }

  .theme-toggle {
    margin-top: 32px;
    text-align: center;

    .toggle-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      border: 1px solid var(--el-border-color);
      border-radius: 20px;
      background: var(--el-bg-color-page);
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        border-color: var(--el-color-primary);
        background: var(--el-color-primary-light-9);
      }

      .toggle-icon {
        font-size: 16px;
      }

      .toggle-text {
        font-size: 12px;
        color: var(--el-text-color-secondary);
        font-weight: 500;
      }
    }
  }
}

.footer-info {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

// ==================== 高科技主题 ====================
.theme-tech {
  .bg-decoration {
    .bg-gradient {
      background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
      opacity: 1;
    }

    .bg-pattern {
      background-image:
        linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px);
      background-size: 50px 50px;
    }

    .floating-shapes .shape {
      opacity: 0.15;
      filter: blur(60px);

      &.shape-1 {
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
      }

      &.shape-2 {
        background: linear-gradient(135deg, #4ade80, #06b6d4);
      }

      &.shape-3 {
        background: linear-gradient(135deg, #facc15, #f43f5e);
      }
    }
  }

  .login-card {
    background: rgba(30, 41, 59, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 2px;
    border: 1px solid rgba(6, 182, 212, 0.3);
    box-shadow:
      0 0 40px rgba(6, 182, 212, 0.15),
      0 25px 50px -12px rgba(0, 0, 0, 0.5);

    .logo-section {
      .logo-icon {
        color: var(--el-color-primary);
        filter: drop-shadow(0 0 15px rgba(6, 182, 212, 0.5));
      }

      .app-name {
        font-family: var(--app-font-mono);
        letter-spacing: 3px;
        text-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
      }

      .app-desc {
        font-family: var(--app-font-mono);
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 11px;
      }
    }

    .login-form {
      :deep(.el-input__wrapper) {
        border-radius: 0;
      }

      :deep(.el-input__prefix) {
        color: var(--el-color-primary);
      }
    }

    .login-btn {
      border-radius: 0;
      text-transform: uppercase;
      letter-spacing: 2px;
      font-family: var(--app-font-mono);
    }

    .theme-toggle .toggle-btn {
      border-radius: 0;
      font-family: var(--app-font-mono);

      .toggle-text {
        letter-spacing: 1px;
      }
    }
  }

  .footer-info {
    font-family: var(--app-font-mono);
    letter-spacing: 1px;
  }
}
</style>
