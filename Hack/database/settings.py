import logging

_LOG = logging.getLogger(__name__)
_cache = {}

DEFAULTS = {
    "START_PIC": "",
    "START_TEXT": "",
    "SUPPORT": "",
    "MUST_JOIN": "",
    "MUST_JOIN_2": "",
    "MAINTENANCE": "off",
}

def _col():
    try:
        from Hack.database import DB
        if DB is None:
            return None
        if getattr(DB, "settings", None) is not None:
            return DB.settings
        for attr in ("db", "database"):
            obj = getattr(DB, attr, None)
            if obj is not None:
                return obj["settings"]
    except Exception:
        pass
    return None

async def get(key, default=None):
    if key in _cache:
        return _cache[key]
    col = _col()
    if col is None:
        val = DEFAULTS.get(key, default)
        _cache[key] = val
        return val
    doc = await col.find_one({"_id": key})
    val = doc["value"] if doc else DEFAULTS.get(key, default)
    _cache[key] = val
    return val

async def set(key, value):
    col = _col()
    if col is not None:
        await col.update_one({"_id": key}, {"$set": {"value": value}}, upsert=True)
    _cache[key] = value
    return True

async def all():
    out = dict(DEFAULTS)
    out.update(_cache)
    col = _col()
    if col is not None:
        async for d in col.find():
            out[d["_id"]] = d["value"]
    return out

async def reset(key):
    col = _col()
    if col is not None:
        await col.delete_one({"_id": key})
    _cache.pop(key, None)
