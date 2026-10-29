from telethon import events
from Hack import bot
from Hack.helpers import _btn, _S, START_TEXT, START_BUTTON, MENU1, KEYBOARD1


@bot.on(events.CallbackQuery(data=b"BACK_START"))
async def back_cb(event):
    await event.edit(START_TEXT, buttons=START_BUTTON, parse_mode="html")


@bot.on(events.CallbackQuery(data=b"VAULT"))
async def vault_cb(event):
    await event.edit(MENU1, buttons=KEYBOARD1, parse_mode="html")


@bot.on(events.CallbackQuery(data=b"ACCOUNT"))
async def account_cb(event):
    text = "<b>👤 Account</b>\n\n<blockquote>Tap B on the A-P keyboard for full info.</blockquote>"
    await event.edit(text, buttons=[[_btn("🏠 Back", "BACK_START", _S)]], parse_mode="html")


@bot.on(events.CallbackQuery(data=b"HELP"))
async def help_cb(event):
    text = "<b>📖 Apex Help</b>\n\n<blockquote>1. Tap Vault to open tools\n2. Send a valid session string\n3. Use A-P keyboard for actions</blockquote>"
    await event.edit(text, buttons=[[_btn("🏠 Back", "BACK_START", _S)]], parse_mode="html")


@bot.on(events.CallbackQuery(data=b"STATUS"))
async def status_cb(event):
    from Hack import botname, botusername
    text = f"<b>📡 Status</b>\n\n<blockquote>Bot: @{botusername}\nUser: {botname}\nStatus: live</blockquote>"
    await event.edit(text, buttons=[[_btn("🏠 Back", "BACK_START", _S)]], parse_mode="html")
