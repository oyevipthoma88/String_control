import asyncio
import signal
import sys

try:
    import uvloop
    uvloop.install()
except ImportError:
    pass

from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN
from logger import LOGGER

bot = TelegramClient("apex_session_bot", API_ID, API_HASH)


async def shutdown(sig, loop):
    LOGGER(__name__).info(f"Received {sig.name}, shutting down...")
    await bot.disconnect()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def main():
    await bot.start(bot_token=BOT_TOKEN)
    LOGGER(__name__).info("Bot started")

    from plugins import ALL_MODULES
    import importlib

    for module in ALL_MODULES:
        importlib.import_module(f"plugins.{module}")
    LOGGER(__name__).info("Plugins loaded")

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown(s, loop)))

    await bot.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
