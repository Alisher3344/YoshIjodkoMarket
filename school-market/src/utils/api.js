// Barcha API so'rovlar shu fayl orqali o'tadi
const BASE = import.meta.env.VITE_API_URL || 'https://api.yoshijodkor.uz/api'

function getToken() {
  return localStorage.getItem('auth_token')
}

async function request(method, url, data = null) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(`${BASE}${url}`, {
    method,
    headers,
    body: data ? JSON.stringify(data) : null
  })

  const json = await res.json()
  if (!res.ok) throw new Error(json.error || 'Xatolik yuz berdi')
  return json
}

// ── AUTH ──
export const authAPI = {
  login: (username, password) => request('POST', '/auth/login', { username, password }),
  me: () => request('GET', '/auth/me'),
}

// ── PRODUCTS ──
export const productsAPI = {
  getAll: (params = {}) => {
    const q = new URLSearchParams(params).toString()
    return request('GET', `/products${q ? '?' + q : ''}`)
  },
  getOne: (id) => request('GET', `/products/${id}`),
  create: (data) => request('POST', '/products', data),
  update: (id, data) => request('PUT', `/products/${id}`, data),
  delete: (id) => request('DELETE', `/products/${id}`),
}

// ── ORDERS ──
export const ordersAPI = {
  create: (data) => request('POST', '/orders', data),
  getAll: () => request('GET', '/orders'),
  updateStatus: (id, status) => request('PUT', `/orders/${id}/status`, { status }),
}

// ── CUSTOM ORDERS ──
export const customOrdersAPI = {
  create: (data) => request('POST', '/custom-orders', data),
  getAll: () => request('GET', '/custom-orders'),
  updateStatus: (id, status) => request('PUT', `/custom-orders/${id}/status`, { status }),
}

// ── USERS ──
export const usersAPI = {
  getAll: () => request('GET', '/users'),
  create: (data) => request('POST', '/users', data),
  update: (id, data) => request('PUT', `/users/${id}`, data),
  delete: (id) => request('DELETE', `/users/${id}`),
  toggle: (id) => request('PATCH', `/users/${id}/toggle`),
}
