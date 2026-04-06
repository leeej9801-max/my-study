export const decode = (data) => {
  return JSON.parse(decodeURIComponent(window.atob(data)))
}

export const encode = (data) => {
  return window.btoa(encodeURIComponent(JSON.stringify(data)))
}

export const setStorage = (key, data) => {
  localStorage.setItem(key, encode(data))
}

export const getStorage = key => {
  const data = localStorage.getItem(key)
  return data === null ? null : decode(data)
}

export const removeStorage = key => {
  localStorage.removeItem(key)
}

export const getDate = () => {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}