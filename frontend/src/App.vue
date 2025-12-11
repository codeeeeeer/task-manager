<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useThemeStore } from '@/store/theme'
import websocketClient from '@/utils/websocket'

const authStore = useAuthStore()
const themeStore = useThemeStore()

onMounted(() => {
  // 初始化主题
  themeStore.initTheme()

  // 如果已登录，连接WebSocket
  if (authStore.isLoggedIn) {
    websocketClient.connect()
  }
})
</script>

<style lang="scss">
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
