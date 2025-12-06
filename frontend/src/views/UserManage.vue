<template>
  <div class="user-manage">
    <div class="header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="showCreateDialog = true">新建用户</el-button>
    </div>

    <!-- 搜索区 -->
    <el-card class="filter-card">
      <el-form :inline="true">
        <el-form-item label="搜索">
          <el-input v-model="searchText" placeholder="用户编号、姓名或邮箱" clearable style="width: 250px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 用户列表 -->
    <el-table :data="users" v-loading="loading" style="width: 100%; margin-top: 20px">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="um_code" label="用户编号" width="120" />
      <el-table-column prop="name" label="姓名" width="120" />
      <el-table-column prop="email" label="邮箱" min-width="200" />
      <el-table-column prop="is_admin" label="角色" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.is_admin ? 'danger' : 'primary'">
            {{ scope.row.is_admin ? '管理员' : '普通用户' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.is_active ? 'success' : 'info'">
            {{ scope.row.is_active ? '激活' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button size="small" type="primary" link @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" link @click="handleToggleStatus(scope.row)">
            {{ scope.row.is_active ? '禁用' : '启用' }}
          </el-button>
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
      @size-change="loadUsers"
      @current-change="loadUsers"
      style="margin-top: 20px; justify-content: flex-end"
    />

    <!-- 新建用户对话框 -->
    <el-dialog v-model="showCreateDialog" title="新建用户" width="500px" @close="resetForm">
      <el-form :model="form" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="用户编号" prop="um_code">
          <el-input v-model="form.um_code" placeholder="如: UM001" />
        </el-form-item>

        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" type="email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>

        <el-form-item label="角色" prop="is_admin">
          <el-radio-group v-model="form.is_admin">
            <el-radio :label="false">普通用户</el-radio>
            <el-radio :label="true">管理员</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate" :loading="submitting">创建</el-button>
      </template>
    </el-dialog>

    <!-- 编辑用户对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑用户" width="500px" @close="resetForm">
      <el-form :model="form" :rules="editRules" ref="formRef" label-width="100px">
        <el-form-item label="用户编号">
          <el-input v-model="form.um_code" disabled />
        </el-form-item>

        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" type="email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="角色" prop="is_admin">
          <el-radio-group v-model="form.is_admin">
            <el-radio :label="false">普通用户</el-radio>
            <el-radio :label="true">管理员</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUpdate" :loading="submitting">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, createUser, updateUser } from '@/api/user'

// 数据
const users = ref([])
const loading = ref(false)
const submitting = ref(false)
const showCreateDialog = ref(false)
const showEditDialog = ref(false)
const formRef = ref(null)
const searchText = ref('')

// 分页
const pagination = reactive({
  page: 1,
  per_page: 20,
  total: 0
})

// 表单
const form = reactive({
  id: null,
  um_code: '',
  name: '',
  email: '',
  password: '',
  is_admin: false
})

// 表单验证规则
const formRules = {
  um_code: [{ required: true, message: '请输入用户编号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ]
}

const editRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ]
}

// 加载用户列表
const loadUsers = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      per_page: pagination.per_page,
      search: searchText.value
    }

    const res = await getUsers(params)
    users.value = res.users || []
    pagination.total = res.total || 0
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadUsers()
}

// 重置
const handleReset = () => {
  searchText.value = ''
  pagination.page = 1
  loadUsers()
}

// 创建用户
const handleCreate = async () => {
  try {
    await formRef.value.validate()
    submitting.value = true

    await createUser({
      um_code: form.um_code,
      name: form.name,
      email: form.email,
      password: form.password,
      is_admin: form.is_admin
    })

    ElMessage.success('用户创建成功')
    showCreateDialog.value = false
    loadUsers()
  } catch (error) {
    if (error !== false) {
      console.error('创建用户失败:', error)
    }
  } finally {
    submitting.value = false
  }
}

// 编辑用户
const handleEdit = (row) => {
  form.id = row.id
  form.um_code = row.um_code
  form.name = row.name
  form.email = row.email
  form.is_admin = row.is_admin
  showEditDialog.value = true
}

// 更新用户
const handleUpdate = async () => {
  try {
    await formRef.value.validate()
    submitting.value = true

    await updateUser(form.id, {
      name: form.name,
      email: form.email,
      is_admin: form.is_admin
    })

    ElMessage.success('用户更新成功')
    showEditDialog.value = false
    loadUsers()
  } catch (error) {
    if (error !== false) {
      console.error('更新用户失败:', error)
    }
  } finally {
    submitting.value = false
  }
}

// 切换用户状态
const handleToggleStatus = async (row) => {
  try {
    const action = row.is_active ? '禁用' : '启用'
    await ElMessageBox.confirm(`确定要${action}用户 ${row.name} 吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await updateUser(row.id, { is_active: !row.is_active })
    ElMessage.success(`${action}成功`)
    loadUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('切换状态失败:', error)
    }
  }
}

// 重置表单
const resetForm = () => {
  formRef.value?.resetFields()
  form.id = null
  form.um_code = ''
  form.name = ''
  form.email = ''
  form.password = ''
  form.is_admin = false
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
    hour12: false
  })
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped lang="scss">
.user-manage {
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
    background: #fff9f0;
    border: 1px solid #ffd6a5;

    :deep(.el-card__body) {
      padding: 15px;
    }
  }

  :deep(.el-pagination) {
    display: flex;
  }
}
</style>
