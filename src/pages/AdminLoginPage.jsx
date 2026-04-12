import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Lock, User, Eye, EyeOff } from 'lucide-react'
import { useLangStore, useAuthStore, useUsersStore } from '../store'
import toast from 'react-hot-toast'

export default function AdminLoginPage() {
  const { lang, t } = useLangStore()
  const { login, loginWithAPI } = useAuthStore()
  const { users } = useUsersStore()
  const navigate = useNavigate()

  const [form, setForm] = useState({ username: '', password: '' })
  const [showPwd, setShowPwd] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleLogin = async () => {
    if (!form.username || !form.password) {
      setError(lang === 'uz' ? "Barcha maydonlarni to'ldiring" : 'Заполните все поля')
      return
    }
    setLoading(true)
    const uname = form.username.trim()
    const upass = form.password.trim()

    // 1. API orqali login
    const apiRes = await loginWithAPI(uname, upass)
    if (apiRes.success) {
      toast.success(lang === 'uz' ? `Xush kelibsiz, ${apiRes.user?.name || 'Admin'}! 👋` : `Добро пожаловать, ${apiRes.user?.name || 'Admin'}! 👋`, { icon: '🎉' })
      navigate('/admin/dashboard')
      setLoading(false)
      return
    }

    // 2. Fallback: hardcoded admin yoki local users
    const isAdmin = uname === 'admin' && (upass === 'admin123' || upass === 'admin2008#')
    const userMatch = users.find(u => u.username.trim() === uname && u.password.trim() === upass && u.active !== false)

    if (isAdmin || userMatch) {
      login()
      const name = userMatch?.name || 'Admin'
      toast.success(lang === 'uz' ? `Xush kelibsiz, ${name}! 👋` : `Добро пожаловать, ${name}! 👋`, { icon: '🎉' })
      navigate('/admin/dashboard')
    } else {
      setError(lang === 'uz' ? "Login yoki parol noto'g'ri" : 'Неверный логин или пароль')
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-[#4c1d95] hero-pattern flex items-center justify-center px-4 pt-20">
      <div className="absolute top-1/4 right-10 w-64 h-64 rounded-full bg-[#ffffff]/5 blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 left-10 w-64 h-64 rounded-full bg-[#8b5cf6]/10 blur-3xl pointer-events-none" />

      <div className="w-full max-w-md">
        <div className="bg-white rounded-3xl p-8 shadow-2xl animate-fadeInUp">
          {/* Logo */}
          <div className="text-center mb-7">
            <img src="/logo.png" alt="logo" className="w-20 h-20 object-contain mx-auto mb-3" />
            <h1 className="text-2xl font-black text-[#4c1d95] font-serif">{t('admin_title')}</h1>
            <p className="text-gray-400 text-sm mt-1">Yosh Ijodkor</p>
          </div>

          {/* Demo hint */}
          <div className="bg-[#ede9fe] border border-[#4c1d95]/20 rounded-xl p-3 mb-6">
            <p className="text-xs text-[#4c1d95] font-semibold text-center">
              {lang === 'uz' ? 'Admin: admin / admin123' : 'Админ: admin / admin123'}
            </p>
          </div>

          {/* Fields */}
          <div className="space-y-4 mb-5">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1.5">{t('admin_username')}</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  value={form.username}
                  onChange={e => { setForm(p => ({ ...p, username: e.target.value })); setError('') }}
                  onKeyDown={e => e.key === 'Enter' && handleLogin()}
                  placeholder="username"
                  className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-gray-200 focus:border-[#4c1d95] outline-none text-sm transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1.5">{t('admin_password')}</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type={showPwd ? 'text' : 'password'}
                  value={form.password}
                  onChange={e => { setForm(p => ({ ...p, password: e.target.value })); setError('') }}
                  onKeyDown={e => e.key === 'Enter' && handleLogin()}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-12 py-3 rounded-xl border-2 border-gray-200 focus:border-[#4c1d95] outline-none text-sm transition-colors"
                />
                <button onClick={() => setShowPwd(!showPwd)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                  {showPwd ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-3 mb-4">
              <p className="text-sm text-red-600 text-center font-semibold">{error}</p>
            </div>
          )}

          <button
            onClick={handleLogin}
            disabled={loading}
            className="w-full bg-[#4c1d95] hover:bg-[#5b21b6] disabled:opacity-60 text-white font-black py-4 rounded-2xl transition-all hover:scale-[1.02] shadow-lg shadow-[#4c1d95]/30 flex items-center justify-center gap-2">
            {loading
              ? <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              : t('admin_login')
            }
          </button>

          {/* Show registered users hint */}
          {users.length > 1 && (
            <div className="mt-5 pt-4 border-t border-gray-100">
              <p className="text-xs text-gray-400 text-center mb-2">
                {lang === 'uz' ? "Ro'yxatdan o'tgan foydalanuvchilar:" : 'Зарегистрированные пользователи:'}
              </p>
              <div className="flex flex-wrap gap-2 justify-center">
                {users.filter(u => u.id !== 1).map(u => (
                  <button key={u.id}
                    onClick={() => setForm({ username: u.username, password: '' })}
                    className="text-xs bg-[#ede9fe] text-[#4c1d95] font-bold px-3 py-1 rounded-full hover:bg-[#4c1d95] hover:text-white transition-colors">
                    @{u.username}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
