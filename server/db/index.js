const low = require('lowdb')
const FileSync = require('lowdb/adapters/FileSync')
const path = require('path')
const bcrypt = require('bcryptjs')

const adapter = new FileSync(path.join(__dirname, 'db.json'))
const db = low(adapter)

// MUHIM: faqat bo'sh bo'lsa yoziladi, har restartda QAYTA YOZILMAYDI
const state = db.getState()
if (!state || !state.users || !state.products) {
  db.setState({
    users: [
      {
        id: 1,
        name: 'Bosh Admin',
        username: 'admin',
        password: bcrypt.hashSync('admin123', 10),
        email: 'admin@yoshijodkor.uz',
        role: 'admin',
        active: true,
        createdAt: new Date().toISOString()
      }
    ],
    products: [],
    orders: [],
    customOrders: []
  }).write()
}

// Auto-increment ID: mavjud eng katta id + 1
db.getNextId = (collection) => {
  const items = db.get(collection).value()
  if (!items || items.length === 0) return 1
  const maxId = Math.max(...items.map(i => Number(i.id) || 0))
  return maxId + 1
}

module.exports = db
