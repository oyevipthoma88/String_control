import base64
import struct
import asyncio
import ipaddress
import requests as r

from Hack import bot
from logger import LOGGER
from traceback import format_exc
from env import LOG_GROUP_ID, MUST_JOIN, DISABLED

from telethon import errors, Button
from telethon.events import CallbackQuery
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.sessions.string import _STRUCT_PREFORMAT, CURRENT_VERSION, StringSession
from telethon.errors.rpcerrorlist import UserNotParticipantError, UserIsBlockedError


MENU1 = '''
𝗔 - 𝗖𝗵𝗲𝗰𝗸 𝘂𝘀𝗲𝗿 𝗼𝘄𝗻 𝗴𝗿𝗼𝘂𝗽𝘀 𝗮𝗻𝗱 𝗰𝗵𝗮𝗻𝗻𝗲𝗹𝘀(𝗣𝗨𝗕𝗟𝗜𝗖 𝗢𝗡𝗟𝗬)

𝗕 - 𝗖𝗵𝗲𝗰𝗸 𝘂𝘀𝗲𝗿 𝗮𝗹𝗹 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 𝗹𝗶𝗸𝗲 𝗽𝗵𝗼𝗻𝗲 𝗻𝘂𝗺𝗯𝗲𝗿, 𝘂𝘀𝗿𝗻𝗮𝗺𝗲... 𝗲𝘁𝗰

𝗖 - 𝗕𝗮𝗻 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗺𝗲𝗺𝗯𝗲𝗿𝘀 𝗳𝗿𝗼𝗺 𝘁𝗵𝗲 𝗴𝗿𝗼𝘂𝗽

𝗗 - 𝗞𝗻𝗼𝘄 𝘂𝘀𝗲𝗿 𝗹𝗮𝘀𝘁 𝗼𝘁𝗽, 𝗨𝘀𝗲 𝗼𝗽𝘁𝗶𝗼𝗻 𝗕 𝗳𝗶𝗿𝘀𝘁 𝘁𝗼 𝘁𝗮𝗸𝗲 𝗻𝘂𝗺𝗯𝗲𝗿 𝘁𝗵𝗲𝗻 𝗹𝗼𝗴𝗶𝗻

𝗘 - 𝗝𝗼𝗶𝗻 𝗔 𝗚𝗿𝗼𝘂𝗽/𝗖𝗵𝗮𝗻𝗻𝗲𝗹/𝗟𝗶𝗻𝗸 𝘃𝗶𝗮 𝗦𝘁𝗿𝗶𝗻𝗴𝗦𝗲𝘀𝘀𝗶𝗼𝗻

𝗙 - 𝗟𝗲𝗮𝘃𝗲 𝗔 𝗚𝗿𝗼𝘂𝗽/𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝘃𝗶𝗮 𝗦𝘁𝗿𝗶𝗻𝗴𝗦𝗲𝘀𝘀𝗶𝗼𝗻

𝗚 - 𝗗𝗲𝗹𝗲𝘁𝗲 𝗔 𝗚𝗿𝗼𝘂𝗽/𝗖𝗵𝗮𝗻𝗻𝗲𝗹

𝗛 - 𝗖𝗵𝗲𝗰𝗸 𝘂𝘀𝗲𝗿 𝘁𝘄𝗼 𝘀𝘁𝗲𝗽 𝗶𝘀 𝗲𝗻𝗲𝗮𝗯𝗹𝗲 𝗼𝗿 𝗱𝗶𝘀𝗮𝗯𝗹𝗲
'''

