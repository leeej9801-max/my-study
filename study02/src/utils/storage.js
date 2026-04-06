export const decode = (data) => {
  return JSON.parse(decodeURIComponent(window.atob(data)))
}

export const encode = (data) => {
  return window.btoa(encodeURIComponent(JSON.stringify(data)))
}

export const setStorage = (key, data) => {
  localStorage.setItem(key, data)
}

export const getStorage = key => {
  return localStorage.getItem(key)
}

export const removeStorage = key => {
  localStorage.removeItem(key)
}
