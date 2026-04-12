import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { translations } from '../i18n/translations'
import { initialProducts } from '../data/products'
import { authAPI, productsAPI, ordersAPI, customOrdersAPI, usersAPI } from '../utils/api'

export const useLangStore = create(persist(
  (set, get) => ({
    lang: 'uz',
    setLang: (lang) => set({ lang }),
    t: (key) => translations[get().lang][key] || key,
  }),
  { name: 'lang-storage' }
))

export const useCartStore = create(persist(
  (set, get) => ({
    items: [],
    addItem: (product) => {
      const items = get().items
      const existing = items.find(i => i.id === product.id)
      if (existing) {
        set({ items: items.map(i => i.id === product.id ? { ...i, qty: i.qty + 1 } : i) })
      } else {
        set({ items: [...items, { ...product, qty: 1 }] })
      }
    },
    removeItem: (id) => set({ items: get().items.filter(i => i.id !== id) }),
    updateQty: (id, qty) => {
      if (qty < 1) return
      set({ items: get().items.map(i => i.id === id ? { ...i, qty } : i) })
    },
    clearCart: () => set({ items: [] }),
    get total() { return get().items.reduce((sum, i) => sum + i.price * i.qty, 0) },
    get count() { return get().items.reduce((sum, i) => sum + i.qty, 0) },
  }),
  { name: 'cart-storage' }
))

export const useAuthStore = create(persist(
  (set, get) => ({
    isLoggedIn: false,
    token: null,
    user: null,

    login: (username, password) => {
      if (username === 'admin' && password === 'admin123') {
        set({ isLoggedIn: true })
        return true
      }
      return false
    },

    loginWithAPI: async (username, password) => {
      try {
        const res = await authAPI.login(username, password)
        localStorage.setItem('auth_token', res.token)
        set({ isLoggedIn: true, token: res.token, user: res.user })
        return { success: true, user: res.user }
      } catch (err) {
        // Fallback: local users
        const stored = localStorage.getItem('users-storage')
        if (stored) {
          const all = JSON.parse(stored)?.state?.users || []
          const found = all.find(u =>
            u.username?.trim() === username.trim() &&
            u.password?.trim() === password.trim() &&
            u.active !== false
          )
          if (found || (username === 'admin' && password === 'admin123')) {
            set({ isLoggedIn: true })
            return { success: true }
          }
        }
        if (username === 'admin' && password === 'admin123') {
          set({ isLoggedIn: true })
          return { success: true }
        }
        return { success: false, error: err.message }
      }
    },

    logout: () => {
      localStorage.removeItem('auth_token')
      set({ isLoggedIn: false, token: null, user: null })
    },
  }),
  { name: 'auth-storage' }
))

export const useProductStore = create(persist(
  (set, get) => ({
    products: initialProducts,
    loading: false,
    useAPI: false,

    fetchProducts: async () => {
      set({ loading: true })
      try {
        const products = await productsAPI.getAll()
        if (Array.isArray(products) && products.length > 0) {
          set({ products, useAPI: true })
        } else {
          set({ useAPI: false })
        }
      } catch {
        set({ useAPI: false })
      } finally {
        set({ loading: false })
      }
    },

    addProduct: async (product) => {
      const newProduct = { ...product, id: Date.now(), createdAt: new Date().toISOString() }
      
      try {
        const apiProduct = await productsAPI.create(product)
        set({ products: [apiProduct, ...get().products], useAPI: true })
        return apiProduct
      } catch {
        // Fallback: local qo'shish
        set({ products: [newProduct, ...get().products] })
        return newProduct
      }
    },

    updateProduct: async (id, data) => {
      // Avval localda yangilash (tez ko'rinishi uchun)
      set({ products: get().products.map(p => p.id === id ? { ...p, ...data } : p) })
      
      try {
        await productsAPI.update(id, data)
      } catch {
        // API ishlamasa ham local yangilangan
      }
    },

    deleteProduct: async (id) => {
      // Avval localdan o'chirish
      set({ products: get().products.filter(p => p.id !== id) })
      
      try {
        await productsAPI.delete(id)
      } catch {
        // API ishlamasa ham local o'chirilgan
      }
    },

    decreaseStock: (id, qty = 1) => {
      set({ products: get().products.map(p =>
        p.id === id ? { ...p, stock: Math.max(0, p.stock - qty) } : p
      )})
    },

    getByCategory: (cat) => {
      if (!cat || cat === 'all') return get().products
      return get().products.filter(p => p.category === cat)
    },

    search: (query) => {
      const q = query.toLowerCase()
      return get().products.filter(p =>
        p.name_uz?.toLowerCase().includes(q) ||
        p.name_ru?.toLowerCase().includes(q) ||
        p.author?.toLowerCase().includes(q)
      )
    }
  }),
  { name: 'product-storage' }
))

