import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

API_ID = 32488582   # <-- ВСТАВЬ СВОЙ
API_HASH = "e8ed14a11e9540b1c2ead640bf94e4a5"   # <-- ВСТАВЬ СВОЙ

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("sessions"):
    os.mkdir("sessions")

class PhoneRequest(BaseModel):
    phone: str

class CodeRequest(BaseModel):
    phone: str
    code: str
    password: str | None = None

def get_client(phone):
    return TelegramClient(f"sessions/{phone}", API_ID, API_HASH)

@app.post("/send_code")
async def send_code(data: PhoneRequest):
    client = get_client(data.phone)
    await client.connect()

    if await client.is_user_authorized():
        await client.disconnect()
        return {"status": "already_authorized"}

    await client.send_code_request(data.phone)
    await client.disconnect()

    return {"status": "code_sent"}

@app.post("/login")
async def login(data: CodeRequest):
    client = get_client(data.phone)
    await client.connect()

    try:
        await client.sign_in(data.phone, data.code)
    except SessionPasswordNeededError:
        if not data.password:
            await client.disconnect()
            return {"status": "2fa_required"}
        await client.sign_in(password=data.password)
    except Exception as e:
        await client.disconnect()
        return {"error": str(e)}

    me = await client.get_me()
    await client.disconnect()

    return {
        "status": "authorized",
        "user": {
            "id": me.id,
            "first_name": me.first_name,
            "username": me.username,
            "phone": me.phone
        }
    }
