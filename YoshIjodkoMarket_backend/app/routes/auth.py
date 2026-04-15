from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import create_access_token, get_current_user, verify_password
from ..crud import user as user_crud
from ..schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    db_user = user_crud.get_by_username(db, data.username)
    if not db_user or not verify_password(data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Login yoki parol noto'g'ri")
    if not db_user.active:
        raise HTTPException(status_code=403, detail="Hisob bloklangan")
    token = create_access_token({"sub": str(db_user.id)})
    return {
        "token": token,
        "user": {
            "id":       db_user.id,
            "name":     db_user.name,
            "username": db_user.username,
            "role":     db_user.role,
        },
    }


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {
        "id":       current_user.id,
        "name":     current_user.name,
        "username": current_user.username,
        "role":     current_user.role,
    }