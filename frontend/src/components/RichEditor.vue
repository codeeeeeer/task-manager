<template>
  <div class="rich-editor">
    <Toolbar
      :editor="editorRef"
      :defaultConfig="toolbarConfig"
      :mode="mode"
      style="border-bottom: 1px solid #ccc"
    />
    <Editor
      :defaultConfig="editorConfig"
      :mode="mode"
      v-model="valueHtml"
      @onCreated="handleCreated"
      @onChange="handleChange"
      style="height: 300px; overflow-y: hidden;"
    />
  </div>
</template>

<script setup>
import { ref, shallowRef, onBeforeUnmount, watch } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import '@wangeditor/editor/dist/css/style.css'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  height: {
    type: String,
    default: '300px'
  }
})

const emit = defineEmits(['update:modelValue'])

// 编辑器实例
const editorRef = shallowRef()
const mode = 'default' // 'default' 或 'simple'

// 编辑器内容
const valueHtml = ref('')

// 工具栏配置
const toolbarConfig = {
  toolbarKeys: [
    'headerSelect',
    'bold',
    'italic',
    'underline',
    'through',
    'color',
    'bgColor',
    '|',
    'fontSize',
    'fontFamily',
    'lineHeight',
    '|',
    'bulletedList',
    'numberedList',
    'todo',
    '|',
    'justifyLeft',
    'justifyCenter',
    'justifyRight',
    '|',
    'insertLink',
    'insertImage',
    'insertTable',
    'codeBlock',
    'divider',
    '|',
    'undo',
    'redo',
    '|',
    'fullScreen'
  ]
}

// 编辑器配置
const editorConfig = {
  placeholder: '请输入内容...',
  MENU_CONF: {
    uploadImage: {
      // 暂时禁用图片上传，后续可以配置
      server: '/api/upload',
      fieldName: 'file',
      maxFileSize: 10 * 1024 * 1024, // 10M
      maxNumberOfFiles: 10,
      allowedFileTypes: ['image/*'],
      customInsert(res, insertFn) {
        // res 即服务端的返回结果
        const url = res.data.url
        const alt = res.data.alt || ''
        const href = res.data.href || ''
        insertFn(url, alt, href)
      }
    }
  }
}

// 编辑器创建完成
const handleCreated = (editor) => {
  editorRef.value = editor
}

// 编辑器内容变化
const handleChange = (editor) => {
  emit('update:modelValue', valueHtml.value)
}

// 监听外部值变化
watch(() => props.modelValue, (newVal) => {
  if (newVal !== valueHtml.value) {
    valueHtml.value = newVal
  }
}, { immediate: true })

// 组件销毁时，销毁编辑器
onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})
</script>

<style scoped lang="scss">
.rich-editor {
  border: 1px solid #ccc;
  border-radius: 4px;
  overflow: hidden;

  :deep(.w-e-text-container) {
    background-color: #fff;
  }

  :deep(.w-e-toolbar) {
    background-color: #fafafa;
  }
}
</style>
