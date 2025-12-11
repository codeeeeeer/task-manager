import { defineStore } from 'pinia'

const THEME_KEY = 'task_manager_theme'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    currentTheme: localStorage.getItem(THEME_KEY) || 'light'
  }),

  actions: {
    setTheme(theme) {
      this.currentTheme = theme
      localStorage.setItem(THEME_KEY, theme)
      document.documentElement.className = `theme-${theme}`
    },

    toggleTheme() {
      const newTheme = this.currentTheme === 'light' ? 'tech' : 'light'
      this.setTheme(newTheme)
    },

    initTheme() {
      document.documentElement.className = `theme-${this.currentTheme}`
    }
  }
})
