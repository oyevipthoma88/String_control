import logging
from functools import wraps
from telethon.errors import FloodWaitError, RPCError
_LOG = logging.getLogger(__name__)

def safe(func):
    @wraps(func)
    async def w(event, *a, **kw):
        try:
            return await func(event, *a, **kw)
        except FloodWaitError as e:
            await event.reply(f"⏳ Flood wait {e.seconds}s")
        except RPCError as e:
            _LOG.error(f"RPC: {e}")
            await event.reply(f"❌ Telegram: {e}")
        except Exception as e:
            _LOG.exception("Unhandled")
            await event.reply(f"⚠️ {e}")
    return w
