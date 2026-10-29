from telethon import events
from telethon.tl.functions.account import (
    GetAuthorizationsRequest,
    ResetAuthorizationRequest,
    ResetAuthorizationsRequest,
)
from bot import bot
from utils.decorators import join_check
from utils.helpers import ask_session


@bot.on(events.NewMessage(pattern="/me"))
@join_check
async def me(event):
    async with bot.conversation(event.chat_id) as conv:
        client = await ask_session(conv)
        if not client:
            return
        try:
            me = await client.get_me()
            username = f"@{me.username}" if me.username else "-"
            text = (
                f"**Account Info**\n"
                f"ID: `{me.id}`\n"
                f"Name: {me.first_name or ''} {me.last_name or ''}\n"
                f"Phone: `+{me.phone}`\n"
                f"Username: {username}\n"
                f"DC: `{client.session.dc_id}`"
            )
            await conv.send_message(text, parse_mode="md")
        finally:
            await client.disconnect()


@bot.on(events.NewMessage(pattern="/sessions"))
@join_check
async def sessions(event):
    async with bot.conversation(event.chat_id) as conv:
        client = await ask_session(conv)
        if not client:
            return
        try:
            res = await client(GetAuthorizationsRequest())
            lines = ["**Active Sessions**\n"]
            for auth in res.authorizations:
                lines.append(
                    f"Hash: `{auth.hash}`\n"
                    f"Device: {auth.device_model} ({auth.platform})\n"
                    f"IP: `{auth.ip}`\n"
                    f"Country: {auth.country}\n"
                    f"Created: {auth.date_created}\n"
                    f"Current: {'YES' if auth.current else 'NO'}\n"
                )
            await conv.send_message("\n".join(lines), parse_mode="md")
        finally:
            await client.disconnect()


@bot.on(events.NewMessage(pattern=r"/terminate(?: (.+))?"))
@join_check
async def terminate(event):
    async with bot.conversation(event.chat_id) as conv:
        client = await ask_session(conv)
        if not client:
            return
        try:
            target_hash = event.pattern_match.group(1)
            if target_hash:
                await client(ResetAuthorizationRequest(hash=int(target_hash)))
                await conv.send_message("Session terminated.")
            else:
                await client(ResetAuthorizationsRequest())
                await conv.send_message("All other sessions terminated.")
        except Exception as e:
            await conv.send_message(f"Error: `{e}`")
        finally:
            await client.disconnect()


@bot.on(events.NewMessage(pattern="/logout"))
@join_check
async def logout(event):
    async with bot.conversation(event.chat_id) as conv:
        client = await ask_session(conv)
        if not client:
            return
        try:
            await client.log_out()
            await conv.send_message("Session logged out and invalidated.")
        except Exception as e:
            await conv.send_message(f"Error: `{e}`")
        finally:
            await client.disconnect()
