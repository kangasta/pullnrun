from requests import request
from shutil import make_archive

try:
    import boto3
    S3 = boto3.client('s3')
except ImportError:
    pass

from ._utils import timestamp, create_meta, filter_dict

def _push_http(filename, url, method='PUT', data=None, headers=None):
    ok = True
    status = None

    start = timestamp()
    try:
        with open(filename, 'rb') as f:
            files = {'file': (filename, f)}
            r = request(method, url, data=data, headers=headers, files=files)
            status = r.status_code
            r.raise_for_status()
    except:
        ok = False
    end = timestamp()

    return {
        'type': 'push_http',
        'ok': ok,
        'data': {
            'url': url,
            'file': filename,
            'status': status,
        },
        'meta': create_meta(start, end)
    }

def _push_s3(bucket, filename, object_name=None):
    if not object_name:
        object_name = filename

    ok = None

    start = timestamp()
    try:
        S3.upload_file(filename, bucket, object_name)
        ok=True
    except:
        ok=False
    end = timestamp()

    return {
        'type': 'push_s3',
        'ok': ok,
        'data': {
            'bucket': bucket,
            'object_name': object_name,
            'filename': filename,
        },
        'meta': create_meta(start, end)
    }

def push(**kwargs):
    to = kwargs.get('to')
    if to == 'url':
        keys = ('filename', 'url', 'method', 'data', 'headers', )
        return _push_http(**filter_dict(kwargs, keys))
    elif to == 's3':
        keys = ('bucket', 'object_name', 'filename')
        return _push_s3(**filter_dict(kwargs, keys))
