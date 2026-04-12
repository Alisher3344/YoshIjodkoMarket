const low = require('lowdb')
const FileSync = require('lowdb/adapters/FileSync')
const path = require('path')

const adapter = new FileSync(path.join(__dirname, 'db.json'))
const db = low(adapter)

// Faqat db.json bo'sh bo'lsa default yoziladi
db.defaults({
  users: [],
  products: [],
  orders: [],
  customOrders: []
}).write()

module.exports = db
