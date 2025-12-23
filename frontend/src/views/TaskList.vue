<template>
  <div class="task-list">
    <div class="header">
      <h2>任务列表</h2>
      <div>
        <el-button type="success" @click="downloadClient">下载Chrome插件</el-button>
        <el-button type="warning" @click="exportTasks">导出任务</el-button>
        <el-button type="primary" @click="showCreateDialog = true">新建任务</el-button>
      </div>
    </div>

    <!-- 搜索筛选区 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="任务标题">
          <el-input v-model="filters.search" placeholder="请输入任务标题" clearable style="width: 200px" />
        </el-form-item>

        <el-form-item label="任务状态">
          <el-select v-model="filters.status" placeholder="请选择状态" clearable style="width: 150px">
            <el-option label="新建" value="新建" />
            <el-option label="待响应" value="待响应" />
            <el-option label="处理中" value="处理中" />
            <el-option label="挂起" value="挂起" />
            <el-option label="已完成" value="已完成" />
            <el-option label="关闭" value="关闭" />
          </el-select>
        </el-form-item>

        <el-form-item label="任务分类">
          <el-select v-model="filters.category" placeholder="请选择分类" clearable style="width: 150px">
            <el-option label="版本任务" value="版本任务" />
            <el-option label="紧急任务" value="紧急任务" />
            <el-option label="其他任务" value="其他任务" />
            <el-option label="定时周期任务" value="定时周期任务" />
            <el-option label="普通任务" value="普通任务" />
          </el-select>
        </el-form-item>

        <el-form-item label="创建人">
          <el-select v-model="filters.creator_id" placeholder="请选择创建人" clearable filterable style="width: 150px">
            <el-option
              v-for="user in userList"
              :key="user.id"
              :label="`${user.name} (${user.um_code})`"
              :value="user.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="当前处理人">
          <el-select v-model="filters.current_handler_id" placeholder="请选择处理人" clearable filterable style="width: 150px">
            <el-option
              v-for="user in userList"
              :key="user.id"
              :label="`${user.name} (${user.um_code})`"
              :value="user.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" @click="handleMyTasks">我的任务</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 任务列表 -->
    <el-table :data="tasks" v-loading="loading" style="width: 100%; margin-top: 20px">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="任务标题" min-width="200">
        <template #default="scope">
          <el-link type="primary" @click="viewDetail(scope.row.id)">{{ scope.row.title }}</el-link>
        </template>
      </el-table-column>
      <el-table-column prop="category" label="任务分类" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="creator_name" label="创建人" width="120" />
      <el-table-column prop="current_handler_name" label="当前处理人" width="120" />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="scope">
          <el-button size="small" type="primary" link @click="viewDetail(scope.row.id)">查看</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="pagination.page"
      v-model:page-size="pagination.per_page"
      :page-sizes="[10, 20, 50, 100]"
      :total="pagination.total"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSearch"
      @current-change="loadTasks"
      style="margin-top: 20px; justify-content: flex-end"
    />

    <!-- 新建任务对话框 -->
    <el-dialog v-model="showCreateDialog" title="新建任务" width="700px" @close="resetCreateForm">
      <el-form :model="createForm" :rules="createRules" ref="createFormRef" label-width="120px">
        <el-form-item label="任务标题" prop="title">
          <el-input v-model="createForm.title" placeholder="请输入任务标题" />
        </el-form-item>

        <el-form-item label="任务分类" prop="category">
          <el-select v-model="createForm.category" placeholder="请选择分类" style="width: 100%">
            <el-option label="版本任务" value="版本任务" />
            <el-option label="紧急任务" value="紧急任务" />
            <el-option label="其他任务" value="其他任务" />
            <el-option label="定时周期任务" value="定时周期任务" />
            <el-option label="普通任务" value="普通任务" />
          </el-select>
        </el-form-item>

        <el-form-item label="当前处理人" prop="current_handler_id">
          <el-select v-model="createForm.current_handler_id" placeholder="请选择处理人" filterable style="width: 100%">
            <el-option
              v-for="user in userList"
              :key="user.id"
              :label="`${user.name} (${user.um_code})`"
              :value="user.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="期望开始时间">
          <el-date-picker
            v-model="createForm.expected_start_time"
            type="datetime"
            placeholder="请选择期望开始时间"
            format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="期望完成时间">
          <el-date-picker
            v-model="createForm.expected_end_time"
            type="datetime"
            placeholder="请选择期望完成时间"
            format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="任务描述">
          <div style="width: 100%;">
            <QuillEditor v-model:content="createForm.description" contentType="html" theme="snow" />
          </div>
        </el-form-item>

        <el-form-item label="附件">
          <el-upload
            v-model:file-list="createForm.attachments"
            :auto-upload="false"
            multiple
            :limit="10"
          >
            <el-button size="small">选择文件</el-button>
          </el-upload>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate" :loading="creating">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getTasks, createTask, uploadAttachment } from '@/api/task'
import { getAllUsers } from '@/api/user'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()

// 数据
const tasks = ref([])
const userList = ref([])
const loading = ref(false)
const creating = ref(false)
const showCreateDialog = ref(false)
const createFormRef = ref(null)

