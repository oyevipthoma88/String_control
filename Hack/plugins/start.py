import env
import logging
from Hack import bot
from Hack.helpers import START_TEXT, START_BUTTON, log_deep
from Hack.database import DB
from Hack.database import settings
from telethon import events
_LOG = logging.getLogger(__name__)

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    try:
        uid = event.sender_id
        sender = await event.get_sender()
        if DB:
            try:
                await DB.add_user(uid)
            except Exception:
                pass
        pic = await settings.get("START_PIC", getattr(env, "START_PIC", "") or "")
        text = await settings.get("START_TEXT", START_TEXT)
        if pic:
            try:
                await bot.send_file(event.chat_id, file=pic, caption=text, buttons=START_BUTTON, parse_mode="html")
            except Exception as e:
                _LOG.warning(f"START_PIC failed: {e}")
                await event.reply(text, buttons=START_BUTTON, parse_mode="html")
        else:
            await event.reply(text, buttons=START_BUTTON, parse_mode="html")
        try:
            await log_deep("🚀 Bot Started", sender)
        except Exception:
            pass
    except Exception as e:
        _LOG.exception("start failed")
        await event.reply(f"⚠️ Error: {e}")

@bot.on(events.NewMessage(pattern="/hack"))
async def hack(event):
    if not event.is_private:
        return await event.reply("Private only.")
    from Hack.helpers import MENU1, KEYBOARD1
    await event.reply(MENU1, buttons=KEYBOARD1)
