import os
from dotenv import load_dotenv
load_dotenv()
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SUDOERS = list(map(int, os.getenv("SUDOERS", "").split())) if os.getenv("SUDOERS") else []
MONGO_URL = os.getenv("MONGO_URL", "")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0")) if os.getenv("LOG_GROUP_ID") else 0
MUST_JOIN = os.getenv("MUST_JOIN", "")
DISABLED = os.getenv("DISABLED", "").split()
if not API_ID: raise SystemExit("❌ API_ID missing in .env")
if not API_HASH: raise SystemExit("❌ API_HASH missing in .env")
if not BOT_TOKEN: raise SystemExit("❌ BOT_TOKEN missing in .env")
