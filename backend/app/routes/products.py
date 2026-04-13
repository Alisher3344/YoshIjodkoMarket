from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models.models import Product
from ..auth import admin_only

router = APIRouter()

class ProductSchema(BaseModel):
    name_uz: str
    name_ru: str = ""
    desc_uz: str = ""
    desc_ru: str = ""
    price: float
    stock: int = 1
    category: str = ""
    author: str = ""
    class_uz: str = ""
    class_ru: str = ""
    school: str = ""
    district: str = ""
    phone: str = ""
    image: str = ""
    is_new: bool = True

@router.get("/")
def get_products(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    q = db.query(Product)
    if category and category != "all":
        q = q.filter(Product.category == category)
    if search:
        s = f"%{search.lower()}%"
        q = q.filter(
            Product.name_uz.ilike(s) |
            Product.name_ru.ilike(s) |
            Product.author.ilike(s)
        )
    return q.all()

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    return product

@router.post("/", dependencies=[Depends(admin_only)])
def create_product(data: ProductSchema, db: Session = Depends(get_db)):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/{product_id}", dependencies=[Depends(admin_only)])
def update_product(product_id: int, data: ProductSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    for key, value in data.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", dependencies=[Depends(admin_only)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    db.delete(product)
    db.commit()
    return {"success": True}