import time
from pyrogram import Client, filters
from pyrogram.types import Message
from apex.config import OWNER_ID
from apex.database import db

@Client.on_message(filters.command("ping") & filters.user(OWNER_ID))
async def ping_cmd(client, message: Message):
    t0 = time.time()
    m = await message.reply("🏓 Pong...")
    await m.edit_text(f"🏓 **Pong!**\n`{(time.time()-t0)*1000:.2f} ms`")

@Client.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_cmd(client, message: Message):
    users = await db.count_users()
    await message.reply(f"📊 **Stats**\n👥 Users: `{users}`")
