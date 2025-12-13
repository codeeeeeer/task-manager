<template>
  <div class="task-detail">
    <div v-if="task">
      <h2>{{ task.title }}</h2>

      <div class="action-buttons" v-if="canRespond || canTransfer || canSuspend || canComplete || canClose || canEdit">
        <el-button v-if="canRespond" type="primary" @click="handleRespond">响应</el-button>
        <el-button v-if="canEdit" type="primary" @click="showProgressDialog = true">更新进度</el-button>
        <el-button v-if="canTransfer" type="warning" @click="showTransferDialog = true">转派</el-button>
        <el-button v-if="canSuspend" type="info" @click="handleSuspend">挂起</el-button>
        <el-button v-if="canComplete" type="success" @click="handleComplete">完成</el-button>
        <el-button v-if="canClose" type="danger" @click="handleClose">关闭</el-button>
      </div>

      <el-descriptions :column="2" border class="task-info">
        <el-descriptions-item label="创建时间">{{ formatTime(task.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ task.creator_name }}</el-descriptions-item>
        <el-descriptions-item label="状态">{{ task.status }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ task.category }}</el-descriptions-item>
        <el-descriptions-item label="当前处理人">{{ task.current_handler_name }}</el-descriptions-item>
        <el-descriptions-item label="进度">{{ task.progress }}%</el-descriptions-item>
        <el-descriptions-item label="时间进度">{{ task.time_progress }}%</el-descriptions-item>
        <el-descriptions-item label="期望开始时间">{{ formatTime(task.expected_start_time) }}</el-descriptions-item>
        <el-descriptions-item label="期望完成时间">{{ formatTime(task.expected_end_time) }}</el-descriptions-item>
      </el-descriptions>

      <div class="task-description">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
          <h3 style="margin: 0;">任务描述</h3>
          <el-button v-if="canEdit && !isEditingDesc" size="small" @click="startEditDesc">编辑</el-button>
          <div v-if="isEditingDesc">
            <el-button size="small" @click="cancelEditDesc">取消</el-button>
            <el-button size="small" type="primary" @click="saveDesc">保存</el-button>
          </div>
        </div>
        <div v-if="!isEditingDesc" class="description-content" v-html="task.description"></div>
        <QuillEditor v-else v-model:content="editDesc" contentType="html" theme="snow" style="height: 300px" />
      </div>

      <div class="task-transfers">
        <h3>流转记录</h3>
        <el-timeline>
          <el-timeline-item v-for="transfer in transfers" :key="transfer.id" :timestamp="formatTime(transfer.created_at)">
            <p><strong>{{ transfer.operator_name }}</strong> {{ transfer.transfer_type }}
              <span v-if="transfer.target_user_name">→ {{ transfer.target_user_name }}</span>
            </p>
            <p v-if="transfer.message" class="transfer-message">{{ transfer.message }}</p>
          </el-timeline-item>
        </el-timeline>
      </div>

      <div class="task-attachments">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
          <h3 style="margin: 0;">附件</h3>
          <el-upload
            v-if="canEdit"
            :show-file-list="false"
            :before-upload="handleUpload"
            :auto-upload="false"
            :on-change="handleFileChange"
          >
            <el-button size="small" type="primary">上传附件</el-button>
          </el-upload>
        </div>
        <el-table :data="attachments" style="width: 100%">
          <el-table-column prop="file_name" label="文件名" />
          <el-table-column prop="file_size" label="大小" width="120">
            <template #default="scope">{{ formatFileSize(scope.row.file_size) }}</template>
          </el-table-column>
          <el-table-column prop="uploader_name" label="上传人" width="120" />
          <el-table-column prop="created_at" label="上传时间" width="180">
            <template #default="scope">{{ formatTime(scope.row.created_at) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button size="small" type="primary" link @click="handleDownload(scope.row)">下载</el-button>
              <el-button v-if="canEdit" size="small" type="danger" link @click="handleDeleteAttachment(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="task-comments">
        <h3>任务留言</h3>
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <strong>{{ comment.user_name }}</strong>
            <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
          </div>
          <div class="comment-content">{{ comment.content }}</div>
        </div>

        <div class="comment-input">
          <el-input v-model="newComment" type="textarea" :rows="3" placeholder="输入留言内容" />
          <el-button type="primary" @click="handleAddComment" :disabled="!newComment.trim()">发表留言</el-button>
        </div>
      </div>
    </div>
    <div v-else>
      <el-skeleton :rows="5" animated />
    </div>

    <el-dialog v-model="showTransferDialog" title="流转任务" width="500px">
      <el-form :model="transferForm" label-width="100px">
        <el-form-item label="目标用户">
          <el-select v-model="transferForm.target_user_id" placeholder="请选择目标用户" style="width: 100%">
            <el-option v-for="user in users" :key="user.id" :label="user.name" :value="user.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="流转说明">
          <el-input v-model="transferForm.message" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showTransferDialog = false">取消</el-button>
        <el-button type="primary" @click="handleTransfer">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showProgressDialog" title="更新进度" width="400px">
      <el-form label-width="80px">
        <el-form-item label="当前进度">
          <el-slider v-model="progressValue" :marks="{ 0: '0%', 25: '25%', 50: '50%', 75: '75%', 100: '100%' }" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showProgressDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUpdateProgress">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getTaskDetail, respondTask, transferTask, suspendTask, completeTask, closeTask, getTaskTransfers, getTaskComments, createComment, updateTask, getAttachments, uploadAttachment, deleteAttachment, downloadAttachment } from '@/api/task'
