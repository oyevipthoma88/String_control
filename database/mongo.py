from pymongo import AsyncMongoClient


class Mongo:
    def __init__(self, url: str):
        self.client = AsyncMongoClient(url)
        self.db = self.client.string_control
        self.users = self.db.users

    async def add_user(self, user_id: int):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id}},
            upsert=True,
        )

    async def get_users(self) -> list[int]:
        cursor = self.users.find({}, {"user_id": 1})
        return [doc["user_id"] async for doc in cursor]
