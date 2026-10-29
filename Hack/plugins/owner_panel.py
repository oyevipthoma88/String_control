import env
from telethon import events
from Hack import bot
from Hack.helpers import _btn, _P, _S, _D
from Hack.database import settings

OWNERS = set(env.SUDOERS)
STATE = {}

def own(uid):
    return uid in OWNERS

PANEL_TEXT = "<b>🛡️ Owner Control Panel</b>\n\n<blockquote>Manage bot settings live.</blockquote>"

def panel_kb():
    return [
        [_btn("🖼 Start Pic","OP_PIC",_P), _btn("📝 Start Text","OP_TEXT",_P)],
        [_btn("📢 Support","OP_SUPPORT",_S), _btn("🔒 Force Sub","OP_FORCE",_S)],
        [_btn("🛠 Maintenance","OP_MAINT",_D), _btn("📊 Stats","OP_STATS",_S)],
        [_btn("🏠 Back","BACK_START",_S)],
    ]

LABELS = {
    "START_PIC": ("🖼 Start Pic","Send direct image URL."),
    "START_TEXT": ("📝 Start Text","Send new HTML text."),
    "SUPPORT": ("📢 Support","Send support link."),
    "MUST_JOIN": ("🔒 Force Sub","Send channel username without @."),
    "MAINTENANCE": ("🛠 Maintenance","Send on/off."),
}

@bot.on(events.NewMessage(pattern="/panel"))
async def panel(event):
    if not own(event.sender_id):
        return await event.reply("⛔ Owner only.")
    await event.reply(PANEL_TEXT, buttons=panel_kb(), parse_mode="html")

@bot.on(events.CallbackQuery(data=b"OP_BACK"))
async def op_back(event):
    await event.edit(PANEL_TEXT, buttons=panel_kb(), parse_mode="html")

async def _open(event, key):
    if not own(event.sender_id):
        return await event.answer("⛔", alert=True)
    label, hint = LABELS[key]
    cur = await settings.get(key, "")
    STATE[event.sender_id] = key
    await event.edit(f"<b>{label}</b>\n\n{hint}\n\nCurrent: <code>{cur}</code>", buttons=[[_btn("🏠 Back","OP_BACK",_S)]], parse_mode="html")

@bot.on(events.CallbackQuery(data=b"OP_PIC"))
async def op_pic(event):
    await _open(event, "START_PIC")

@bot.on(events.CallbackQuery(data=b"OP_TEXT"))
async def op_text(event):
    await _open(event, "START_TEXT")

@bot.on(events.CallbackQuery(data=b"OP_SUPPORT"))
async def op_support(event):
    await _open(event, "SUPPORT")

@bot.on(events.CallbackQuery(data=b"OP_FORCE"))
async def op_force(event):
    await _open(event, "MUST_JOIN")

@bot.on(events.CallbackQuery(data=b"OP_MAINT"))
async def op_maint(event):
    await _open(event, "MAINTENANCE")

@bot.on(events.CallbackQuery(data=b"OP_STATS"))
async def op_stats(event):
    vals = await settings.all()
    body = "<b>📊 Stats</b>\n\n"
    for k, v in vals.items():
        body += f"<b>{k}</b>: <code>{v}</code>\n"
    await event.edit(body, buttons=[[_btn("🏠 Back","OP_BACK",_S)]], parse_mode="html")

@bot.on(events.NewMessage())
async def op_input(event):
    uid = event.sender_id
    if uid not in STATE:
        return
    if not event.is_private or not event.text:
        return
    key = STATE.pop(uid)
    val = event.text.strip()
    await settings.set(key, val)
    label, _ = LABELS[key]
    await event.reply(f"✅ <b>{label}</b> updated:\n<code>{val}</code>", parse_mode="html", buttons=panel_kb())
