import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

MONGO_URL = os.getenv("MONGO_URL") or None
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID")) if os.getenv("LOG_GROUP_ID") else None
MUST_JOIN = os.getenv("MUST_JOIN") or None
SUDOERS = [int(x) for x in os.getenv("SUDOERS", "").split() if x.isdigit()]

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise SystemExit("API_ID, API_HASH and BOT_TOKEN are required.")
