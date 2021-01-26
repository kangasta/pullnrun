from .builtin import functions
from .utils.console import JsonStreams
from .utils.task import parse_task, parse_return_value


def _name(input_dict):
    name = input_dict.get('name')
    if not name:
        return ''

    return f': {name}'


def execute_task(task_data, plan_settings, env):
    console = JsonStreams(plan_settings.log_to_console)

    task_index = env.get('pullnrun_task_index')
    task_count = env.get('pullnrun_task_count')
    task_progress = (
        f' {task_index}/{task_count}' if task_index and task_count else '')

    task = parse_task(task_data, env, plan_settings)
    if task.error:
        console.error(f'Failed to parse task: {task.error}')
        return task.result(console, 'error')

    if not task.settings.when:
        console.input(f'# Skip task {task_progress}{_name(task_data)}')
        return task.result(console, 'skipped')

    console.input(
        f'# Execute task{task_progress}: {task.name or task.function}')
    if task.description:
        console.log(task.description)
    function = functions.get(task.function)
    if not function:
        console.error(f'Function not found for {task.function}.')
        return task.result(console, 'error')

    try:
        return_value = function(**task.parameters, settings=task.settings)
        success, console_data, new_vars = parse_return_value(return_value)
    except Exception as e:
        console.error(f'Caught error raised from task: {str(e)}')
        return task.result(console, 'error')

    if task.settings.register:
        env.register(task.settings.register, return_value)
    if new_vars:
        for key, value in new_vars.items():
            env.register(key, value)

    console.extend(console_data)
    result = 'success' if success else 'fail'
    return task.result(console, result, )
