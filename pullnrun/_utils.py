import json
from time import time

def timestamp():
    return int(time() * 1000)

def as_list(a):
    if isinstance(a, list):
        return a
    if a is None:
        return []
    return [a]

def create_meta(start, end, **kwargs):
    try:
        json.dumps(kwargs)
    except:
        raise ValueError('kwargs should be JSON serializable')

    return {
        'start': start,
        'end': end,
        **kwargs
    }
