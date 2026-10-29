from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
from apex.config import MUST_JOIN

BOT_NAME = "Apex Session Control"
TAGLINE = "Secure • Fast • Reliable"
PRIMARY = ButtonStyle.PRIMARY
DANGER = ButtonStyle.DANGER
SUCCESS = ButtonStyle.SUCCESS

START_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🔐 Generate", callback_data="gen", style=PRIMARY),
        InlineKeyboardButton("🗑️ Revoke", callback_data="revoke", style=DANGER),
    ],
    [InlineKeyboardButton("📊 Info", callback_data="info", style=SUCCESS)],
])
BACK_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🏠 Back", callback_data="start", style=SUCCESS)],
])
CANCEL_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("❌ Cancel", callback_data="cancel", style=DANGER)],
])