// 筛选条件
const filters = reactive({
  search: '',
  status: '',
  category: '',
  creator_id: null,
  current_handler_id: null
})

// 分页
const pagination = reactive({
  page: 1,
  per_page: 20,
  total: 0
})

// 创建任务表单
const createForm = reactive({
  title: '',
  category: '',
  description: '',
  current_handler_id: null,
  expected_start_time: null,
  expected_end_time: null,
  attachments: []
})

// 表单验证规则
const createRules = {
  title: [{ required: true, message: '请输入任务标题', trigger: 'blur' }],
  category: [{ required: true, message: '请选择任务分类', trigger: 'change' }],
  current_handler_id: [{ required: true, message: '请选择当前处理人', trigger: 'change' }]
}

// 加载用户列表
const loadUsers = async () => {
  try {
    const res = await getAllUsers()
    userList.value = res || []
  } catch (error) {
    console.error('加载用户列表失败:', error)
  }
}

// 加载任务列表
const loadTasks = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      per_page: pagination.per_page,
      ...filters
    }

    // 移除空值
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null) {
        delete params[key]
      }
    })

    const res = await getTasks(params)
    tasks.value = res.tasks || []
    pagination.total = res.total || 0
  } catch (error) {
    console.error('加载任务失败:', error)
    ElMessage.error('加载任务列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadTasks()
}

// 重置
const handleReset = () => {
  filters.search = ''
  filters.status = ''
  filters.category = ''
  filters.creator_id = null
  filters.current_handler_id = null
  pagination.page = 1
  loadTasks()
}

// 我的任务
const handleMyTasks = () => {
  filters.search = ''
  filters.status = ''
  filters.category = ''
  filters.creator_id = null
  filters.current_handler_id = authStore.currentUserId
  pagination.page = 1
  loadTasks()
}

// 创建任务
const handleCreate = async () => {
  try {
    await createFormRef.value.validate()
    creating.value = true

    const data = {
      title: createForm.title,
      category: createForm.category,
      description: createForm.description,
      current_handler_id: createForm.current_handler_id,
      expected_start_time: createForm.expected_start_time?.toISOString(),
      expected_end_time: createForm.expected_end_time?.toISOString()
    }

    const task = await createTask(data)

    // 上传附件
    if (createForm.attachments.length > 0) {
      for (const fileItem of createForm.attachments) {
        await uploadAttachment(task.id, fileItem.raw)
      }
    }

    ElMessage.success('任务创建成功')
    showCreateDialog.value = false
    loadTasks()
  } catch (error) {
    if (error !== false) {
      console.error('创建任务失败:', error)
      ElMessage.error('创建任务失败')
    }
  } finally {
    creating.value = false
  }
}

// 重置创建表单
const resetCreateForm = () => {
  createFormRef.value?.resetFields()
  createForm.title = ''
  createForm.category = ''
  createForm.description = ''
  createForm.current_handler_id = null
  createForm.expected_start_time = null
  createForm.expected_end_time = null
  createForm.attachments = []
}

// 查看详情
const viewDetail = (taskId) => {
  router.push(`/tasks/${taskId}`)
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}

// 获取状态标签类型
const getStatusType = (status) => {
  const typeMap = {
    '新建': 'info',
    '待响应': 'warning',
    '处理中': 'primary',
    '挂起': 'danger',
    '已完成': 'success',
    '关闭': 'info'
  }
  return typeMap[status] || 'info'
}

// 下载Chrome插件
const downloadClient = () => {
  const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'
  window.open(`${baseURL}/tasks/download-client`, '_blank')
}

// 导出任务
const exportTasks = () => {
  if (tasks.value.length === 0) {
    ElMessage.warning('当前没有可导出的任务')
    return
  }

  const headers = ['ID', '任务标题', '任务分类', '状态', '创建人', '当前处理人', '创建时间']
  const csvContent = [
    headers.join(','),
    ...tasks.value.map(task => [
      task.id,
      `"${task.title.replace(/"/g, '""')}"`,
      task.category,
      task.status,
      task.creator_name || '-',
      task.current_handler_name || '-',
      formatDate(task.created_at)
    ].join(','))
  ].join('\n')

  const BOM = '\uFEFF'
  const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `任务列表_${new Date().toISOString().slice(0, 10)}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  ElMessage.success('任务导出成功')
}

onMounted(() => {
  loadUsers()
  loadTasks()
})
</script>

<style scoped lang="scss">
.task-list {
  padding: 20px;

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      color: #ff6b6b;
      margin: 0;
    }
  }

  .filter-card {
    :deep(.el-card__body) {
      padding: 15px;
    }

    .filter-form {
      :deep(.el-form-item) {
        margin-bottom: 10px;
      }
    }
  }

  :deep(.el-table) {
    .el-link {
      font-weight: 500;
    }
  }

  :deep(.el-pagination) {
    display: flex;
  }

  :deep(.el-dialog__body) {
    .ql-editor {
      min-height: 200px;
    }
  }
}
</style>
