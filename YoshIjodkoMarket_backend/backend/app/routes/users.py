from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import require_admin
from ..crud import user as user_crud
from ..schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()


@router.get("/", dependencies=[Depends(require_admin)])
def get_users(db: Session = Depends(get_db)):
    """Barcha userlar — faqat admin."""
    users = user_crud.get_all(db)
    return [
        {
            "id":        u.id,
            "name":      u.name,
            "username":  u.username,
            "email":     u.email,
            "role":      u.role,
            "active":    u.active,
            "createdAt": u.created_at,
        }
        for u in users
    ]


@router.post("/", dependencies=[Depends(require_admin)])
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    """Yangi user yaratish — faqat admin."""
    exists = user_crud.get_by_username(db, data.username)
    if exists:
        raise HTTPException(status_code=400, detail="Bu username band")
    user = user_crud.create(db, data)
    return {"id": user.id, "name": user.name, "username": user.username}


@router.put("/{user_id}", dependencies=[Depends(require_admin)])
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    """User ma'lumotlarini yangilash — faqat admin."""
    user = user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    user_crud.update(db, user, data)
    return {"success": True}


@router.delete("/{user_id}", dependencies=[Depends(require_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Userni o'chirish — faqat admin."""
    user = user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    user_crud.delete(db, user)
    return {"success": True}


@router.patch("/{user_id}/toggle", dependencies=[Depends(require_admin)])
def toggle_user(user_id: int, db: Session = Depends(get_db)):
    """Userni aktiv/blok qilish — faqat admin."""
    user = user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    user_crud.toggle_active(db, user)
    return {"success": True, "active": user.active}