import os
from dotenv import load_dotenv
load_dotenv()
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
MONGO_URL = os.getenv("MONGO_URL", "")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0"))
MUST_JOIN = os.getenv("MUST_JOIN", "").lstrip("@")
