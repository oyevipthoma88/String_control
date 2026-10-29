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

def _normalize(ch):
    """Return (kind, ident, url) where kind = 'public' / 'private' / None."""
    ch = (ch or "").strip()
    if not ch:
        return None
    # Full URL
    if ch.startswith("http://") or ch.startswith("https://"):
        low = ch.lower()
        if "t.me/+" in low or "/joinchat/" in low:
            return ("private", ch, ch)
        parts = low.rstrip("/").split("/")
        if "t.me" in parts:
            idx = parts.index("t.me")
            if idx + 1 < len(parts):
                name = parts[idx + 1]
                return ("public", name, f"https://t.me/{name}")
        return ("private", ch, ch)
    # Plain username
    name = ch.lstrip("@")
    return ("public", name, f"https://t.me/{name}")

async def _channels():
    out, seen = [], set()
    for key in ("MUST_JOIN", "MUST_JOIN_2"):
        raw = await settings.get(key, "") or getattr(env, key, "")
        n = _normalize(raw)
        if n and n[1] not in seen:
            out.append(n)
            seen.add(n[1])
    return out

async def _is_member(user_id, kind, ident):
    if kind == "private":
        return True  # can't verify invite-only — trust user
    key = (user_id, ident)
    if key in _MEM:
        return True
    try:
        await bot.get_permissions(ident, user_id)
        _MEM.add(key)
        return True
    except UserNotParticipantError:
        return False
    except Exception as e:
        _LOG.warning("membership %s: %s", ident, e)
        return True

async def check(user_id):
    for kind, ident, url in await _channels():
        if not await _is_member(user_id, kind, ident):
            return False, ident
    return True, None

def join_buttons(channels):
    rows = []
    for kind, ident, url in channels:
        label = "Invite" if kind == "private" else ident
        rows.append([Button.url(f"📢 Join {label}", url)])
    rows.append([btn("✅ I joined — Verify", "FS_VERIFY", S)])
    return rows

async def require(event):
    ok, missing = await check(event.sender_id)
    if ok:
        return True
    channels = await _channels()
    text = (
        "<b>🔒 Join required</b>\n\n"
        "Please join the channel(s) below, then tap <b>Verify</b>.\n\n"
        f"{DIV}\n"
    )
    for kind, ident, url in channels:
        text += f"• <a href='{url}'>{ident if kind=='public' else 'Invite Link'}</a>\n"
    text += f"{DIV}\n\n<i>After joining, tap Verify.</i>"
    await event.reply(text, buttons=join_buttons(channels), parse_mode="html", link_preview=False)
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
        if event.data.startswith(b"OP_") or event.data.startswith(b"OWNER_"):
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
