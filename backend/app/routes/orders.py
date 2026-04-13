from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import require_admin
from ..crud import order as order_crud
from ..schemas.order import OrderCreate, OrderStatusUpdate

router = APIRouter()


@router.post("/")
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    """Yangi buyurtma yaratish — hamma foydalana oladi."""
    return order_crud.create_order(db, data)


@router.get("/", dependencies=[Depends(require_admin)])
def get_orders(db: Session = Depends(get_db)):
    """Barcha buyurtmalar — faqat admin."""
    return order_crud.get_all_orders(db)


@router.put("/{order_id}/status", dependencies=[Depends(require_admin)])
def update_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
):
    """Buyurtma statusini yangilash — faqat admin."""
    order = order_crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    order_crud.update_order_status(db, order, data.status)
    return {"success": True}