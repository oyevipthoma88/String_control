from motor.motor_asyncio import AsyncIOMotorClient
from apex.config import MONGO_URL

class Database:
    def __init__(self):
        if not MONGO_URL:
            self.users = self.sessions = None
            return
        c = AsyncIOMotorClient(MONGO_URL)
        self.users = c["apex_db"]["users"]
        self.sessions = c["apex_db"]["sessions"]

    async def add_user(self, uid, name):
        if self.users:
            await self.users.update_one({"user_id": uid}, {"$set": {"first_name": name}}, upsert=True)

    async def count_users(self):
        return await self.users.count_documents({}) if self.users else 0

    async def save_session(self, uid, kind, s):
        if self.sessions:
            await self.sessions.update_one({"user_id": uid, "type": kind}, {"$set": {"session": s}}, upsert=True)

db = Database()
