<template>
  <div class="dashboard">
    <!-- 统计概览卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6" v-for="(stat, index) in overviewStats" :key="stat.key">
        <div class="stat-card" :class="`stat-card-${index + 1}`">
          <div class="stat-icon">
            <el-icon :size="24">
              <component :is="statIcons[index]" />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
          <div class="stat-decoration"></div>
        </div>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :md="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span class="header-title">任务状态分布</span>
              <span class="header-badge">实时</span>
            </div>
          </template>
          <div ref="statusChart" class="chart-container"></div>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span class="header-title">任务分类分布</span>
              <span class="header-badge">统计</span>
            </div>
          </template>
          <div ref="categoryChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 任务列表区域 -->
    <el-row :gutter="20" class="tasks-row">
      <el-col :xs="24" :md="12">
        <el-card class="task-card">
          <template #header>
            <div class="card-header">
              <span class="header-title">我的待办任务</span>
              <el-tag size="small" type="primary">{{ pendingTasks.length }}</el-tag>
            </div>
          </template>
          <el-empty v-if="!pendingTasks.length" description="暂无待办任务" :image-size="80" />
          <div v-else class="task-list">
            <div
              v-for="task in pendingTasks"
              :key="task.id"
              class="task-item"
              @click="goToTask(task.id)"
            >
              <div class="task-content">
                <div class="task-title">{{ task.title }}</div>
                <div class="task-meta">
                  <el-tag size="small" :type="getStatusType(task.status)">{{ task.status }}</el-tag>
                  <el-tag size="small" type="info">{{ task.category }}</el-tag>
                </div>
              </div>
              <el-icon class="task-arrow"><ArrowRight /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <el-card class="task-card urgent-card">
          <template #header>
            <div class="card-header">
              <span class="header-title">紧急任务提醒</span>
              <el-tag size="small" type="danger">{{ urgentTasks.length }}</el-tag>
            </div>
          </template>
          <el-empty v-if="!urgentTasks.length" description="暂无紧急任务" :image-size="80" />
          <div v-else class="task-list">
            <div
              v-for="task in urgentTasks"
              :key="task.id"
              class="task-item urgent"
              @click="goToTask(task.id)"
            >
              <div class="task-indicator">
                <el-icon v-if="task.urgency === 'overdue'" class="indicator-icon danger"><WarningFilled /></el-icon>
                <el-icon v-else class="indicator-icon warning"><Warning /></el-icon>
              </div>
              <div class="task-content">
                <div class="task-title">{{ task.title }}</div>
                <div class="task-meta">
                  <el-tag size="small" :type="task.urgency === 'overdue' ? 'danger' : 'warning'">
                    {{ task.urgency === 'overdue' ? `逾期${task.overdue_days}天` : `剩余${task.remaining_hours}小时` }}
                  </el-tag>
                  <el-tag size="small" type="info">{{ task.category }}</el-tag>
                </div>
              </div>
              <el-icon class="task-arrow"><ArrowRight /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { WarningFilled, Warning, ArrowRight, Document, Clock, Check, List } from '@element-plus/icons-vue'
import { getTaskStatistics, getMyPendingTasks, getUrgentTasks } from '@/api/task'
import { useThemeStore } from '@/store/theme'
import * as echarts from 'echarts'

const router = useRouter()
const themeStore = useThemeStore()

const statIcons = [Document, Clock, List, Check]

const overviewStats = ref([
  { key: 'total', label: '总任务数', value: 0 },
  { key: 'pending', label: '待响应', value: 0 },
  { key: 'processing', label: '处理中', value: 0 },
  { key: 'completed', label: '已完成', value: 0 }
])

const pendingTasks = ref([])
const urgentTasks = ref([])
const statusChart = ref(null)
const categoryChart = ref(null)
let statusChartInstance = null
let categoryChartInstance = null

const isTechTheme = computed(() => themeStore.currentTheme === 'tech')

const getChartColors = () => {
  if (isTechTheme.value) {
    return {
      primary: '#06b6d4',
      success: '#4ade80',
      warning: '#facc15',
      danger: '#f43f5e',
      info: '#94a3b8',
      text: '#cbd5e1',
      bg: 'transparent'
    }
  }
  return {
    primary: '#3b82f6',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#6b7280',
    text: '#374151',
    bg: '#ffffff'
  }
}

const loadStatistics = async () => {
  try {
    const stats = await getTaskStatistics()
    overviewStats.value[0].value = stats.total
    overviewStats.value[1].value = stats.status_distribution['待响应'] || 0
    overviewStats.value[2].value = stats.status_distribution['处理中'] || 0
    overviewStats.value[3].value = stats.status_distribution['已完成'] || 0

    updateStatusChart(stats.status_distribution)
    updateCategoryChart(stats.category_distribution)
  } catch (error) {
    ElMessage.error('加载统计数据失败')
  }
}

const loadPendingTasks = async () => {
  try {
    const tasks = await getMyPendingTasks(10)
    pendingTasks.value = tasks
  } catch (error) {
    ElMessage.error('加载待办任务失败')
  }
}

