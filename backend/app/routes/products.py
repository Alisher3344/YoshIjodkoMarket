from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import require_admin
from ..crud import product as product_crud
from ..schemas.product import ProductCreate, ProductResponse

router = APIRouter()


@router.get("/")
def get_products(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Barcha mahsulotlar — category va search bo'yicha filter."""
    return product_crud.get_all(db, category=category, search=search)


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """ID bo'yicha bitta mahsulot."""
    product = product_crud.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    return product


@router.post("/", dependencies=[Depends(require_admin)])
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    """Yangi mahsulot yaratish — faqat admin."""
    return product_crud.create(db, data)


@router.put("/{product_id}", dependencies=[Depends(require_admin)])
def update_product(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    """Mahsulotni yangilash — faqat admin."""
    product = product_crud.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    return product_crud.update(db, product, data)


@router.delete("/{product_id}", dependencies=[Depends(require_admin)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Mahsulotni o'chirish — faqat admin."""
    product = product_crud.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    product_crud.delete(db, product)
    return {"success": True}