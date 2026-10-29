from telethon import TelegramClient
from telethon.sessions import StringSession
def new_client(api_id, api_hash):
    return TelegramClient(StringSession(), api_id, api_hash)
async def start(c):
    await c.connect()
async def send_code(c, phone):
    sent = await c.send_code_request(phone)
    return sent.phone_code_hash
async def sign_code(c, phone, code, h):
    try:
        await c.sign_in(phone=phone, code=code, phone_code_hash=h)
        return "success"
    except Exception as e:
        return "2fa_needed" if "password" in str(e).lower() else f"error:{e}"
async def sign_password(c, pw):
    try:
        await c.sign_in(password=pw)
        return "success"
    except Exception as e:
        return f"error:{e}"
async def export_and_close(c):
    s = c.session.save()
    await c.disconnect()
    return s