const loadUrgentTasks = async () => {
  try {
    const tasks = await getUrgentTasks(24)
    urgentTasks.value = tasks
  } catch (error) {
    ElMessage.error('加载紧急任务失败')
  }
}

const updateStatusChart = (data) => {
  if (!statusChartInstance) {
    statusChartInstance = echarts.init(statusChart.value)
  }

  const colors = getChartColors()
  const colorMap = {
    '新建': colors.info,
    '待响应': colors.warning,
    '处理中': colors.primary,
    '挂起': colors.danger,
    '已完成': colors.success,
    '关闭': colors.info
  }

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: isTechTheme.value ? 'rgba(30, 41, 59, 0.95)' : '#fff',
      borderColor: isTechTheme.value ? 'rgba(6, 182, 212, 0.3)' : '#e5e7eb',
      textStyle: { color: colors.text }
    },
    legend: {
      bottom: '5%',
      textStyle: { color: colors.text, fontSize: 12 }
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: isTechTheme.value ? 0 : 8,
        borderColor: isTechTheme.value ? 'rgba(6, 182, 212, 0.2)' : '#fff',
        borderWidth: 2
      },
      label: { show: false },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: 'bold' },
        itemStyle: {
          shadowBlur: isTechTheme.value ? 20 : 10,
          shadowColor: isTechTheme.value ? 'rgba(6, 182, 212, 0.5)' : 'rgba(0, 0, 0, 0.2)'
        }
      },
      data: Object.entries(data).map(([name, value]) => ({
        name,
        value,
        itemStyle: { color: colorMap[name] || colors.info }
      }))
    }]
  }
  statusChartInstance.setOption(option)
}

const updateCategoryChart = (data) => {
  if (!categoryChartInstance) {
    categoryChartInstance = echarts.init(categoryChart.value)
  }

  const colors = getChartColors()

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: isTechTheme.value ? 'rgba(30, 41, 59, 0.95)' : '#fff',
      borderColor: isTechTheme.value ? 'rgba(6, 182, 212, 0.3)' : '#e5e7eb',
      textStyle: { color: colors.text }
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: Object.keys(data),
      axisLine: { lineStyle: { color: isTechTheme.value ? 'rgba(6, 182, 212, 0.3)' : '#e5e7eb' } },
      axisLabel: { color: colors.text, fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: isTechTheme.value ? 'rgba(6, 182, 212, 0.1)' : '#f3f4f6' } },
      axisLabel: { color: colors.text }
    },
    series: [{
      type: 'bar',
      data: Object.values(data),
      barWidth: '50%',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: colors.primary },
          { offset: 1, color: isTechTheme.value ? 'rgba(6, 182, 212, 0.3)' : 'rgba(59, 130, 246, 0.3)' }
        ]),
        borderRadius: isTechTheme.value ? 0 : [4, 4, 0, 0]
      },
      emphasis: {
        itemStyle: {
          shadowBlur: isTechTheme.value ? 15 : 5,
          shadowColor: isTechTheme.value ? 'rgba(6, 182, 212, 0.5)' : 'rgba(59, 130, 246, 0.3)'
        }
      }
    }]
  }
  categoryChartInstance.setOption(option)
}

const getStatusType = (status) => {
  const typeMap = {
    '新建': 'info',
    '待响应': 'warning',
    '处理中': 'primary',
    '挂起': 'info',
    '已完成': 'success',
    '关闭': 'info'
  }
  return typeMap[status] || 'info'
}

const goToTask = (taskId) => {
  router.push(`/tasks/${taskId}`)
}

const refreshData = () => {
  loadStatistics()
  loadPendingTasks()
  loadUrgentTasks()
}

const handleResize = () => {
  statusChartInstance?.resize()
  categoryChartInstance?.resize()
}

onMounted(() => {
  refreshData()
  window.addEventListener('resize', handleResize)

  if (window.socket) {
    window.socket.on('task_updated', refreshData)
    window.socket.on('task_created', refreshData)
    window.socket.on('task_transferred', refreshData)
  }
})

onUnmounted(() => {
  statusChartInstance?.dispose()
  categoryChartInstance?.dispose()
  window.removeEventListener('resize', handleResize)

  if (window.socket) {
    window.socket.off('task_updated', refreshData)
    window.socket.off('task_created', refreshData)
    window.socket.off('task_transferred', refreshData)
  }
})
</script>

<style scoped lang="scss">
.dashboard {
  padding: 0;
}

