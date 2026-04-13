from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models.models import CustomOrder
from ..auth import admin_only

router = APIRouter()

class CustomOrderSchema(BaseModel):
    customer_name: str
    customer_phone: str
    description: str = ""
    budget: str = ""
    category: str = ""

class StatusSchema(BaseModel):
    status: str

@router.post("/")
def create_custom_order(data: CustomOrderSchema, db: Session = Depends(get_db)):
    order = CustomOrder(**data.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/", dependencies=[Depends(admin_only)])
def get_custom_orders(db: Session = Depends(get_db)):
    return db.query(CustomOrder).order_by(CustomOrder.created_at.desc()).all()

@router.put("/{order_id}/status", dependencies=[Depends(admin_only)])
def update_status(order_id: int, data: StatusSchema, db: Session = Depends(get_db)):
    order = db.query(CustomOrder).filter(CustomOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    order.status = data.status
    db.commit()
    return {"success": True}