import { getUsers } from '@/api/user'
import { getToken } from '@/utils/auth'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const route = useRoute()
const task = ref(null)
const transfers = ref([])
const comments = ref([])
const attachments = ref([])
const users = ref([])
const newComment = ref('')
const showTransferDialog = ref(false)
const transferForm = ref({ target_user_id: null, message: '' })
const showProgressDialog = ref(false)
const progressValue = ref(0)
const isEditingDesc = ref(false)
const editDesc = ref('')

const currentUser = computed(() => JSON.parse(localStorage.getItem('user_info') || '{}'))

const canRespond = computed(() => {
  if (!task.value) return false
  return task.value.current_handler_id === currentUser.value.id &&
    ['新建', '待响应', '挂起'].includes(task.value.status)
})

const canTransfer = computed(() => {
  if (!task.value) return false
  return (task.value.current_handler_id === currentUser.value.id || currentUser.value.is_admin) &&
    !['已完成', '关闭'].includes(task.value.status)
})

const canSuspend = computed(() => {
  if (!task.value) return false
  return (task.value.current_handler_id === currentUser.value.id || currentUser.value.is_admin) &&
    task.value.status === '处理中'
})

const canComplete = computed(() => {
  if (!task.value) return false
  return (task.value.current_handler_id === currentUser.value.id || currentUser.value.is_admin) &&
    !['已完成', '关闭'].includes(task.value.status)
})

const canClose = computed(() => {
  if (!task.value) return false
  return (task.value.current_handler_id === currentUser.value.id || currentUser.value.is_admin) &&
    task.value.status !== '关闭'
})

const canEdit = computed(() => {
  if (!task.value) return false
  return task.value.current_handler_id === currentUser.value.id || currentUser.value.is_admin
})

const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const loadTask = async () => {
  try {
    const taskId = route.params.id
    task.value = await getTaskDetail(taskId)
    progressValue.value = task.value.progress || 0
  } catch (error) {
    ElMessage.error('加载任务详情失败')
  }
}

const loadTransfers = async () => {
  try {
    const taskId = route.params.id
    transfers.value = await getTaskTransfers(taskId)
  } catch (error) {
    ElMessage.error('加载流转记录失败')
  }
}

const loadComments = async () => {
  try {
    const taskId = route.params.id
    comments.value = await getTaskComments(taskId)
  } catch (error) {
    ElMessage.error('加载留言失败')
  }
}

const loadUsers = async () => {
  try {
    const result = await getUsers({ page: 1, per_page: 1000 })
    users.value = result.users
  } catch (error) {
    ElMessage.error('加载用户列表失败')
  }
}

const loadAttachments = async () => {
  try {
    const taskId = route.params.id
    attachments.value = await getAttachments(taskId)
  } catch (error) {
    ElMessage.error('加载附件失败')
  }
}

const handleRespond = async () => {
  try {
    await respondTask(route.params.id)
    ElMessage.success('任务已响应')
    await loadTask()
    await loadTransfers()
  } catch (error) {
    ElMessage.error(error.message || '响应失败')
  }
}

const handleTransfer = async () => {
  if (!transferForm.value.target_user_id) {
    ElMessage.warning('请选择目标用户')
    return
  }
  try {
    await transferTask(route.params.id, transferForm.value)
    ElMessage.success('任务已流转')
    showTransferDialog.value = false
    transferForm.value = { target_user_id: null, message: '' }
    await loadTask()
    await loadTransfers()
  } catch (error) {
    ElMessage.error(error.message || '流转失败')
  }
}

