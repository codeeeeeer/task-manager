<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 统计概览卡片 -->
      <el-col :xs="24" :sm="12" :md="6" v-for="stat in overviewStats" :key="stat.key">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 16px">
      <!-- 状态分布图表 -->
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>
            <span>任务状态分布</span>
          </template>
          <div ref="statusChart" style="height: 240px"></div>
        </el-card>
      </el-col>

      <!-- 分类分布图表 -->
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>
            <span>任务分类分布</span>
          </template>
          <div ref="categoryChart" style="height: 240px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 16px">
      <!-- 我的待办任务 -->
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>
            <span>我的待办任务</span>
          </template>
          <el-empty v-if="!pendingTasks.length" description="暂无待办任务" />
          <div v-else class="task-list">
            <div v-for="task in pendingTasks" :key="task.id" class="task-item" @click="goToTask(task.id)">
              <div class="task-title">{{ task.title }}</div>
              <div class="task-meta">
                <el-tag size="small" :type="getStatusType(task.status)">{{ task.status }}</el-tag>
                <el-tag size="small" type="info">{{ task.category }}</el-tag>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 紧急任务提醒 -->
      <el-col :xs="24" :md="12">
        <el-card>
          <template #header>
            <span>紧急任务提醒</span>
          </template>
          <el-empty v-if="!urgentTasks.length" description="暂无紧急任务" />
          <div v-else class="task-list">
            <div v-for="task in urgentTasks" :key="task.id" class="task-item urgent" @click="goToTask(task.id)">
              <div class="task-title">
                <el-icon v-if="task.urgency === 'overdue'" color="#f56c6c"><WarningFilled /></el-icon>
                <el-icon v-else color="#e6a23c"><Warning /></el-icon>
                {{ task.title }}
              </div>
              <div class="task-meta">
                <el-tag size="small" :type="task.urgency === 'overdue' ? 'danger' : 'warning'">
                  {{ task.urgency === 'overdue' ? `逾期${task.overdue_days}天` : `剩余${task.remaining_hours}小时` }}
                </el-tag>
                <el-tag size="small" type="info">{{ task.category }}</el-tag>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { WarningFilled, Warning } from '@element-plus/icons-vue'
import { getTaskStatistics, getMyPendingTasks, getUrgentTasks } from '@/api/task'
import * as echarts from 'echarts'

const router = useRouter()

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

const loadStatistics = async () => {
  try {
    const stats = await getTaskStatistics()
    overviewStats.value[0].value = stats.total
    overviewStats.value[1].value = stats.status_distribution['待响应'] || 0
    overviewStats.value[2].value = stats.status_distribution['处理中'] || 0
    overviewStats.value[3].value = stats.status_distribution['已完成'] || 0

    // 更新图表
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

  const option = {
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: '60%',
      data: Object.entries(data).map(([name, value]) => ({ name, value })),
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
  statusChartInstance.setOption(option)
}

const updateCategoryChart = (data) => {
  if (!categoryChartInstance) {
    categoryChartInstance = echarts.init(categoryChart.value)
  }

  const option = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: { type: 'category', data: Object.keys(data) },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: Object.values(data),
      itemStyle: { color: '#409EFF' }
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

onMounted(() => {
  refreshData()

  window.addEventListener('resize', () => {
    statusChartInstance?.resize()
    categoryChartInstance?.resize()
  })

  // 监听任务变更事件，自动刷新统计数据
  if (window.socket) {
    window.socket.on('task_updated', refreshData)
    window.socket.on('task_created', refreshData)
    window.socket.on('task_transferred', refreshData)
  }
})

onUnmounted(() => {
  statusChartInstance?.dispose()
  categoryChartInstance?.dispose()

  // 移除socket监听
  if (window.socket) {
    window.socket.off('task_updated', refreshData)
    window.socket.off('task_created', refreshData)
    window.socket.off('task_transferred', refreshData)
  }
})
</script>

<style scoped lang="scss">
.dashboard {
  padding: 16px;

  :deep(.el-card__header) {
    font-weight: 600;
    font-size: 15px;
    color: #303133;
  }
}

.stat-card {
  .stat-content {
    text-align: center;
    .stat-value {
      font-size: 32px;
      font-weight: bold;
      color: #409EFF;
      margin-bottom: 8px;
    }
    .stat-label {
      font-size: 14px;
      color: #606266;
      font-weight: 500;
    }
  }
}

.task-list {
  max-height: 280px;
  overflow-y: auto;

  .task-item {
    padding: 12px;
    border-bottom: 1px solid #ebeef5;
    cursor: pointer;
    transition: background-color 0.3s;

    &:hover {
      background-color: #f5f7fa;
    }

    &:last-child {
      border-bottom: none;
    }

    .task-title {
      font-size: 14px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 4px;
      color: #303133;
      font-weight: 500;
    }

    .task-meta {
      display: flex;
      gap: 8px;
    }

    &.urgent {
      border-left: 3px solid #f56c6c;
    }
  }
}
</style>
