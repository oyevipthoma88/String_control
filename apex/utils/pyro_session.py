from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired, PasswordHashInvalid
async def start_session(api_id, api_hash):
    c = Client(":memory:", api_id=api_id, api_hash=api_hash, in_memory=True)
    await c.connect()
    return c
async def request_code(c, phone):
    sent = await c.send_code(phone)
    return sent.phone_code_hash
async def sign_in_with_code(c, phone, ch, code):
    try:
        await c.sign_in(phone, ch, code)
        return "success"
    except SessionPasswordNeeded:
        return "2fa_needed"
    except (PhoneCodeInvalid, PhoneCodeExpired) as e:
        return f"error:{e}"
async def sign_in_with_password(c, pw):
    try:
        await c.check_password(pw)
        return "success"
    except PasswordHashInvalid:
        return "error:Invalid 2FA password"
async def export_and_close(c):
    s = await c.export_session_string()
    await c.disconnect()
    return s