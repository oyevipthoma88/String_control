from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH


async def create_client(session_str: str = "") -> TelegramClient:
    client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
    await client.connect()
    return client


async def ask_session(conv) -> TelegramClient | None:
    await conv.send_message("🔑 Apna session string bhejo:")
    msg = await conv.get_response()
    session_str = msg.text.strip()
    await msg.delete()

    client = await create_client(session_str)
    if not await client.is_user_authorized():
        await conv.send_message("❌ Invalid ya expired session string.")
        await client.disconnect()
        return None
    return client
