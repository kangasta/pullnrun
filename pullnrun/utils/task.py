from jinja2.exceptions import UndefinedError


def _parse_task_settings(task, env, settings):
    try:
        when = env.resolve_expression(task.get('when'))
    except UndefinedError:
        when = False

    task = {
        **task,
        'when': when
    }

    task_settings = settings(task)
    name = task.pop('name', None)

    for key in settings.keys():
        task.pop(key, None)

    return (name, task, task_settings)


def parse_task(task, env, settings):
    name, task, task_settings = _parse_task_settings(task, env, settings)

    if not task_settings.when:
        return (name, None, None, task_settings)

    if len(task.keys()) != 1:
        raise ValueError(
            'Task must contain exactly one function key, '
            f'but {len(task.keys())} were given ({", ".join(task.keys())}).')
    function_name, parameters = next(i for i in task.items())

    if task_settings.resolve_templates:
        parameters = env.resolve_templates(parameters)

    return (name, function_name, parameters, task_settings,)


def parse_result(result):
    return (result.get('success'), result.get(
        'console_data'), result.get('vars'), )
