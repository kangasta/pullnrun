def log_to_console(output_dict):
    ok = '\u2714' if output_dict.get('ok') else '\u2718'
    type_ = output_dict.get('type', '')
    stage = type_.upper().ljust(4)

    status = ''.rjust(4)
    detail = ''
    output = None

    if type_ in ('pull', 'push'):
        status = str(output_dict.get('data', {}).get('status', '')).rjust(4)
        file_ = output_dict.get('data', {}).get('file', '')
        url = output_dict.get('data', {}).get('file', '')
        direction = 'to' if type_ == 'push' else 'from'
        detail = f'{file_} {direction} {url}'
    elif type_ == 'run':
        status = str(output_dict.get('data', {}).get('exit_code', '')).rjust(4)
        detail = ' '.join(output_dict.get('data', {}).get('command', []))
        output = output_dict.get('data', {}).get('output')

    start = output_dict.get('meta', {}).get('start', 0)
    end = output_dict.get('meta', {}).get('end', 0)

    print(f'{ok} {status} {stage} {detail} ({end - start} ms)')

    if output:
        end = '\n' if output[-1] != '\n' else ''
        print(f'\n{output}{end}')