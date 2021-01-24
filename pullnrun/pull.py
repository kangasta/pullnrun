from requests import request

from .utils.console import JsonStreams
from .utils.settings import DEFAULT_SETTINGS

def _write_to_file(response, filename):
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1<<20): # 1 MB
            if chunk: f.write(chunk)


def pull_http(url, method='GET', filename=None, extract=False, settings=DEFAULT_SETTINGS, **kwargs):
    console = JsonStreams(settings.log_to_console)
    console.input(f'# Pull {filename or "file"} from {url}')

    if not filename:
        filename = url.split('/')[-1]
        console.log(f'No filename defined, using {filename}.')

    try:
        with request(method, url, stream=True, **kwargs) as r:
            status_code = r.status_code
            console.log(f'{method.title()} {filename} returned {status_code}.')

            r.raise_for_status()
            _write_to_file(r, filename)
            console.log(f'Writing {filename} completed.')
    except Exception as e:
        console.error(f'Pulling {filename} failed: {str(e)}')
        return (False, console.data, )

    if extract:
        try:
            console.log('Unpacking archive.')
            unpack_archive(filename)
            console.log('Unpacking succeeded.')
        except Exception as e:
            console.error(f'Unpacking failed: {str(e)}')
            return (False, console.data, )

    return (True, console.data, )
