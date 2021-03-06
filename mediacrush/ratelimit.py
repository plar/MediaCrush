from .config import _cfg, _cfgi
from .database import r, _k
from .network import get_ip

from flask import request


def rate_limit_exceeded():
    consumed = int(r.get(_k("rate_limit.%s" % get_ip())))
    if not consumed:
        return False

    return consumed >= _cfgi("bytes_per_hour")


def rate_limit_update(f):
    key = _k("rate_limit.%s" % get_ip())
    f.seek(0, 2)
    b = f.tell()
    f.seek(0)

    if not r.exists(key):
        r.setex(key, 3600, b)
    else:
        r.incrby(key, b)
