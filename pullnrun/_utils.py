import json
from time import time

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

def filter_dict(dict_, keys):
    return {k: v for k, v in dict_.items() if k in keys}

def get_log_entry(type_, status, start=None, end=None, **data):
    return {
        'type': type_,
        'status': status,
        'data': data,
        'meta': create_meta(start, end)
    }

def timestamp():
    return int(time() * 1000)

def void_fn(*_args, **_kwargs):
    return None