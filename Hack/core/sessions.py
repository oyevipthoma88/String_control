import time
_C = {}
TTL = 3600

def get(uid):
    it = _C.get(uid)
    if not it:
        return None
    s, t = it
    if time.time() - t > TTL:
        _C.pop(uid, None)
        return None
    return s

def set(uid, s):
    _C[uid] = (s, time.time())

def clear(uid):
    _C.pop(uid, None)
