const TOKEN_KEY = 'task_manager_token'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export function getUserInfo() {
  const userInfoStr = localStorage.getItem('user_info')
  return userInfoStr ? JSON.parse(userInfoStr) : null
}

export function setUserInfo(userInfo) {
  localStorage.setItem('user_info', JSON.stringify(userInfo))
}

export function removeUserInfo() {
  localStorage.removeItem('user_info')
}
