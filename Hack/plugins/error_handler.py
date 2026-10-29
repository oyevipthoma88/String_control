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

# ===== GLOBAL FIX: CallbackQuery.answer never raises =====
try:
    from telethon.events.callbackquery import CallbackQuery as _CQ
    if not getattr(_CQ.Event, "_apex_safe", False):
        _orig_answer = _CQ.Event.answer
        async def _safe_answer_method(self, *a, **kw):
            try:
                return await _orig_answer(self, *a, **kw)
            except Exception:
                return None
        _CQ.Event.answer = _safe_answer_method
        _CQ.Event._apex_safe = True
        import logging as _l
        _l.getLogger(__name__).info("CallbackQuery.answer patched")
except Exception as _e:
    import logging as _l
    _l.getLogger(__name__).warning("answer patch failed: %s", _e)
