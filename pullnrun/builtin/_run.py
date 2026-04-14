from ciou.streams import run

from pullnrun.utils.data import DEFAULT_SETTINGS
from pullnrun.utils.task import parse_return_value


def run_command(command, settings=DEFAULT_SETTINGS, **kwargs):
    result = run(command, log_to_console=settings.log_to_console, **kwargs)

    return dict(
        success=result.success,
        console_data=result.console,
    )


def run_script(script, settings=DEFAULT_SETTINGS, **kwargs):
    console_data = []

    for command in script:
        success, new_lines, _ = parse_return_value(
            run_command(command, settings, **kwargs))
        console_data.extend(new_lines)

        if settings.stop_on_errors and not success:
            return dict(success=False, console_data=console_data, )

    return dict(success=True, console_data=console_data, )
