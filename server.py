from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

async def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        })

@app.post("/register")
async def register(data: RegData):
    await send_message( 
        data.user_id,
        f"✅ <b>Регистрация подтверждена!</b>\n\n"
        f"📌 <b>Ваши данные:</b>\n"
        f"👤 {data.fullname}\n"
        f"📧 {data.email}\n"
        f"📱 {data.phone}\n\n"
        f"До встречи на конференции! 🎉"
    )
    await send_message(
        ADMIN_ID,
        f"🔔 <b>Новая регистрация!</b>\n\n"
        f"👤 {data.fullname}\n"
        f"📧 {data.email}\n"
        f"📱 {data.phone}\n"
        f"🆔 user_id: {data.user_id}"
    )
    return {"ok": True}
