from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from apex.helpers import START_KEYBOARD, BOT_NAME, TAGLINE, SUCCESS
from apex.database import db

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    await db.add_user(message.from_user.id, message.from_user.first_name)
    await message.reply(f"🛡️ **{BOT_NAME}**\n\n_{TAGLINE}_\n\nGenerate Pyrogram & Telethon sessions, manage 2FA, revoke access.", reply_markup=START_KEYBOARD)

@Client.on_callback_query(filters.regex("^start$"))
async def start_cb(client, cq: CallbackQuery):
    await cq.message.edit_text(f"🛡️ **{BOT_NAME}**\n\nChoose:", reply_markup=START_KEYBOARD)

@Client.on_callback_query(filters.regex("^cancel$"))
async def cancel_cb(client, cq: CallbackQuery):
    await cq.message.edit_text("❌ Cancelled.", reply_markup=START_KEYBOARD)

@Client.on_callback_query(filters.regex("^info$"))
async def info_cb(client, cq: CallbackQuery):
    u = cq.from_user
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Back", callback_data="start", style=SUCCESS)]])
    await cq.message.edit_text(f"👤 **Info**\n🆔 `{u.id}`\n📛 {u.first_name}\n🔗 @{u.username or None}", reply_markup=kb)

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message: Message):
    await message.reply("📖 **Apex Help**\n\n/start /help /ping\n\n🔐 Generate → API_ID → API_HASH → phone → OTP → (2FA) → string")
