from typing import Optional
from sqlalchemy.orm import Session

from ..models.product import Product
from ..schemas.product import ProductCreate


def get_all(
    db: Session,
    category: Optional[str] = None,
    search: Optional[str] = None,
) -> list:
    """
    Barcha mahsulotlarni qaytaradi.
    category berilsa — shu kategoriya bo'yicha filter qiladi.
    search berilsa — nom va muallif bo'yicha qidiradi.
    """
    q = db.query(Product)

    if category and category != "all":
        q = q.filter(Product.category == category)

    if search:
        s = f"%{search.lower()}%"
        q = q.filter(
            Product.name_uz.ilike(s)
            | Product.name_ru.ilike(s)
            | Product.author.ilike(s)
        )

    return q.all()


def get_by_id(db: Session, product_id: int) -> Optional[Product]:
    """ID bo'yicha bitta mahsulot topadi. Topilmasa None qaytaradi."""
    return db.query(Product).filter(Product.id == product_id).first()


def create(db: Session, data: ProductCreate) -> Product:
    """Yangi mahsulot yaratadi va DB ga saqlaydi."""
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update(db: Session, product: Product, data: ProductCreate) -> Product:
    """Mavjud mahsulotni yangilaydi."""
    for key, value in data.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete(db: Session, product: Product) -> None:
    """Mahsulotni o'chiradi."""
    db.delete(product)
    db.commit()