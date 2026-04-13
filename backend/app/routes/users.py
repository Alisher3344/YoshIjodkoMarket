from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models.models import User
from ..auth import admin_only, hash_password

router = APIRouter()

class UserSchema(BaseModel):
    name: str
    username: str
    password: str
    email: str = ""
    role: str = "admin"

class UserUpdateSchema(BaseModel):
    name: str
    username: str
    email: str = ""
    role: str = "admin"
    password: Optional[str] = None

@router.get("/", dependencies=[Depends(admin_only)])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "name": u.name,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "active": u.active,
            "createdAt": u.created_at
        }
        for u in users
    ]

@router.post("/", dependencies=[Depends(admin_only)])
def create_user(data: UserSchema, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.username == data.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Bu username band")
    user = User(
        name=data.name,
        username=data.username,
        password=hash_password(data.password),
        email=data.email,
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "username": user.username}

@router.put("/{user_id}", dependencies=[Depends(admin_only)])
def update_user(user_id: int, data: UserUpdateSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    user.name = data.name
    user.username = data.username
    user.email = data.email
    user.role = data.role
    if data.password:
        user.password = hash_password(data.password)
    db.commit()
    return {"success": True}

@router.delete("/{user_id}", dependencies=[Depends(admin_only)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    db.delete(user)
    db.commit()
    return {"success": True}

@router.patch("/{user_id}/toggle", dependencies=[Depends(admin_only)])
def toggle_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    user.active = not user.active
    db.commit()
    return {"success": True, "active": user.active}