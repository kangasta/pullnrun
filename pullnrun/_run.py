import subprocess

from ._utils import timestamp, get_log_entry

def run(log, command, directory=None):
    kwargs = {
        'stdout': subprocess.PIPE,
        'stderr': subprocess.STDOUT,
        'text': True,
    }

    status = 'STARTED'
    returncode = None
    stdout = None

    start = timestamp()
    log(get_log_entry('run', status, command=command, start=start))

    try:
        cp = subprocess.run(command, cwd=directory, check=False, **kwargs)
        returncode = cp.returncode
        status = 'SUCCESS' if returncode == 0 else 'FAIL'
        stdout = str(cp.stdout)
    except:
        status = 'ERROR'
    end = timestamp()

    log(get_log_entry('run', status, command=command, exit_code=returncode, output=stdout, start=start, end=end))
    return status == 'SUCCESS'
