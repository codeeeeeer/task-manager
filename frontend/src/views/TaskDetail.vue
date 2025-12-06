<template>
  <div class="task-detail">
    <div v-if="task">
      <h2>{{ task.title }}</h2>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="状态">{{ task.status }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ task.category }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ task.creator_name }}</el-descriptions-item>
        <el-descriptions-item label="当前处理人">{{ task.current_handler_name }}</el-descriptions-item>
        <el-descriptions-item label="进度">{{ task.progress }}%</el-descriptions-item>
        <el-descriptions-item label="时间进度">{{ task.time_progress }}%</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ task.description }}</el-descriptions-item>
      </el-descriptions>
    </div>
    <div v-else>
      <el-skeleton :rows="5" animated />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getTaskDetail } from '@/api/task'

const route = useRoute()
const task = ref(null)

const loadTask = async () => {
  try {
    const taskId = route.params.id
    task.value = await getTaskDetail(taskId)
  } catch (error) {
    console.error('加载任务详情失败:', error)
  }
}

onMounted(() => {
  loadTask()
})
</script>

<style scoped lang="scss">
.task-detail {
  padding: 20px;

  h2 {
    color: #ff6b6b;
    margin-bottom: 20px;
  }
}
</style>
