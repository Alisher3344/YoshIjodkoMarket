from typing import Optional
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import hash_password


def get_all(db: Session) -> list:
    """Barcha foydalanuvchilarni qaytaradi."""
    return db.query(User).all()


def get_by_id(db: Session, user_id: int) -> Optional[User]:
    """ID bo'yicha bitta user topadi."""
    return db.query(User).filter(User.id == user_id).first()


def get_by_username(db: Session, username: str) -> Optional[User]:
    """Login uchun username bo'yicha topadi."""
    return db.query(User).filter(User.username == username).first()


def create(db: Session, data: UserCreate) -> User:
    """
    Yangi user yaratadi.
    Parolni saqlashdan oldin hash qiladi.
    """
    user = User(
        name     = data.name,
        username = data.username,
        password = hash_password(data.password),
        email    = data.email,
        role     = data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User, data: UserUpdate) -> User:
    """
    User ma'lumotlarini yangilaydi.
    Yangi parol berilsa hash qilinadi.
    Berilmasa eski parol o'zgarmaydi.
    """
    user.name     = data.name
    user.username = data.username
    user.email    = data.email
    user.role     = data.role
    if data.password:
        user.password = hash_password(data.password)
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user: User) -> None:
    """Userni o'chiradi."""
    db.delete(user)
    db.commit()


def toggle_active(db: Session, user: User) -> User:
    """Userni aktiv yoki blok holatiga o'tkazadi."""
    user.active = not user.active
    db.commit()
    db.refresh(user)
    return user