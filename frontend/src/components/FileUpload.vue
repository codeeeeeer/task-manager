<template>
  <div class="file-upload">
    <el-upload
      ref="uploadRef"
      :action="uploadUrl"
      :headers="headers"
      :on-success="handleSuccess"
      :on-error="handleError"
      :on-remove="handleRemove"
      :file-list="fileList"
      :limit="limit"
      :on-exceed="handleExceed"
      :before-upload="beforeUpload"
      multiple
    >
      <el-button type="primary" :icon="Upload">上传附件</el-button>
      <template #tip>
        <div class="el-upload__tip">
          支持扩展名：{{ accept }}，单个文件不超过 {{ maxSize }}MB
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import { getToken } from '@/utils/auth'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  limit: {
    type: Number,
    default: 10
  },
  maxSize: {
    type: Number,
    default: 50 // MB
  },
  accept: {
    type: String,
    default: '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.jpg,.jpeg,.png,.gif,.zip,.rar'
  }
})

const emit = defineEmits(['update:modelValue'])

const uploadRef = ref()
const fileList = ref([])

// 上传URL
const uploadUrl = computed(() => {
  return import.meta.env.VITE_API_BASE_URL + '/upload' || '/api/upload'
})

// 请求头
const headers = computed(() => {
  return {
    Authorization: `Bearer ${getToken()}`
  }
})

// 上传前检查
const beforeUpload = (file) => {
  const size = file.size / 1024 / 1024
  if (size > props.maxSize) {
    ElMessage.error(`文件大小不能超过 ${props.maxSize}MB`)
    return false
  }
  return true
}

// 上传成功
const handleSuccess = (response, file, fileList) => {
  if (response.code === 0) {
    ElMessage.success('上传成功')
    updateFileList(fileList)
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

// 上传失败
const handleError = (error) => {
  ElMessage.error('上传失败')
  console.error('上传失败:', error)
}

// 移除文件
const handleRemove = (file, fileList) => {
  updateFileList(fileList)
}

// 超出限制
const handleExceed = () => {
  ElMessage.warning(`最多只能上传 ${props.limit} 个文件`)
}

// 更新文件列表
const updateFileList = (list) => {
  const files = list
    .filter(item => item.status === 'success')
    .map(item => ({
      name: item.name,
      url: item.response?.data?.url || item.url,
      size: item.size
    }))
  emit('update:modelValue', files)
}

// 清空文件列表
const clearFiles = () => {
  uploadRef.value?.clearFiles()
  emit('update:modelValue', [])
}

// 暴露方法
defineExpose({
  clearFiles
})
</script>

<style scoped lang="scss">
.file-upload {
  :deep(.el-upload__tip) {
    color: #999;
    font-size: 12px;
    margin-top: 5px;
  }
}
</style>
