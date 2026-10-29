from telethon import events, TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError,
    PasswordHashInvalidError,
)
from bot import bot
from config import API_ID, API_HASH
from utils.decorators import join_check


@bot.on(events.NewMessage(pattern="/gen"))
@join_check
async def gen(event):
    async with bot.conversation(event.chat_id) as conv:
        await conv.send_message(
            "Apna phone number international format me bhejo (e.g. `+919876543210`):",
            parse_mode="md",
        )
        phone_msg = await conv.get_response()
        phone = phone_msg.text.strip()
        await phone_msg.delete()

        client = TelegramClient(StringSession(), API_ID, API_HASH)
        await client.connect()

        try:
            sent = await client.send_code_request(phone)

            await conv.send_message("Telegram par aaya hua OTP bhejo:")
            otp_msg = await conv.get_response()
            otp = otp_msg.text.strip().replace(" ", "")
            await otp_msg.delete()

            try:
                await client.sign_in(
                    phone, code=otp, phone_code_hash=sent.phone_code_hash
                )
            except SessionPasswordNeededError:
                await conv.send_message("2-Step Verification on hai. Password bhejo:")
                pw_msg = await conv.get_response()
                pw = pw_msg.text.strip()
                await pw_msg.delete()
                await client.sign_in(password=pw)

            string = StringSession.save(client.session)

            await conv.send_message(
                f"**Your session string:**\n\n`{string}`\n\n"
                "Ise kisi ke saath share mat karo.",
                parse_mode="md",
            )

        except PhoneCodeInvalidError:
            await conv.send_message("Invalid OTP. `/gen` dobara try karo.")
        except PasswordHashInvalidError:
            await conv.send_message("Invalid 2FA password. `/gen` dobara try karo.")
        except Exception as e:
            await conv.send_message(f"Error: `{e}`")
        finally:
            await client.disconnect()
