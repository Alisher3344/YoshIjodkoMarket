const express = require('express')
const router = express.Router()
const bcrypt = require('bcryptjs')
const jwt = require('jsonwebtoken')
const db = require('../db')

const SECRET = process.env.JWT_SECRET || 'maktab_market_secret_2024'

// POST /api/auth/login
router.post('/login', (req, res) => {
  const { username, password } = req.body
  if (!username || !password)
    return res.status(400).json({ error: "Username va parol kerak" })

  const user = db.get('users').find({ username: username.trim() }).value()
  if (!user || !user.active)
    return res.status(401).json({ error: "Login yoki parol noto'g'ri" })

  const match = bcrypt.compareSync(password, user.password)
  if (!match)
    return res.status(401).json({ error: "Login yoki parol noto'g'ri" })

  const token = jwt.sign(
    { id: user.id, username: user.username, role: user.role, name: user.name },
    SECRET,
    { expiresIn: '7d' }
  )

  res.json({
    token,
    user: { id: user.id, name: user.name, username: user.username, role: user.role, email: user.email }
  })
})

// GET /api/auth/me
router.get('/me', (req, res) => {
  const token = req.headers.authorization?.split(' ')[1]
  if (!token) return res.status(401).json({ error: 'Token kerak' })
  try {
    const decoded = jwt.verify(token, SECRET)
    const user = db.get('users').find({ id: decoded.id }).value()
    if (!user) return res.status(404).json({ error: 'Foydalanuvchi topilmadi' })
    const { password, ...safeUser } = user
    res.json(safeUser)
  } catch {
    res.status(401).json({ error: 'Token yaroqsiz' })
  }
})

module.exports = router
