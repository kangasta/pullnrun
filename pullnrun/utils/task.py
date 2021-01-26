def parse_task(task, env, settings):
    task_settings = settings(task)

    task = {**task}
    name = task.pop('name', None)
    for key in settings.keys():
        task.pop(key, None)

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