const handleUpdateProgress = async () => {
  try {
    await updateTask(route.params.id, { progress: progressValue.value })
    ElMessage.success('进度更新成功')
    showProgressDialog.value = false
    await loadTask()
  } catch (error) {
    ElMessage.error(error.message || '更新失败')
  }
}

const handleSuspend = async () => {
  try {
    await suspendTask(route.params.id, {})
    ElMessage.success('任务已挂起')
    await loadTask()
    await loadTransfers()
  } catch (error) {
    ElMessage.error(error.message || '挂起失败')
  }
}

const handleComplete = async () => {
  try {
    await completeTask(route.params.id, {})
    ElMessage.success('任务已完成')
    await loadTask()
    await loadTransfers()
  } catch (error) {
    ElMessage.error(error.message || '完成失败')
  }
}

const handleClose = async () => {
  try {
    await closeTask(route.params.id, {})
    ElMessage.success('任务已关闭')
    await loadTask()
    await loadTransfers()
  } catch (error) {
    ElMessage.error(error.message || '关闭失败')
  }
}

const handleAddComment = async () => {
  if (!newComment.value.trim()) return
  try {
    await createComment(route.params.id, { content: newComment.value })
    ElMessage.success('留言成功')
    newComment.value = ''
    await loadComments()
  } catch (error) {
    ElMessage.error(error.message || '留言失败')
  }
}

const startEditDesc = () => {
  editDesc.value = task.value.description || ''
  isEditingDesc.value = true
}

const cancelEditDesc = () => {
  isEditingDesc.value = false
  editDesc.value = ''
}

const saveDesc = async () => {
  try {
    await updateTask(route.params.id, { description: editDesc.value })
    ElMessage.success('任务描述已更新')
    isEditingDesc.value = false
    await loadTask()
  } catch (error) {
    ElMessage.error(error.message || '更新失败')
  }
}

const handleFileChange = async (file) => {
  try {
    await uploadAttachment(route.params.id, file.raw)
    ElMessage.success('附件上传成功')
    await loadAttachments()
  } catch (error) {
    ElMessage.error(error.message || '上传失败')
  }
}

const handleUpload = () => {
  return false
}

const handleDownload = (attachment) => {
  const token = getToken()
  if (!token) {
    ElMessage.error('请先登录')
    return
  }
  const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'
  const url = `${baseURL}/tasks/${route.params.id}/attachments/${attachment.id}/download`
  fetch(url, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
    .then(res => {
      if (!res.ok) {
        return res.json().then(err => { throw new Error(err.msg || err.message || '下载失败') })
      }
      return res.blob()
    })
    .then(blob => {
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = attachment.file_name
      a.click()
      window.URL.revokeObjectURL(url)
    })
    .catch(err => ElMessage.error(err.message || '下载失败'))
}

const handleDeleteAttachment = async (attachment) => {
  try {
    await deleteAttachment(route.params.id, attachment.id)
    ElMessage.success('附件删除成功')
    await loadAttachments()
  } catch (error) {
    ElMessage.error(error.message || '删除失败')
  }
}

onMounted(() => {
  loadTask()
  loadTransfers()
  loadComments()
  loadUsers()
  loadAttachments()
})
</script>

<style scoped lang="scss">
.task-detail {
  padding: 20px;

  h2 {
    color: #ff6b6b;
    margin-bottom: 20px;
  }

  .action-buttons {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
  }

  .task-info {
    margin-bottom: 30px;
  }

  .task-description {
    margin-bottom: 30px;

    h3 {
      color: #ff8c42;
      margin-bottom: 15px;
      font-size: 18px;
    }

    .description-content {
      padding: 15px;
      line-height: 1.6;
      min-height: 100px;
    }

    :deep(.ql-container) {
      height: 300px;
    }
  }

  .task-transfers {
    margin-bottom: 30px;

    h3 {
      color: #ff8c42;
      margin-bottom: 15px;
      font-size: 18px;
    }

    .transfer-message {
      color: #666;
      margin-top: 5px;
      font-size: 14px;
    }
  }

  .task-attachments {
    margin-bottom: 30px;

    h3 {
      color: #ff8c42;
      margin-bottom: 15px;
      font-size: 18px;
    }
  }

  .task-comments {
    h3 {
      color: #ff8c42;
      margin-bottom: 15px;
      font-size: 18px;
    }

    .comment-item {
      padding: 15px;
      margin-bottom: 15px;

      .comment-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;

        .comment-time {
          color: #999;
          font-size: 12px;
        }
      }

      .comment-content {
        line-height: 1.6;
        white-space: pre-wrap;
      }
    }

    .comment-input {
      margin-top: 20px;

      .el-button {
        margin-top: 10px;
      }
    }
  }
}
</style>