MENU2 = '''
𝗜 - 𝗧𝗲𝗿𝗺𝗶𝗻𝗮𝘁𝗲 𝗔𝗹𝗹 𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝗮𝗰𝘁𝗶𝘃𝗲 𝘀𝗲𝘀𝘀𝗶𝗼𝗻𝘀 𝗲𝘅𝗰𝗲𝗽𝘁 𝗬𝗼𝘂𝗿 𝗦𝘁𝗿𝗶𝗻𝗴𝗦𝗲𝘀𝘀𝗶𝗼𝗻

𝗝 - 𝗗𝗲𝗹𝗲𝘁𝗲 𝗔𝗰𝗰𝗼𝘂𝗻𝘁

𝗞 - 𝗟𝗲𝗮𝘃𝗲 𝗔𝗹𝗹 𝗚𝗿𝗼𝘂𝗽𝘀/𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀

𝗟 - 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗕𝘂𝘁𝘁𝗼𝗻𝘀

𝗠 - 𝗧𝗲𝗿𝗺𝗶𝗻𝗮𝘁𝗲 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗦𝗲𝘀𝘀𝗶𝗼𝗻

𝗡 - 𝗜𝗻𝘃𝗶𝘁𝗲 𝗔𝗹𝗹

𝗢 - 𝗗𝗲𝗺𝗼𝘁𝗲 𝗮 𝗺𝗲𝗺𝗯𝗲𝗿

𝗣 - 𝗣𝗿𝗼𝗺𝗼𝘁𝗲 𝗮 𝗺𝗲𝗺𝗯𝗲𝗿
'''

BROADCAST_BUTTONS = [[
    Button.inline("Group", data="1"),
    Button.inline("User", data="2"),
], [
    Button.inline("All", data="3"),
]]

BROADCAST_OPTION = {
    b"1": {
        "group": True
    },
    b"2": {
        "user": True
    },
    b"3": {
        "group": True,
        "user": True
    }
}

KEYBOARD1 = [
    [
        Button.inline("A", data="A"),
        Button.inline("B", data="B"),
        Button.inline("C", data="C"),
        Button.inline("D", data="D")
    ],
    [
        Button.inline("E", data="E"),
        Button.inline("F", data="F"),
        Button.inline("G", data="G"),
        Button.inline("H", data="H")
    ],
    [
        Button.inline("𝗡𝗘𝗫𝗧 ⏭️", data="next")
    ]
]

KEYBOARD2 = [
    [
        Button.inline("I", data="I"),
        Button.inline("J", data="J"),
        Button.inline("K", data="K"),
        Button.inline("L", data="L")
    ],
    [
        Button.inline("M", data="M"),
        Button.inline("N", data="N"),
        Button.inline("O", data="O"),
        Button.inline("P", data="P")
    ],
    [
        Button.inline(" 𝗕𝗔𝗖𝗞 ⏮️", data="back")
    ]
]


async def join_checker(e):
    if not MUST_JOIN:
        return True
    chat = await bot.get_entity(MUST_JOIN)
    try:
        await bot(GetParticipantRequest(chat, e.sender_id))
        return True
    except UserNotParticipantError:
        join_chat = f"https://t.me/{chat.username}"
        button = [[
            Button.url(text="Join", url=join_chat),
        ]]

        TEXT = "Hey looks like you haven't join our chat yet, Please join first!"

        await bot.send_message(e.sender_id, TEXT, buttons=button)

        return False
    except Exception as err:
        LOGGER(__name__).error(err)
        return True


def paste(text):
    link = 'https://spaceb.in/'
    url = 'https://spaceb.in/api/v1/documents'
    payload = {"content": text, "extension": "txt"}
    headers = {
        "Content-Type": "application/json"
    }

    response = r.post(url, json=payload, headers=headers)
    hash = response.json().get('payload').get('id')

    return link + hash


def on_callback(data=None):
    def dec(func):
        async def wrap(e):
            check = await join_checker(e)
            if not check:
                return

            if func.__name__ in DISABLED:
                await e.answer("This function is currently disabled", alert=True)
                return
            try:
                await func(e)
            except errors.common.AlreadyInConversationError:
                pass
            except (asyncio.CancelledError, UserIsBlockedError):
                return
            except Exception as err:
                ERROR_TXT = f'ERROR MESSAGE:- {err}'
                ERROR_TXT += f'\n\nERROR TRACEBACK:- {format_exc()}'
                if LOG_GROUP_ID:
                    try:
                        link = paste(ERROR_TXT)
                        await bot.send_message(LOG_GROUP_ID, link, link_preview=False)
                    except:
                        pass
                else:
                    LOGGER(__name__).error(ERROR_TXT)
                await e.reply('Some Error occur from bot side. Please report it to @MASTIWITHFRIENDSXD')

        bot.add_event_handler(wrap, CallbackQuery(data=data))

    return dec



