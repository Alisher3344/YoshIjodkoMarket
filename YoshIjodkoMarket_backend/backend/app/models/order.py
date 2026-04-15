from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from ..core.database import Base


class Order(Base):
    """
    Buyurtmalar jadvali.
    items — JSON string ko'rinishida saqlanadi:
    [{"id": 1, "name_uz": "Kitob", "price": 15000, "qty": 2}]
    status: new | processing | done | cancelled
    """
    __tablename__ = "orders"

    id               = Column(Integer, primary_key=True, index=True)
    customer_name    = Column(String, nullable=False)
    customer_phone   = Column(String, nullable=False)
    customer_address = Column(String, default="")
    items            = Column(Text, default="[]")
    total            = Column(Float, default=0)
    status           = Column(String, default="new")
    payment_method   = Column(String, default="cash")
    created_at       = Column(DateTime(timezone=True), server_default=func.now())


class CustomOrder(Base):
    """
    Maxsus buyurtmalar — mijoz o'zi tavsif yozadi.
    status: new | processing | done | cancelled
    """
    __tablename__ = "custom_orders"

    id             = Column(Integer, primary_key=True, index=True)
    customer_name  = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    description    = Column(Text, default="")
    budget         = Column(String, default="")
    category       = Column(String, default="")
    status         = Column(String, default="new")
    created_at     = Column(DateTime(timezone=True), server_default=func.now())