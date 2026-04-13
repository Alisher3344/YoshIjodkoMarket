from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT sozlamalari
    SECRET_KEY: str = "maktab-market-secret-key-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 kun

    # Database
    DATABASE_URL: str = "sqlite:///./market.db"

    # Frontend URL (CORS uchun)
    CLIENT_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


# Barcha joyda shu obyekt import qilinadi
settings = Settings()