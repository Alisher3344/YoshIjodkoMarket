from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.database import engine, Base
from .core.config import settings
from .routes import auth, products, orders, custom_orders, users

# DB jadvallarini yaratish
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Maktab Market API", version="2.0.0")

# CORS — frontend bilan ulanish uchun
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.CLIENT_URL,
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routelarni ulash
app.include_router(auth.router,          prefix="/api/auth",         tags=["auth"])
app.include_router(products.router,      prefix="/api/products",     tags=["products"])
app.include_router(orders.router,        prefix="/api/orders",       tags=["orders"])
app.include_router(custom_orders.router, prefix="/api/custom-orders",tags=["custom-orders"])
app.include_router(users.router,         prefix="/api/users",        tags=["users"])


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Maktab Market API ishlayapti ✅"}