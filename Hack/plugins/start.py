import env
import logging
from Hack import bot
from Hack.helpers import start_buttons, log_deep, DIV, START_TEXT as DEFAULT_TEXT
from Hack.database import DB, settings
from Hack.plugins import force_sub
from telethon import events

_LOG = logging.getLogger(__name__)

async def show_start(uid, sender):
    text = await settings.get("START_TEXT", "")
    if not text or len(text) < 20:
        text = DEFAULT_TEXT
    pic = await settings.get("START_PIC", "") or getattr(env, "START_PIC", "")
    is_owner = uid in set(env.SUDOERS)
    kb = start_buttons(is_owner)
    if pic:
        try:
            await bot.send_file(uid, file=pic, caption=text, buttons=kb, parse_mode="html")
        except Exception as e:
            _LOG.warning("start pic: %s", e)
            await bot.send_message(uid, text, buttons=kb, parse_mode="html")
    else:
        await bot.send_message(uid, text, buttons=kb, parse_mode="html")

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
        if await settings.get("MAINTENANCE", "off") == "on" and uid not in set(env.SUDOERS):
            return await event.reply("🛠 <b>Maintenance mode</b>\n\nPlease try again later.", parse_mode="html")
        if not await force_sub.require(event):
            return
        await show_start(uid, sender)
        try:
            await log_deep("🚀 Bot Started", sender)
        except Exception:
            pass
    except Exception as e:
        _LOG.exception("start failed")
        await event.reply(f"⚠️ {e}")

@bot.on(events.NewMessage(pattern="/hack"))
async def hack(event):
    if not event.is_private:
        return await event.reply("Private only.")
    if not await force_sub.require(event):
        return
    from Hack.helpers import MENU1, KEYBOARD1
    await event.reply(MENU1, buttons=KEYBOARD1, parse_mode="html")
