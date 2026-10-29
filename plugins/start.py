from telethon import events
from bot import bot
from database import DB
from config import LOG_GROUP_ID
from utils.decorators import join_check


@bot.on(events.NewMessage(pattern="/start"))
@join_check
async def start(event):
    if DB:
        await DB.add_user(event.sender_id)

    text = (
        "👋 **APEX Session Control Bot**\n\n"
        "Main aapki **apni** Telegram sessions manage karne me help karta hoon.\n\n"
        "**Commands:**\n"
        "/gen - Naya session string generate karo\n"
        "/me - Account info dekho\n"
        "/sessions - Active sessions list karo\n"
        "/terminate - Doosri sessions band karo\n"
        "/logout - Session logout karo\n"
        "/help - Yeh menu"
    )
    await event.reply(text, parse_mode="md")

    if LOG_GROUP_ID:
        try:
            await bot.send_message(LOG_GROUP_ID, f"New user: `{event.sender_id}`")
        except Exception:
            pass


@bot.on(events.NewMessage(pattern="/help"))
async def help_cmd(event):
    await event.reply(
        "**Commands**\n"
        "/gen - Session string banao\n"
        "/me - Account info\n"
        "/sessions - Active sessions\n"
        "/terminate - Baaki sessions band karo\n"
        "/logout - Session logout karo",
        parse_mode="md",
    )
