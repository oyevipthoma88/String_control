from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from config import MUST_JOIN, SUDOERS
from logger import LOGGER


def sudo_only(func):
    async def wrapper(event):
        if event.sender_id not in SUDOERS:
            await event.reply("⛔ You are not authorized.")
            return
        return await func(event)
    return wrapper


def join_check(func):
    async def wrapper(event):
        if not MUST_JOIN:
            return await func(event)
        try:
            chat = await event.client.get_entity(MUST_JOIN)
            await event.client(GetParticipantRequest(chat, event.sender_id))
        except UserNotParticipantError:
            await event.reply(f"📢 Please join @{MUST_JOIN} first, then try again.")
            return
        except Exception as e:
            LOGGER(__name__).warning(f"Force-sub check failed: {e}")
        return await func(event)
    return wrapper
