import request from './request'

export function getTasks(params) {
  return request({
    url: '/tasks',
    method: 'get',
    params
  })
}

export function getTaskDetail(taskId) {
  return request({
    url: `/tasks/${taskId}`,
    method: 'get'
  })
}

export function createTask(data) {
  return request({
    url: '/tasks',
    method: 'post',
    data
  })
}

export function transferTask(taskId, data) {
  return request({
    url: `/tasks/${taskId}/transfer`,
    method: 'post',
    data
  })
}

export function respondTask(taskId) {
  return request({
    url: `/tasks/${taskId}/respond`,
    method: 'post'
  })
}

export function completeTask(taskId, data) {
  return request({
    url: `/tasks/${taskId}/complete`,
    method: 'post',
    data
  })
}

export function getTaskTransfers(taskId) {
  return request({
    url: `/tasks/${taskId}/transfers`,
    method: 'get'
  })
}

export function getTaskComments(taskId) {
  return request({
    url: `/tasks/${taskId}/comments`,
    method: 'get'
  })
}

export function createComment(taskId, data) {
  return request({
    url: `/tasks/${taskId}/comments`,
    method: 'post',
    data
  })
}

export function suspendTask(taskId, data) {
  return request({
    url: `/tasks/${taskId}/suspend`,
    method: 'post',
    data
  })
}

export function closeTask(taskId, data) {
  return request({
    url: `/tasks/${taskId}/close`,
    method: 'post',
    data
  })
}

export function updateTask(taskId, data) {
  return request({
    url: `/tasks/${taskId}`,
    method: 'put',
    data
  })
}

export function getAttachments(taskId) {
  return request({
    url: `/tasks/${taskId}/attachments`,
    method: 'get'
  })
}

export function uploadAttachment(taskId, file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: `/tasks/${taskId}/attachments`,
    method: 'post',
    data: formData,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export function deleteAttachment(taskId, attachmentId) {
  return request({
    url: `/tasks/${taskId}/attachments/${attachmentId}`,
    method: 'delete'
  })
}

export function downloadAttachment(taskId, attachmentId) {
  return `/api/tasks/${taskId}/attachments/${attachmentId}/download`
}
