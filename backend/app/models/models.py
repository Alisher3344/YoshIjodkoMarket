from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, default="")
    role = Column(String, default="admin")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name_uz = Column(String, nullable=False)
    name_ru = Column(String, default="")
    desc_uz = Column(Text, default="")
    desc_ru = Column(Text, default="")
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=1)
    category = Column(String, default="")
    author = Column(String, default="")
    class_uz = Column(String, default="")
    class_ru = Column(String, default="")
    school = Column(String, default="")
    district = Column(String, default="")
    phone = Column(String, default="")
    image = Column(String, default="")
    is_new = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    customer_address = Column(String, default="")
    items = Column(Text, default="[]")  # JSON string
    total = Column(Float, default=0)
    status = Column(String, default="new")
    payment_method = Column(String, default="cash")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CustomOrder(Base):
    __tablename__ = "custom_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    description = Column(Text, default="")
    budget = Column(String, default="")
    category = Column(String, default="")
    status = Column(String, default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())