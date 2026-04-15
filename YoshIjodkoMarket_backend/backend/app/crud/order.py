import json
from typing import Optional
from sqlalchemy.orm import Session

from ..models.order import Order, CustomOrder
from ..schemas.order import OrderCreate, CustomOrderCreate


# ── Oddiy buyurtmalar ──────────────────────────────────────────────────────

def create_order(db: Session, data: OrderCreate) -> dict:
    """
    Yangi buyurtma yaratadi.
    items listni JSON string ga o'tkazib saqlaydi.
    Qaytishda items ni yana list ga o'giradi.
    """
    order = Order(
        customer_name    = data.customer_name,
        customer_phone   = data.customer_phone,
        customer_address = data.customer_address,
        items            = json.dumps(data.items, ensure_ascii=False),
        total            = data.total,
        payment_method   = data.payment_method,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    result = order.__dict__.copy()
    result["items"] = json.loads(order.items)
    return result


def get_all_orders(db: Session) -> list:
    """Barcha buyurtmalarni yangilari birinchi qaytaradi."""
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    result = []
    for o in orders:
        d = o.__dict__.copy()
        d["items"] = json.loads(o.items or "[]")
        result.append(d)
    return result


def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
    """ID bo'yicha bitta buyurtma topadi."""
    return db.query(Order).filter(Order.id == order_id).first()


def update_order_status(db: Session, order: Order, status: str) -> None:
    """Buyurtma statusini yangilaydi."""
    order.status = status
    db.commit()


# ── Maxsus buyurtmalar ─────────────────────────────────────────────────────

def create_custom_order(db: Session, data: CustomOrderCreate) -> CustomOrder:
    """Yangi maxsus buyurtma yaratadi."""
    order = CustomOrder(**data.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_all_custom_orders(db: Session) -> list:
    """Barcha maxsus buyurtmalarni yangilari birinchi."""
    return (
        db.query(CustomOrder)
        .order_by(CustomOrder.created_at.desc())
        .all()
    )


def get_custom_order_by_id(db: Session, order_id: int) -> Optional[CustomOrder]:
    """ID bo'yicha bitta maxsus buyurtma topadi."""
    return db.query(CustomOrder).filter(CustomOrder.id == order_id).first()


def update_custom_order_status(
    db: Session, order: CustomOrder, status: str
) -> None:
    """Maxsus buyurtma statusini yangilaydi."""
    order.status = status
    db.commit()