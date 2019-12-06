import json

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

def main(input_dict):
    for stage, function in FUNCTION_MAPPINGS.items():
        for action in as_list(input_dict.get(stage)):
            output = function(**action)
            _log(output)

if __name__ == '__main__':
    main({'run': {'command': ['echo', 'asd']}})