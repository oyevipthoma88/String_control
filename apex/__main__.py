import asyncio
from pyrogram import Client
from apex.config import API_ID, API_HASH, BOT_TOKEN
from apex.helpers import BOT_NAME, TAGLINE

async def main():
    app = Client("apex", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="apex.plugins"))
    await app.start()
    me = await app.get_me()
    print("=" * 50)
    print(f"🛡️  {BOT_NAME}")
    print(f"   {TAGLINE}")
    print(f"   @{me.username}")
    print("=" * 50)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
