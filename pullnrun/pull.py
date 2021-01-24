from os import path
import re

from requests import request

from.run import run_command, run_script
from .utils.console import JsonStreams
from .utils.settings import DEFAULT_SETTINGS

def _write_to_file(response, filename):
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1<<20): # 1 MB
            if chunk: f.write(chunk)


def pull_git(url, target=None, branch=None, settings=DEFAULT_SETTINGS):
    console = JsonStreams(settings.log_to_console)
    console.input(f'# Pull repository from {url}')

    if not target:
        match = re.search(r'/([^/]*).git/{0,1}$', url)
        target = match.group(1) if match else ''

    if target and path.isdir(target):
        commands = [
            'git fetch',
            f'git checkout origin/{branch or "HEAD"}'
        ]
        cwd = target
    else:
        branch_option = f'--branch {branch}' if branch else ''
        commands = [
            f'git clone {branch_option} {url} {target}'
        ]
        cwd = None

    return run_script(commands, settings, cwd=cwd)


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
