from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


# SQLite engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Har bir request uchun yangi session ochiladi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Barcha modellar shu Base dan meros oladi
Base = declarative_base()


def get_db():
    """
    FastAPI Depends() orqali ishlatiladi.
    Request tugagach session avtomatik yopiladi.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()