import env
import asyncio
from telethon import events
from telethon.errors import FloodWaitError
from Hack import bot
from Hack.helpers import btn, P, S, D, DIV
from Hack.database import DB, settings

OWNERS = set(env.SUDOERS)
STATE = {}

def own(uid):
    return uid in OWNERS

PANEL_TEXT = (
    "<b>👑 Owner Control Panel</b>\n\n"
    "<blockquote>Live settings for the bot.</blockquote>"
)

def panel_kb():
    return [
        [btn("🖼 Start Pic", "OP_PIC", P), btn("📝 Start Text", "OP_TEXT", P)],
        [btn("📢 Support", "OP_SUPPORT", S), btn("🔒 Force Ch 1", "OP_F1", S)],
        [btn("🔗 Force Ch 2", "OP_F2", S), btn("📨 Broadcast", "OP_BC", D)],
        [btn("🛠 Maintenance", "OP_MAINT", D), btn("📊 Stats", "OP_STATS", S)],
        [btn("🏠 Back", "BACK_START", S)],
    ]

LABELS = {
    "START_PIC": ("🖼 Start Pic", "Send a direct image URL."),
    "START_TEXT": ("📝 Start Text", "Send new HTML text."),
    "SUPPORT": ("📢 Support", "Send a t.me link."),
    "MUST_JOIN": ("🔒 Force Channel 1", "Username without @."),
    "MUST_JOIN_2": ("🔗 Force Channel 2", "Username without @."),
    "MAINTENANCE": ("🛠 Maintenance", "Send on or off."),
}

@bot.on(events.NewMessage(pattern="/panel"))
async def panel(event):
    if not own(event.sender_id):
        return await event.reply("⛔ Owner only.")
    await event.reply(PANEL_TEXT, buttons=panel_kb(), parse_mode="html")

@bot.on(events.CallbackQuery(data=b"OP_OPEN"))
async def op_open(event):
    if not own(event.sender_id):
        return await event.answer("⛔ Owner only", alert=True)
    await event.edit(PANEL_TEXT, buttons=panel_kb(), parse_mode="html")

@bot.on(events.CallbackQuery(data=b"OP_BACK"))
async def op_back(event):
    await event.edit(PANEL_TEXT, buttons=panel_kb(), parse_mode="html")

async def _open(event, key):
    if not own(event.sender_id):
        return await event.answer("⛔", alert=True)
    label, hint = LABELS[key]
    cur = await settings.get(key, "")
    STATE[event.sender_id] = key
    await event.edit(f"<b>{label}</b>\n\n{hint}\n\nCurrent: <code>{cur or chr(45)}</code>", buttons=[[btn("🏠 Back", "OP_BACK", S)]], parse_mode="html")
@bot.on(events.CallbackQuery(data=b"OP_PIC"))
async def op_pic(event):
    await _open(event, "START_PIC")

@bot.on(events.CallbackQuery(data=b"OP_TEXT"))
async def op_text(event):
    await _open(event, "START_TEXT")

@bot.on(events.CallbackQuery(data=b"OP_SUPPORT"))
async def op_support(event):
    await _open(event, "SUPPORT")

@bot.on(events.CallbackQuery(data=b"OP_F1"))
async def op_f1(event):
    await _open(event, "MUST_JOIN")

@bot.on(events.CallbackQuery(data=b"OP_F2"))
async def op_f2(event):
    await _open(event, "MUST_JOIN_2")

@bot.on(events.CallbackQuery(data=b"OP_MAINT"))
async def op_maint(event):
    await _open(event, "MAINTENANCE")

@bot.on(events.CallbackQuery(data=b"OP_STATS"))
async def op_stats(event):
    if not own(event.sender_id):
        return await event.answer("⛔", alert=True)
    vals = await settings.all()
    users = 0
    try:
        if DB:
            users = await DB.count_users()
    except Exception:
        pass
    body = f"<b>📊 Stats</b>\n\n<b>Users:</b> <code>{users}</code>\n{DIV}\n"
    for k, v in vals.items():
        body += f"<b>{k}:</b> <code>{v or chr(45)}</code>\n"
    await event.edit(body, buttons=[[btn("🏠 Back", "OP_BACK", S)]], parse_mode="html")

@bot.on(events.CallbackQuery(data=b"OP_BC"))
async def op_bc(event):
    if not own(event.sender_id):
        return await event.answer("⛔", alert=True)
    STATE[event.sender_id] = "BROADCAST"
    await event.edit("📨 <b>Broadcast</b>\n\nSend the message.\n\n<i>/cancel to abort</i>", buttons=[[btn("🏠 Back", "OP_BACK", S)]], parse_mode="html")

@bot.on(events.NewMessage())
async def op_input(event):
    uid = event.sender_id
    if uid not in STATE:
        return
    if not event.is_private or not event.text:
        return
    if event.text == "/cancel":
        STATE.pop(uid, None)
        return await event.reply("❌ Cancelled.")
    key = STATE.pop(uid)
    val = event.text.strip()
    if key == "BROADCAST":
        return await do_broadcast(event, val)
    await settings.set(key, val)
    label = LABELS[key][0]
    await event.reply(f"✅ <b>{label}</b> updated:\n<code>{val}</code>", parse_mode="html", buttons=panel_kb())

async def do_broadcast(event, text):
    if not DB:
        return await event.reply("❌ No DB.")
    col = getattr(DB, "users", None)
    if col is None:
        db = getattr(DB, "db", None) or getattr(DB, "database", None)
        if db is not None:
            col = db["users"]
    if col is None:
        return await event.reply("❌ Users collection missing.")
    sent, failed = 0, 0
    status = await event.reply("📨 Broadcasting...")
    async for u in col.find({}):
        uid = u.get("user_id")
        if not uid:
            continue
        try:
            await bot.send_message(uid, text, parse_mode="html")
            sent += 1
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            try:
                await bot.send_message(uid, text, parse_mode="html")
                sent += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1
        if (sent + failed) % 20 == 0:
            try:
                await status.edit(f"📨 {sent} ✓ | ❌ {failed}")
            except Exception:
                pass
    await status.edit(f"✅ <b>Done</b>\n\nSent: <code>{sent}</code>\nFailed: <code>{failed}</code>", parse_mode="html")
