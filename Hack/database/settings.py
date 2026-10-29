import logging
_LOG = logging.getLogger(__name__)
_cache = {}
try:
    from Hack.database import DB
except Exception:
    DB = None

def _col():
    if DB is None:
        return None
    if hasattr(DB, "settings"):
        return DB.settings
    for attr in ("db", "database"):
        obj = getattr(DB, attr, None)
        if obj is not None and hasattr(obj, "settings"):
            return obj.settings
    return None

async def get(key, default=None):
    if key in _cache:
        return _cache[key]
    col = _col()
    if col is None:
        return default
    doc = await col.find_one({"_id": key})
    val = doc["value"] if doc else default
    _cache[key] = val
    return val

async def set(key, value):
    col = _col()
    if col is not None:
        await col.update_one({"_id": key}, {"$set": {"value": value}}, upsert=True)
    _cache[key] = value
    return True

async def all():
    col = _col()
    out = dict(_cache)
    if col is None:
        return out
    async for d in col.find():
        out[d["_id"]] = d["value"]
    return out
