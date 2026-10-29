import env
import logging
from Hack import bot
from Hack.helpers import _btn, _P, _S, _D, log_deep
from Hack.database import DB
from Hack.database import settings
from telethon import events
_LOG = logging.getLogger(__name__)


def _menu(event):
    b = [
        [_btn("🔐 Vault","VAULT",_P), _btn("📊 Account","ACCOUNT",_P)],
        [_btn("📖 Help","HELP",_S), _btn("📡 Status","STATUS",_S)],
    ]
    if event.sender_id in set(env.SUDOERS):
        b.append([_btn("👑 Owner Panel","OP_OPEN",_D)])
    return b


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
        text = await settings.get("START_TEXT", "")
        if not text or not isinstance(text, str) or len(text) < 20:
            from Hack.helpers import START_TEXT as _def
            text = _def
        kb = _menu(event)
        if pic:
            try:
                await bot.send_file(event.chat_id, file=pic, caption=text, buttons=kb, parse_mode="html")
            except Exception as e:
                _LOG.warning(f"START_PIC failed: {e}")
                await event.reply(text, buttons=kb, parse_mode="html")
        else:
            await event.reply(text, buttons=kb, parse_mode="html")
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
    from Hack.helpers import MENU1, KEYBOARD1
    await event.reply(MENU1, buttons=KEYBOARD1)
