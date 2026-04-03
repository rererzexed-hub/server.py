from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

class RegData(BaseModel):
    fullname: str
    email: str
    phone: str
    user_id: int
    username: Optional[str] = ''
    first_name: Optional[str] = ''

async def send_photo(chat_id, photo_url, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "HTML"
        })

@app.post("/register")
async def register(data: RegData):
    if data.user_id:
        await send_photo(
            data.user_id,
            "https://i.postimg.cc/bd26ppTS/image.jpg",
            f"👤 {data.fullname}\n"
            f"📧 {data.email}\n"
            f"📱 {data.phone}\n\n"
            f"До встречи на конференции! 🎉"
        )

    username_str = f"@{data.username}" if data.username else "не указан"
    await send_message(
        ADMIN_ID,
        f"🔔 <b>Новая регистрация!</b>\n\n"
        f"👤 {data.fullname}\n"
        f"📧 {data.email}\n"
        f"📱 {data.phone}\n"
        f"🆔 Telegram: {username_str} ({data.user_id})"
    )
    return {"ok": True}