# https://github.com/TeamUltroid/Ultroid/blob/main/pyUltroid/startup/connections.py

_PYRO_FORM = {351: ">B?256sI?", 356: ">B?256sQ?", 362: ">BI?256sQ?"}

DC_IPV4 = {
    1: "149.154.175.53",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.130",
}


def validate_session(session):
    # Telethon Session
    if session.startswith(CURRENT_VERSION):
        if len(session.strip()) != 353:
            return False
        return StringSession(session)

    # Pyrogram Session
    elif len(session) in _PYRO_FORM.keys():
        if len(session) in [351, 356]:
            dc_id, _, auth_key, _, _ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" *
                                         (-len(session) % 4)),
            )
        else:
            dc_id, _, _, auth_key, _, _ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" *
                                         (-len(session) % 4)),
            )
        return StringSession(CURRENT_VERSION + base64.urlsafe_b64encode(
            struct.pack(
                _STRUCT_PREFORMAT.format(4),
                dc_id,
                ipaddress.ip_address(DC_IPV4[dc_id]).packed,
                443,
                auth_key,
            )).decode("ascii"))
    else:
        return False

# ===== APEX BRANDING =====
MENU1 = """🛡️ APEX STRING CONTROL
A Channels | B Info | C Ban | D OTP
E Join | F Leave | G Delete | H 2FA
"""
MENU2 = """🛡️ APEX STRING CONTROL
I Terminate | J Delete-acc | K Leave-all | L Broadcast
M Logout | N Scrap | O Demote | P Promote
"""

# ===== COLOURED KEYBOARD OVERRIDE =====
try:
    from telethon.tl.types import KeyboardButtonStyle as _KBS
    _P = _KBS(bg_primary=True)
    _D = _KBS(bg_danger=True)
    _S = _KBS(bg_success=True)
except Exception:
    _P = _D = _S = None

def _btn(t, d, s=None):
    if s is not None:
        try:
            from telethon.tl.types import KeyboardButtonCallback
            return KeyboardButtonCallback(text=t, data=d.encode() if isinstance(d, str) else d, style=s)
        except Exception:
            pass
    return Button.inline(t, data=d)

KEYBOARD1 = [
    [_btn("A", "A", _P), _btn("B", "B", _P), _btn("C", "C", _D), _btn("D", "D", _P)],
    [_btn("E", "E", _P), _btn("F", "F", _P), _btn("G", "G", _D), _btn("H", "H", _S)],
    [_btn("𝗡𝗘𝗫𝗧 ⏭️", "next", _S)],
]
KEYBOARD2 = [
    [_btn("I", "I", _D), _btn("J", "J", _D), _btn("K", "K", _D), _btn("L", "L", _P)],
    [_btn("M", "M", _D), _btn("N", "N", _P), _btn("O", "O", _S), _btn("P", "P", _S)],
    [_btn("𝗕𝗔𝗖𝗞 ⏮️", "back", _S)],
]


# ===== APEX PREMIUM UI =====
from datetime import datetime

START_TEXT = (
    "<b>🛡️ APEX STRING CONTROL</b>\n"
    "<i>Secure · Fast · Reliable</i>\n\n"
    "<blockquote>Your Telegram session cockpit. Create, inspect and revoke "
    "Pyrogram & Telethon sessions — with bank-grade hygiene.</blockquote>\n\n"
    "<b>⚡ Telethon 1.45</b> · <b>🎨 Bot API 9.4</b> · <b>🔒 Encrypted Vault</b>\n\n"
    "<i>Tap a module below to begin.</i>"
)

START_BUTTON = [
    [_btn("🔐 Vault", "VAULT", _P), _btn("📊 Account", "ACCOUNT", _P)],
    [_btn("📖 Help", "HELP", _S), _btn("📡 Status", "STATUS", _S)],
]