export const useOrderStore = create(persist(
  (set, get) => ({
    orders: [],

    addOrder: async (orderData) => {
      const order = {
        ...orderData,
        id: 'ORD-' + Date.now(),
        status: 'new',
        createdAt: new Date().toISOString(),
      }
      try {
        const res = await ordersAPI.create(order)
        order.id = res.id || order.id
      } catch {}
      set({ orders: [order, ...get().orders] })
      return order.id
    },

    fetchOrders: async () => {
      try {
        const orders = await ordersAPI.getAll()
        if (Array.isArray(orders)) set({ orders })
      } catch {}
    },

    updateStatus: async (id, status) => {
      set({ orders: get().orders.map(o => o.id === id ? { ...o, status } : o) })
      try { await ordersAPI.updateStatus(id, status) } catch {}
    },

    getStats: () => {
      const orders = get().orders
      const revenue = orders.filter(o => o.status === 'done').reduce((sum, o) => sum + o.total, 0)
      return {
        total: orders.length,
        new: orders.filter(o => o.status === 'new').length,
        done: orders.filter(o => o.status === 'done').length,
        revenue,
      }
    }
  }),
  { name: 'order-storage' }
))

export const useCustomOrderStore = create(persist(
  (set, get) => ({
    customOrders: [],

    addCustomOrder: async (order) => {
      const newOrder = {
        ...order,
        id: 'CUS-' + Date.now(),
        status: 'new',
        createdAt: new Date().toISOString(),
        messages: [],
      }
      try {
        const res = await customOrdersAPI.create(newOrder)
        newOrder.id = res.id || newOrder.id
      } catch {}
      set({ customOrders: [newOrder, ...get().customOrders] })
      return newOrder.id
    },

    fetchCustomOrders: async () => {
      try {
        const customOrders = await customOrdersAPI.getAll()
        if (Array.isArray(customOrders)) set({ customOrders })
      } catch {}
    },

    updateCustomStatus: async (id, status) => {
      set({ customOrders: get().customOrders.map(o => o.id === id ? { ...o, status } : o) })
      try { await customOrdersAPI.updateStatus(id, status) } catch {}
    },

    addMessage: (orderId, message) => {
      set({
        customOrders: get().customOrders.map(o =>
          o.id === orderId
            ? { ...o, messages: [...(o.messages || []), { ...message, time: new Date().toISOString() }] }
            : o
        )
      })
    },
  }),
  { name: 'custom-orders-storage' }
))

export const useUsersStore = create(persist(
  (set, get) => ({
    users: [
      { id: 1, username: 'admin', password: 'admin123', role: 'admin', name: 'Bosh Admin', email: 'admin@yoshijodkor.uz', createdAt: '2024-01-01T00:00:00.000Z', active: true },
    ],

    fetchUsers: async () => {
      try {
        const users = await usersAPI.getAll()
        if (Array.isArray(users)) set({ users })
      } catch {}
    },

    addUser: async (user) => {
      try {
        const newUser = await usersAPI.create(user)
        set({ users: [newUser, ...get().users] })
        return { success: true }
      } catch (err) {
        if (err.message === 'Bu username band') return { error: err.message }
      }
      const exists = get().users.find(u => u.username === user.username)
      if (exists) return { error: 'Bu username allaqachon mavjud' }
      const newUser = { ...user, id: Date.now(), createdAt: new Date().toISOString(), active: true }
      set({ users: [newUser, ...get().users] })
      return { success: true }
    },

    updateUser: async (id, data) => {
      set({ users: get().users.map(u => u.id === id ? { ...u, ...data } : u) })
      try { await usersAPI.update(id, data) } catch {}
    },

    deleteUser: async (id) => {
      set({ users: get().users.filter(u => u.id !== id) })
      try { await usersAPI.delete(id) } catch {}
    },

    toggleActive: async (id) => {
      set({ users: get().users.map(u => u.id === id ? { ...u, active: !u.active } : u) })
      try { await usersAPI.toggle(id) } catch {}
    },

    loginUser: (username, password) => {
      const user = get().users.find(u => u.username === username && u.password === password && u.active)
      return user || null
    },
  }),
  { name: 'users-storage' }
))
