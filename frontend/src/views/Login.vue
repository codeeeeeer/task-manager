<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>任务分发工具</h2>
      <el-form :model="loginForm" :rules="rules" ref="formRef">
        <el-form-item prop="email">
          <el-input
            v-model="loginForm.email"
            placeholder="邮箱"
            prefix-icon="Message"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
          />
        </el-form-item>
        <el-button
          type="primary"
          @click="handleLogin"
          :loading="loading"
          class="login-button"
        >
          登录
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

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
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    ElMessage.error(error.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);

  .login-card {
    width: 400px;
    padding: 20px;

    h2 {
      text-align: center;
      margin-bottom: 30px;
      color: #ff6b6b;
    }

    .login-button {
      width: 100%;
    }
  }
}
</style>
