from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db

# Bcrypt hasher — parollarni xavfsiz saqlaydi
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Request headerdan Bearer token o'qiydi
security = HTTPBearer()


# ── Parol funksiyalari ─────────────────────────────────────────────────────

def verify_password(plain: str, hashed: str) -> bool:
    """Kiritilgan parolni DB dagi hash bilan solishtiradi."""
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    """Parolni bcrypt bilan hashlaydi — DB ga shu saqlanadi."""
    return pwd_context.hash(password)


# ── JWT funksiyalari ───────────────────────────────────────────────────────

def create_access_token(data: dict) -> str:
    """
    JWT token yaratadi.
    data = {"sub": "user_id"}
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# ── Dependency funksiyalar ─────────────────────────────────────────────────

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Himoyalangan har bir endpointda token tekshiradi.
    Token to'g'ri bo'lsa User obyektini qaytaradi.
    """
    # Bu import shu yerda — circular import oldini olish uchun
    from ..models.user import User

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token noto'g'ri")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token noto'g'ri")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.active:
        raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi")
    return user


def require_admin(current_user=Depends(get_current_user)):
    """
    Faqat admin roliga ruxsat beradi.
    Admin bo'lmasa 403 Forbidden qaytaradi.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Ruxsat yo'q — faqat admin")
    return current_user