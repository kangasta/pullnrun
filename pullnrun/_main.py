import json

try:
    import importlib.resources as resources
except ImportError:
    import importlib_resources as resources

from jsonschema import validate

from ._utils import as_list
from ._log import log_to_console

from ._pull import pull
from ._push import push
from ._run import run

FUNCTION_MAPPINGS = {
    'pull': pull,
    'run': run,
    'push': push,
}

def _validate(input_dict):
    schema = json.loads(resources.read_text('pullnrun', 'schema.json'))
    validate(instance=input_dict, schema=schema)

def main(input_dict, log=log_to_console):
    _validate(input_dict)
    success, error = (0, 0, )

    for stage, function in FUNCTION_MAPPINGS.items():
        for action in as_list(input_dict.get(stage)):
            ok = function(log=log, **action)
            if ok:
                success += 1
            else:
                error += 1

    return (success, error, )
