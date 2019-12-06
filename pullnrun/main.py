import json
import os

from jsonschema import validate

from ._utils import as_list

from ._pull import pull
from ._push import push
from ._run import run

FUNCTION_MAPPINGS = {
    'pull': pull,
    'run': run,
    'push': push,
}

def _log(output_dict):
    output_str = json.dumps(output_dict)
    print(output_str)

def _validate(input_dict):
    base_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(base_path, 'schema.json'), 'r') as f:
        schema = json.load(f)

    validate(instance=input_dict, schema=schema)

def main(input_dict):
    _validate(input_dict)

    for stage, function in FUNCTION_MAPPINGS.items():
        for action in as_list(input_dict.get(stage)):
            output = function(**action)
            _log(output)

if __name__ == '__main__':
    main({'run': {'command': ['echo', 'asd']}})