import sys

from jinja2 import __version__ as _jinja2_version

from pullnrun import __version__
from pullnrun.utils.data import DEFAULT_SETTINGS
from pullnrun.utils.console import JsonStreams


def log_versions(settings=DEFAULT_SETTINGS):
    console = JsonStreams(settings.log_to_console)

    console.input(f'# Log versions')
    console.log(f'pullnrun {__version__}')
    console.log(f'jinja2 {_jinja2_version}')
    console.log(f'python {sys.version}')
    console.log(sys.executable)

    return dict(success=True, console_data=console.data, )
