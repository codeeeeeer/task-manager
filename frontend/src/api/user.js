import request from './request'

/**
 * 获取所有用户列表（用于下拉选择）
 */
export function getAllUsers() {
  return request({
    url: '/users/all',
    method: 'get'
  })
}

/**
 * 获取用户列表（管理员）
 */
export function getUsers(params) {
  return request({
    url: '/users',
    method: 'get',
    params
  })
}

/**
 * 创建用户（管理员）
 */
export function createUser(data) {
  return request({
    url: '/users',
    method: 'post',
    data
  })
}

/**
 * 更新用户（管理员）
 */
export function updateUser(userId, data) {
  return request({
    url: `/users/${userId}`,
    method: 'put',
    data
  })
}

/**
 * 修改密码
 */
export function changePassword(userId, data) {
  return request({
    url: `/users/${userId}/change-password`,
    method: 'post',
    data
  })
}