// ==================== 统计卡片 ====================
.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  position: relative;
  padding: 24px;
  background: var(--el-bg-color-overlay);
  border-radius: var(--app-card-radius);
  border: 1px solid var(--el-border-color-light);
  box-shadow: var(--app-shadow);
  display: flex;
  align-items: center;
  gap: 16px;
  overflow: hidden;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--app-shadow-lg);
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    flex-shrink: 0;
  }

  .stat-info {
    flex: 1;
    min-width: 0;

    .stat-value {
      font-size: 28px;
      font-weight: 700;
      color: var(--el-text-color-primary);
      line-height: 1.2;
    }

    .stat-label {
      font-size: 13px;
      color: var(--el-text-color-secondary);
      margin-top: 4px;
    }
  }

  .stat-decoration {
    position: absolute;
    right: -20px;
    bottom: -20px;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    opacity: 0.1;
  }

  &.stat-card-1 {
    .stat-icon { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
    .stat-decoration { background: #3b82f6; }
  }

  &.stat-card-2 {
    .stat-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }
    .stat-decoration { background: #f59e0b; }
  }

  &.stat-card-3 {
    .stat-icon { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
    .stat-decoration { background: #8b5cf6; }
  }

  &.stat-card-4 {
    .stat-icon { background: linear-gradient(135deg, #10b981, #059669); }
    .stat-decoration { background: #10b981; }
  }
}

// ==================== 图表卡片 ====================
.charts-row {
  margin-bottom: 24px;
}

.chart-card {
  height: 100%;

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .header-title {
      font-weight: 600;
      color: var(--el-text-color-primary);
    }

    .header-badge {
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 10px;
      background: var(--el-color-primary-light-9);
      color: var(--el-color-primary);
    }
  }

  .chart-container {
    height: 280px;
  }
}

// ==================== 任务列表卡片 ====================
.tasks-row {
  margin-bottom: 0;
}

.task-card {
  height: 100%;

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .header-title {
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
  }

  .task-list {
    max-height: 320px;
    overflow-y: auto;
  }

  .task-item {
    display: flex;
    align-items: center;
    padding: 14px 16px;
    margin: 0 -20px;
    cursor: pointer;
    transition: all 0.2s ease;
    border-bottom: 1px solid var(--el-border-color-lighter);

    &:last-child {
      border-bottom: none;
    }

    &:hover {
      background: var(--el-color-primary-light-9);

      .task-arrow {
        opacity: 1;
        transform: translateX(0);
      }
    }

    .task-indicator {
      margin-right: 12px;

      .indicator-icon {
        font-size: 20px;

        &.danger { color: var(--el-color-danger); }
        &.warning { color: var(--el-color-warning); }
      }
    }

    .task-content {
      flex: 1;
      min-width: 0;

      .task-title {
        font-size: 14px;
        font-weight: 500;
        color: var(--el-text-color-primary);
        margin-bottom: 8px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .task-meta {
        display: flex;
        gap: 8px;
      }
    }

    .task-arrow {
      color: var(--el-text-color-secondary);
      opacity: 0;
      transform: translateX(-8px);
      transition: all 0.2s ease;
    }

    &.urgent {
      border-left: 3px solid var(--el-color-danger);
      margin-left: -20px;
      padding-left: 17px;
    }
  }
}

// ==================== 高科技主题 ====================
:global(html.theme-tech) {
  .stat-card {
    background: rgba(30, 41, 59, 0.85);
    backdrop-filter: blur(12px);
    border-radius: 2px;
    border-color: var(--el-border-color);

    &:hover {
      border-color: var(--el-color-primary);
      box-shadow: var(--app-shadow-lg);
    }

    .stat-icon {
      border-radius: 0;
    }

    .stat-value {
      font-family: var(--app-font-mono);
      text-shadow: 0 0 20px rgba(6, 182, 212, 0.3);
    }

    .stat-label {
      font-family: var(--app-font-mono);
      text-transform: uppercase;
      letter-spacing: 1px;
      font-size: 11px;
    }

    &.stat-card-1 {
      .stat-icon {
        background: linear-gradient(135deg, #06b6d4, #0891b2);
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
      }
      .stat-decoration { background: #06b6d4; }
    }

    &.stat-card-2 {
      .stat-icon {
        background: linear-gradient(135deg, #facc15, #eab308);
        box-shadow: 0 0 15px rgba(250, 204, 21, 0.4);
      }
      .stat-decoration { background: #facc15; }
    }

    &.stat-card-3 {
      .stat-icon {
        background: linear-gradient(135deg, #a78bfa, #8b5cf6);
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
      }
      .stat-decoration { background: #8b5cf6; }
    }

    &.stat-card-4 {
      .stat-icon {
        background: linear-gradient(135deg, #4ade80, #22c55e);
        box-shadow: 0 0 15px rgba(74, 222, 128, 0.4);
      }
      .stat-decoration { background: #4ade80; }
    }
  }

  .chart-card {
    .header-badge {
      border-radius: 0;
      font-family: var(--app-font-mono);
      letter-spacing: 1px;
    }
  }

  .task-card {
    .task-item {
      &:hover {
        background: rgba(6, 182, 212, 0.08);
      }

      .task-title {
        font-family: var(--app-font-mono);
      }

      &.urgent {
        border-left-color: var(--el-color-danger);
        box-shadow: inset 3px 0 15px rgba(244, 63, 94, 0.2);
      }
    }
  }
}
</style>
