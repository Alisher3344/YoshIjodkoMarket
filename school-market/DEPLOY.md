# 🚀 Yoshijodkor.uz — Deploy qilish qo'llanmasi

## Loyiha tuzilishi

```
school-market/
├── src/                  ← React frontend (Vite)
│   ├── store/index.js    ← Zustand store (API bilan ishlaydi)
│   ├── utils/api.js      ← API so'rovlar
│   └── data/products.js  ← Fallback ma'lumotlar
├── server/               ← Express backend
│   ├── index.js          ← Server entry point
│   ├── db/db.json        ← JSON ma'lumotlar bazasi (12 ta mahsulot)
│   ├── db/index.js       ← Lowdb konfiguratsiyasi
│   ├── routes/           ← API route'lar
│   │   ├── auth.js       ← Login/register
│   │   ├── products.js   ← Mahsulotlar CRUD
│   │   ├── orders.js     ← Buyurtmalar
│   │   ├── users.js      ← Foydalanuvchilar
│   │   └── customOrders.js
│   └── middleware/auth.js ← JWT authentication
└── dist/                 ← Build natijasi
```

## 1-qadam: Serverni ishga tushirish (VPS yoki hosting)

### Node.js o'rnatish (agar yo'q bo'lsa)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Server dependency'larni o'rnatish
```bash
cd server
npm install
```

### Serverni ishga tushirish
```bash
# Test uchun
node index.js

# PM2 bilan (production uchun)
npm install -g pm2
pm2 start index.js --name "school-market-api"
pm2 save
pm2 startup
```

## 2-qadam: Frontend build

```bash
# Root papkada
npm install
npm run build
```

## 3-qadam: Nginx konfiguratsiyasi

```nginx
# /etc/nginx/sites-available/yoshijodkor.uz
server {
    listen 80;
    server_name yoshijodkor.uz www.yoshijodkor.uz;

    # Frontend (dist papkasi)
    root /var/www/yoshijodkor.uz/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}

# API subdomain
server {
    listen 80;
    server_name api.yoshijodkor.uz;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/yoshijodkor.uz /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 4-qadam: SSL (HTTPS)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yoshijodkor.uz -d www.yoshijodkor.uz -d api.yoshijodkor.uz
```

## Admin panel kirish
- URL: https://yoshijodkor.uz/admin
- Login: `admin`
- Parol: `admin123`

## API endpoints
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | /api/products | Barcha mahsulotlar |
| GET | /api/products/:id | Bitta mahsulot |
| POST | /api/products | Yangi qo'shish (admin) |
| PUT | /api/products/:id | Yangilash (admin) |
| DELETE | /api/products/:id | O'chirish (admin) |
| POST | /api/auth/login | Kirish |
| GET | /api/orders | Buyurtmalar (admin) |
| POST | /api/orders | Yangi buyurtma |

## Muhim: .env sozlamalari

### Frontend (.env)
```
VITE_API_URL=https://api.yoshijodkor.uz/api
```

### Server (server/.env)
```
PORT=5000
JWT_SECRET=maktab_market_super_secret_key_2024
CLIENT_URL=https://yoshijodkor.uz
NODE_ENV=production
```
