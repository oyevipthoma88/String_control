from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization
from apex.helpers import CANCEL_KEYBOARD, BACK_KEYBOARD
waiting = set()
@Client.on_callback_query(filters.regex("^revoke$"))
async def revoke_start(client, cq: CallbackQuery):
    waiting.add(cq.from_user.id)
    await cq.message.edit_text("🗑️ **Revoke**\nPaste your **session string**:", reply_markup=CANCEL_KEYBOARD)
@Client.on_message(filters.private & filters.text, group=2)
async def revoke_handler(client, message: Message):
    uid = message.from_user.id
    if uid not in waiting:
        return
    waiting.discard(uid)
    uc = Client(":memory:", session_string=message.text.strip(), in_memory=True)
    try:
        await uc.connect()
        auths = await uc.invoke(GetAuthorizations())
        cur, n = auths.authorization_hash, 0
        for a in auths.authorizations:
            if a.hash != cur:
                await uc.invoke(ResetAuthorization(hash=a.hash))
                n += 1
        await uc.disconnect()
        await message.reply(f"✅ **Revoked {n} session(s).**", reply_markup=BACK_KEYBOARD)
    except Exception as e:
        try:
            await uc.disconnect()
        except Exception:
            pass
        await message.reply(f"❌ `{e}`", reply_markup=BACK_KEYBOARD)