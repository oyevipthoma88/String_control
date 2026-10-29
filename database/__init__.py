from config import MONGO_URL
from logger import LOGGER
from .mongo import Mongo

DB = None
if MONGO_URL:
    DB = Mongo(MONGO_URL)
    LOGGER(__name__).info("MongoDB connected")
