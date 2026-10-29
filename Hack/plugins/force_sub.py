import logging
import env
from telethon import events
from telethon.tl.custom import Button
from telethon.errors import UserNotParticipantError
from Hack import bot
from Hack.database import settings
from Hack.helpers import btn, P, S, D, DIV, safe_answer

_LOG = logging.getLogger(__name__)
_MEM = set()

async def _channels():
    out = []
    for key in ("MUST_JOIN", "MUST_JOIN_2"):
        ch = await settings.get(key, "") or getattr(env, key, "")
        ch = (ch or "").strip().lstrip("@")
        if ch and ch not in out:
            out.append(ch)
    return out

async def _is_member(user_id, channel):
    key = (user_id, channel)
    if key in _MEM:
        return True
    try:
        await bot.get_permissions(channel, user_id)
        _MEM.add(key)
        return True
    except UserNotParticipantError:
        return False
    except Exception as e:
        _LOG.warning("membership %s: %s", channel, e)
        return True

async def check(user_id):
    for ch in await _channels():
        if not await _is_member(user_id, ch):
            return False, ch
    return True, None

def join_buttons(channels):
    rows = [[Button.url(f"📢 Join @{ch}", f"https://t.me/{ch}")] for ch in channels]
    rows.append([btn("✅ I joined — Verify", "FS_VERIFY", S)])
    return rows

async def require(event):
    ok, missing = await check(event.sender_id)
    if ok:
        return True
    channels = await _channels()
    text = "<b>🔒 Join required</b>\n\nPlease join the channel(s) below, then tap <b>Verify</b>.\n\n" + DIV + "\n"
    for ch in channels:
        text += f"• @{ch}\n"
    text += DIV + "\n\n<i>After joining, tap Verify.</i>"
    await event.reply(text, buttons=join_buttons(channels), parse_mode="html")
    return False

@bot.on(events.CallbackQuery(data=b"FS_VERIFY"))
async def fs_verify(event):
    ok, missing = await check(event.sender_id)
    if not ok:
        return await safe_answer(event, f"❌ You haven't joined @{missing} yet.", alert=True)
    await safe_answer(event, "✅ Verified")
    try:
        await event.delete()
    except Exception:
        pass
    from Hack.plugins.start import show_start
    sender = await event.get_sender()
    await show_start(event.sender_id, sender)

@bot.on(events.CallbackQuery())
async def fs_guard(event):
    try:
        if event.data == b"FS_VERIFY":
            return
        if event.data.startswith(b"OP_"):
            return
        if event.sender_id in set(env.SUDOERS):
            return
        ok, _ = await check(event.sender_id)
        if not ok:
            await safe_answer(event, "🔒 Join the channel first.", alert=True)
            raise events.StopPropagation
    except events.StopPropagation:
        raise
    except Exception as e:
        _LOG.warning("fs_guard: %s", e)
