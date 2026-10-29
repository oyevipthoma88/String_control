import env
from Hack import bot
from Hack.helpers import START_TEXT, START_BUTTON, log_deep
from Hack.database import DB
from telethon import events


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    uid = event.sender_id
    sender = await event.get_sender()
    if DB:
        try:
            await DB.add_user(uid)
        except Exception:
            pass
    pic = getattr(env, "START_PIC", "") or ""
    if pic:
        try:
            await bot.send_file(event.chat_id, pic, caption=START_TEXT, buttons=START_BUTTON, parse_mode="html")
        except Exception:
            await event.reply(START_TEXT, buttons=START_BUTTON, parse_mode="html")
    else:
        await event.reply(START_TEXT, buttons=START_BUTTON, parse_mode="html")
    try:
        await log_deep("🚀 Bot Started", sender)
    except Exception:
        pass


@bot.on(events.NewMessage(pattern="/hack"))
async def hack(event):
    if not event.is_private:
        return await event.reply("Private only.")
    from Hack.helpers import MENU1, KEYBOARD1
    await event.reply(MENU1, buttons=KEYBOARD1)
