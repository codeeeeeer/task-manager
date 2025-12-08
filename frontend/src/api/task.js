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
