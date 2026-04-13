from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any
import json
from ..database import get_db
from ..models.models import Order
from ..auth import admin_only

router = APIRouter()

class OrderSchema(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: str = ""
    items: Any = []
    total: float = 0
    payment_method: str = "cash"

class StatusSchema(BaseModel):
    status: str

@router.post("/")
def create_order(data: OrderSchema, db: Session = Depends(get_db)):
    order = Order(
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        customer_address=data.customer_address,
        items=json.dumps(data.items, ensure_ascii=False),
        total=data.total,
        payment_method=data.payment_method
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    result = order.__dict__.copy()
    result["items"] = json.loads(order.items)
    return result

@router.get("/", dependencies=[Depends(admin_only)])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    result = []
    for o in orders:
        d = o.__dict__.copy()
        d["items"] = json.loads(o.items or "[]")
        result.append(d)
    return result

@router.put("/{order_id}/status", dependencies=[Depends(admin_only)])
def update_status(order_id: int, data: StatusSchema, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    order.status = data.status
    db.commit()
    return {"success": True}