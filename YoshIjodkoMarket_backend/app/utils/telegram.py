import httpx
from ..core.config import settings


async def send_telegram(message: str) -> bool:
    if not settings.TELEGRAM_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
        async with httpx.AsyncClient() as client:
            await client.post(url, json={
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
            })
        return True
    except Exception:
        return False