import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, Base
from app.models.models import User, Product, Order, CustomOrder

# Jadvallarni yaratish
Base.metadata.create_all(bind=engine)

# db.json faylini o'qish — to'g'ri yo'lni ko'rsating
DB_JSON_PATH = r"C:\Users\Asus\Downloads\school-market-FIXED (3)\home\school-market-fixed (1)\server\db\db.json"

with open(DB_JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

db = SessionLocal()

# ── Users ──
print("Users ko'chirilmoqda...")
for u in data.get("users", []):
    exists = db.query(User).filter(User.username == u["username"]).first()
    if not exists:
        user = User(
            id=u["id"],
            name=u["name"],
            username=u["username"],
            password=u["password"],  # bcrypt hash saqlanadi
            email=u.get("email", ""),
            role=u.get("role", "admin"),
            active=u.get("active", True)
        )
        db.add(user)
print(f"  ✅ {len(data.get('users', []))} user")

# ── Products ──
print("Products ko'chirilmoqda...")
for p in data.get("products", []):
    exists = db.query(Product).filter(Product.id == p["id"]).first()
    if not exists:
        product = Product(
            id=p["id"],
            name_uz=p.get("name_uz", ""),
            name_ru=p.get("name_ru", ""),
            desc_uz=p.get("desc_uz", ""),
            desc_ru=p.get("desc_ru", ""),
            price=float(p.get("price", 0)),
            stock=int(p.get("stock", 1)),
            category=p.get("category", ""),
            author=p.get("author", ""),
            class_uz=p.get("class_uz", ""),
            class_ru=p.get("class_ru", ""),
            school=p.get("school", ""),
            district=p.get("district", ""),
            phone=p.get("phone", ""),
            image=p.get("image", ""),
            is_new=p.get("isNew", True)
        )
        db.add(product)
print(f"  ✅ {len(data.get('products', []))} product")

# ── Orders ──
print("Orders ko'chirilmoqda...")
for o in data.get("orders", []):
    exists = db.query(Order).filter(Order.id == o["id"]).first()
    if not exists:
        order = Order(
            id=o["id"],
            customer_name=o.get("customerName", ""),
            customer_phone=o.get("customerPhone", ""),
            customer_address=o.get("customerAddress", ""),
            items=json.dumps(o.get("items", []), ensure_ascii=False),
            total=float(o.get("total", 0)),
            status=o.get("status", "new"),
            payment_method=o.get("paymentMethod", "cash")
        )
        db.add(order)
print(f"  ✅ {len(data.get('orders', []))} order")

# ── Custom Orders ──
print("Custom orders ko'chirilmoqda...")
for co in data.get("customOrders", []):
    exists = db.query(CustomOrder).filter(CustomOrder.id == co["id"]).first()
    if not exists:
        custom = CustomOrder(
            id=co["id"],
            customer_name=co.get("customerName", ""),
            customer_phone=co.get("customerPhone", ""),
            description=co.get("description", ""),
            budget=co.get("budget", ""),
            category=co.get("category", ""),
            status=co.get("status", "new")
        )
        db.add(custom)
print(f"  ✅ {len(data.get('customOrders', []))} custom order")

db.commit()
db.close()
print("\n🎉 Migration muvaffaqiyatli yakunlandi!")