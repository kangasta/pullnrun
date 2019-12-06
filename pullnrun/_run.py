import subprocess

from ._utils import timestamp, create_meta

def run(command, directory=None):
    kwargs = {
        'stdout': subprocess.PIPE,
        'stderr': subprocess.STDOUT,
        'text': True,
    }

    ok = True
    args = None
    returncode = None
    stdout = None

    start = timestamp()
    try:
        cp = subprocess.run(command, cwd=directory, **kwargs)
        args = cp.args
        returncode = cp.returncode
        stdout = str(cp.stdout)
    except:
        ok = False
    end = timestamp()

    return {
        'type': 'run',
        'ok': ok and (returncode == 0),
        'data': {
            'command': args,
            'exit_code': returncode,
            'output': stdout,
        },
        'meta': create_meta(start, end)
    }