async def log_deep(title, user, extra=""):
    try:
        import env
        from Hack import bot
        if not env.LOG_GROUP_ID:
            return
        name = user.first_name or "—"
        uname = getattr(user, "username", None)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body = f"<b>{title}</b>\n\n"
        body += f"<b>Name:</b> {name}\n"
        body += f"<b>ID:</b> <code>{user.id}</code>\n"
        if uname:
            body += f"<b>User:</b> @{uname}\n"
        body += f"<b>Time:</b> <code>{ts}</code>\n"
        if extra:
            body += "\n" + extra
        await bot.send_message(env.LOG_GROUP_ID, body, parse_mode="html")
    except Exception:
        pass

# ===== FINAL OVERRIDE (Telethon 1.45 strings) =====
import logging as _lg
_ULOG = _lg.getLogger(__name__)

# Bot API 9.4 styles as STRINGS (Telethon 1.45 expects strings)
_P = "primary"
_D = "danger"
_S = "success"

def _btn(t, d, s=None):
    """Create inline button with optional style string."""
    from telethon.tl.custom import Button
    try:
        if s:
            return Button.inline(t, data=d, style=s)
        return Button.inline(t, data=d)
    except Exception as e:
        _ULOG.warning(f"_btn fallback: {e}")
        return Button.inline(t, data=d)

KEYBOARD1 = [
    [_btn("A","A",_P), _btn("B","B",_P), _btn("C","C",_D), _btn("D","D",_P)],
    [_btn("E","E",_P), _btn("F","F",_P), _btn("G","G",_D), _btn("H","H",_S)],
    [_btn("▶ Next","next",_S)],
]
KEYBOARD2 = [
    [_btn("I","I",_D), _btn("J","J",_D), _btn("K","K",_D), _btn("L","L",_P)],
    [_btn("M","M",_D), _btn("N","N",_P), _btn("O","O",_S), _btn("P","P",_S)],
    [_btn("◀ Back","back",_S)],
]

START_TEXT = (
    "<b>🛡️ APEX STRING CONTROL</b>\n"
    "<i>Secure · Fast · Reliable</i>\n\n"
    "<b>Your Telegram session cockpit.</b>\n"
    "Create, inspect and revoke Pyrogram & Telethon sessions with bank-grade hygiene.\n\n"
    "━━━━━━━━━━━━━━━\n"
    "<b>⚡ Features</b>\n"
    "• Pyrogram & Telethon sessions\n"
    "• 2FA protected vault\n"
    "• One-tap revoke\n"
    "• Encrypted storage\n"
    "━━━━━━━━━━━━━━━\n\n"
    "<i>Tap a module below to begin.</i>"
)

START_BUTTON = [
    [_btn("🔐 Vault","VAULT",_P), _btn("📊 Account","ACCOUNT",_P)],
    [_btn("📖 Help","HELP",_S), _btn("📡 Status","STATUS",_S)],
]

# ===== APEX FINAL UI OVERRIDE =====
import logging as _lg
from datetime import datetime as _dt
from telethon.tl.custom import Button as _Button

_ULOG = _lg.getLogger(__name__)

P = "primary"
D = "danger"
S = "success"
_P, _D, _S = P, D, S

def btn(text, data, style=None):
    try:
        if style:
            return _Button.inline(text, data=data, style=style)
        return _Button.inline(text, data=data)
    except Exception as e:
        _ULOG.warning("btn fallback: %s", e)
        return _Button.inline(text, data=data)

_btn = btn

DIV = "━━━━━━━━━━━━━━━"

START_TEXT = (
    "<b>🛡️ APEX STRING CONTROL</b>\n"
    "<i>Secure · Fast · Reliable</i>\n\n"
    "<b>Your Telegram session cockpit.</b>\n"
    "Create, inspect and revoke Pyrogram & Telethon sessions — with bank-grade hygiene.\n\n"
    f"{DIV}\n"
    "<b>⚡ What you can do</b>\n"
    "• Generate a string session\n"
    "• Check 2FA and account info\n"
    "• Revoke every other device\n"
    "• Manage groups and channels\n"
    f"{DIV}\n\n"
    "<i>Tap a module below to begin.</i>"
)

