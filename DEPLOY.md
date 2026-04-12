# yoshijodkor.uz ga joylashtirish

## 1. VPS ga ulaning (SSH)
```bash
ssh root@YOUR_SERVER_IP
```

## 2. Kerakli dasturlarni o'rnating
```bash
apt update && apt upgrade -y
apt install -y nodejs npm nginx certbot python3-certbot-nginx
```

## 3. Loyihani serverga yuklang
```bash
mkdir -p /var/www/yoshijodkor.uz
cd /var/www/yoshijodkor.uz
# FileZilla yoki scp bilan school-market papkasini yuklang
```

## 4. Backend o'rnating
```bash
cd /var/www/yoshijodkor.uz/server
npm install
```

## 5. PM2 bilan backendni ishga tushiring (doim ishlaydi)
```bash
npm install -g pm2
pm2 start index.js --name "yoshijodkor-api"
pm2 startup
pm2 save
```

## 6. Frontend build qiling
```bash
cd /var/www/yoshijodkor.uz
npm install
npm run build
# dist/ papkasi tayyor bo'ladi
```

## 7. Nginx sozlang
```bash
cp nginx.conf /etc/nginx/sites-available/yoshijodkor.uz
ln -s /etc/nginx/sites-available/yoshijodkor.uz /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

## 8. SSL sertifikat oling (bepul)
```bash
certbot --nginx -d yoshijodkor.uz -d www.yoshijodkor.uz -d api.yoshijodkor.uz
```

## 9. Done! 
https://yoshijodkor.uz — sayt ishlaydi ✅

## Foydali buyruqlar
```bash
pm2 status          # backend holati
pm2 logs            # loglar
pm2 restart all     # qayta ishga tushirish
nginx -t            # nginx tekshirish
systemctl reload nginx
```
