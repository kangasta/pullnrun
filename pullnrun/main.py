from argparse import ArgumentParser
from datetime import datetime
import json
import sys
import yaml

from jinja2 import __version__ as _jinja2_version

from ._version import __version__
from .execute import execute_task
from .utils.console import JsonStreams
from .utils.data import Settings, DEFAULT_SETTINGS_DICT, Statistics
from .utils.template import Environment
from .validate import validate_plan


INVALID_PLAN = 251
NO_PLAN = 252


def _name(input_dict):
    name = input_dict.get('name')
    if not name:
        return ''

    return f': {name}'


def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        'plan_file',
        type=str,
        nargs='?',
        help='Load execution plan from JSON or YAML file.')
    parser.add_argument(
        '--version',
        action='store_true',
        help='Print version information.')

    return parser.parse_args()


def load_plan_from_file(filename):
    if not filename:
        raise ValueError('No input file given.')

    with open(filename, 'r') as f:
        if filename.endswith('.json'):
            plan = json.load(f)
        elif filename.endswith('.yaml') or filename.endswith('.yml'):
            plan = yaml.load(f, Loader=yaml.SafeLoader)
        else:
            raise ValueError(
                'Failed to recognize file type. '
                'File extension must be json, yaml, or yml.')

    return plan


def main(plan):
    try:
        validate_plan(plan)
    except Exception as e:
        print(f'Failed to validate plan: {str(e)}')
        exit(INVALID_PLAN)

    env = Environment()
    plan_settings = Settings(DEFAULT_SETTINGS_DICT)(plan)
    stats = Statistics()
    console = JsonStreams(plan_settings.log_to_console)

    started = datetime.utcnow()
    tasks = plan.get('tasks')
    console.input(f'# Start plan execution{_name(plan)}')

    if plan.get('description'):
        console.log(plan.get('description'))

    console.input(f'# Print versions')
    console.log(f'pullnrun {__version__}')
    console.log(f'jinja2 {_jinja2_version}')
    console.log(f'python {sys.version}')
    console.log(sys.executable)
    env.register('pullnrun_python_executable', sys.executable)
    env.register('pullnrun_task_count', len(tasks))

    task_results = []

    for i, task in enumerate(tasks, start=1):
        env.register('pullnrun_task_index', i)

        task_result = execute_task(task, plan_settings, env)

        task_results.append(task_result)
        result = task_result.get('result')
        stats.add(result)
        env.register('pullnrun_last_result', result)
        if result in ('error', 'fail',):
            break

    elapsed = (datetime.utcnow() - started).total_seconds()

    console.input(text=f'# Plan execution completed{_name(plan)}')
    console.input(text=f'# Execution statistics{_name(plan)}')
    console.log(f'{"Started:":10} {started.isoformat()}Z')
    console.log(f'{"Elapsed:":10} {elapsed} s')
    console.log(stats.as_str(10))

    return (started, elapsed, stats, console.data)


def entrypoint():
    args = get_args()
    if args.version:
        print(f'pullnrun {__version__}')
        return

    try:
        plan = load_plan_from_file(args.plan_file)
    except ValueError as e:
        print(str(e))
        exit(NO_PLAN)

    _, _, stats, _ = main(plan)
    exit(stats.error + stats.fail)