def start_buttons(is_owner=False):
    rows = [
        [btn("🔐 Session Vault", "VAULT", P), btn("👤 My Account", "ACCOUNT", P)],
        [btn("📖 Help", "HELP", S), btn("📡 Bot Status", "STATUS", S)],
    ]
    if is_owner:
        rows.append([btn("👑 Owner Panel", "OP_OPEN", D)])
    return rows

START_BUTTON = start_buttons(False)

MENU1 = (
    "<b>🔐 SESSION VAULT — Part 1</b>\n"
    "<i>Account & chat tools</i>\n\n"
    f"{DIV}\n"
    "<b>A</b> 📢 Channels — list every channel you own\n"
    "<b>B</b> 👤 Account — ID, name, phone, DC\n"
    "<b>C</b> 🚫 Ban all — ban every member in a group\n"
    "<b>D</b> 🔍 OTP finder — read recent login codes\n"
    "<b>E</b> ➕ Join — join a group or channel\n"
    "<b>F</b> ➖ Leave — leave a group or channel\n"
    "<b>G</b> 🗑 Delete — delete a group or channel you own\n"
    "<b>H</b> 🔐 2FA — check if two-step is enabled\n"
    f"{DIV}\n"
    "<i>Tap A–H below · Next for part 2</i>"
)

MENU2 = (
    "<b>🔐 SESSION VAULT — Part 2</b>\n"
    "<i>Sessions & admin tools</i>\n\n"
    f"{DIV}\n"
    "<b>I</b> 🛑 Terminate — kill every other session\n"
    "<b>J</b> ⚠️ Delete account — permanent, cannot undo\n"
    "<b>K</b> 🚪 Leave all — leave every chat\n"
    "<b>L</b> 📨 Broadcast — message all your chats\n"
    "<b>M</b> 🔓 Logout — end this session\n"
    "<b>N</b> 🧲 Scrap — export members and invite\n"
    "<b>O</b> ⬇️ Demote — remove admin rights\n"
    "<b>P</b> ⬆️ Promote — grant admin rights\n"
    f"{DIV}\n"
    "<i>Tap I–P below · Back for part 1</i>"
)

KEYBOARD1 = [
    [btn("A", "A", P), btn("B", "B", P), btn("C", "C", D), btn("D", "D", P)],
    [btn("E", "E", P), btn("F", "F", P), btn("G", "G", D), btn("H", "H", S)],
    [btn("▶ Next", "next", S)],
]
KEYBOARD2 = [
    [btn("I", "I", D), btn("J", "J", D), btn("K", "K", D), btn("L", "L", P)],
    [btn("M", "M", D), btn("N", "N", P), btn("O", "O", S), btn("P", "P", S)],
    [btn("◀ Back", "back", S)],
]

async def log_deep(title, user, extra=""):
    try:
        import env
        from Hack import bot
        if not env.LOG_GROUP_ID:
            return
        name = getattr(user, "first_name", None) or "—"
        uname = getattr(user, "username", None)
        ts = _dt.now().strftime("%Y-%m-%d %H:%M:%S")
        body = f"<b>{title}</b>\n\n"
        body += f"<b>👤 Name:</b> {name}\n"
        body += f"<b>🆔 ID:</b> <code>{user.id}</code>\n"
        if uname:
            body += f"<b>🔗 Username:</b> @{uname}\n"
        body += f"<b>🕐 Time:</b> <code>{ts}</code>\n"
        if extra:
            body += "\n" + extra
        await bot.send_message(env.LOG_GROUP_ID, body, parse_mode="html")
    except Exception:
        pass

# ===== SAFE HELPERS =====
import asyncio as _asy

def valid_url(u):
    if not u or not isinstance(u, str):
        return False
    u = u.strip()
    return u.startswith("http://") or u.startswith("https://")

async def safe_answer(event, text=None, alert=False):
    try:
        await event.answer(text, alert=alert)
    except Exception:
        pass
