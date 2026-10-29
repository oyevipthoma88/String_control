from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message
from apex.helpers import CANCEL_KEYBOARD, BACK_KEYBOARD
from apex.database import db
from apex.utils import pyro_session

states = {}

@Client.on_callback_query(filters.regex("^gen$"))
async def gen_start(client, cq: CallbackQuery):
    states[cq.from_user.id] = {"step": "api_id"}
    await cq.message.edit_text("🔐 **1/4** Send **API_ID** (my.telegram.org):", reply_markup=CANCEL_KEYBOARD)

@Client.on_message(filters.private & filters.text, group=1)
async def session_input(client, message: Message):
    uid = message.from_user.id
    st = states.get(uid)
    if not st:
        return
    step, text = st.get("step"), message.text.strip()
    if step == "api_id":
        try:
            st["api_id"] = int(text)
        except ValueError:
            return await message.reply("❌ Invalid.", reply_markup=CANCEL_KEYBOARD)
        st["step"] = "api_hash"
        return await message.reply("**2/4** Send **API_HASH**:", reply_markup=CANCEL_KEYBOARD)
    if step == "api_hash":
        st["api_hash"] = text
        st["step"] = "phone"
        return await message.reply("**3/4** Send **phone** with country code:", reply_markup=CANCEL_KEYBOARD)
    if step == "phone":
        st["phone"] = text
        try:
            c = await pyro_session.start_session(st["api_id"], st["api_hash"])
            st["code_hash"] = await pyro_session.request_code(c, text)
            st["client"] = c
            st["step"] = "code"
            return await message.reply("**4/4** Send **OTP**:", reply_markup=CANCEL_KEYBOARD)
        except Exception as e:
            states.pop(uid, None)
            return await message.reply(f"❌ `{e}`", reply_markup=BACK_KEYBOARD)
    if step == "code":
        r = await pyro_session.sign_in_with_code(st["client"], st["phone"], st["code_hash"], text.replace(" ", ""))
        if r == "success":
            s = await pyro_session.export_and_close(st["client"])
            states.pop(uid, None)
            await db.save_session(uid, "pyrogram", s)
            return await message.reply(f"✅ **Session:**\n\n`{s}`", reply_markup=BACK_KEYBOARD)
        if r == "2fa_needed":
            st["step"] = "password"
            return await message.reply("🔒 **2FA** — Send password:", reply_markup=CANCEL_KEYBOARD)
        states.pop(uid, None)
        return await message.reply(f"❌ `{r}`", reply_markup=BACK_KEYBOARD)
    if step == "password":
        r = await pyro_session.sign_in_with_password(st["client"], text)
        if r == "success":
            s = await pyro_session.export_and_close(st["client"])
            states.pop(uid, None)
            await db.save_session(uid, "pyrogram", s)
            return await message.reply(f"✅ **Session:**\n\n`{s}`", reply_markup=BACK_KEYBOARD)
        states.pop(uid, None)
        return await message.reply(f"❌ `{r}`", reply_markup=BACK_KEYBOARD)
