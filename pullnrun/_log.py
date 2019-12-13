def _status(output_dict):
    status = output_dict.get('status')
    if status == 'SUCCESS':
        return '\u2714'
    elif status in ('FAIL', 'ERROR', ):
        return '\u2718'
    elif status == 'STARTED':
        return '\u25B6'
    return ' '

def _http_details(output_dict):
    type_ = output_dict.get('type', '')
    status_code = str(output_dict.get('data', {}).get('status_code', '')).rjust(4)

    file_ = output_dict.get('data', {}).get('file', '')
    direction = 'to' if 'push' in type_ else 'from'
    url = output_dict.get('data', {}).get('url', '')

    detail = f'{file_} {direction} {url}'

    return (status_code, detail, )

def _s3_details(output_dict):
    type_ = output_dict.get('type', '')

    filename = output_dict.get('data', {}).get('filename', '')
    bucket = output_dict.get('data', {}).get('bucket', '')
    object_name = output_dict.get('data', {}).get('object_name', '')

    if 'push' in type_:
        direction = 'to'
        source, target = filename, object_name
    else:
        direction = 'from'
        source, target = object_name, filename

    target = f' as {target}' if source != target else ''
    detail = f'{source} {direction} S3 bucket {bucket}{target}'

    return detail

def _duration(output_dict):
    start = output_dict.get('meta', {}).get('start')
    end = output_dict.get('meta', {}).get('end')

    if not start or not end:
        return ''

    duration = end - start

    if duration >= 1000:
        return f'({duration/1000:.3f} s)'
    else:
        return f'({duration} ms)'

def log_to_console(output_dict):
    status = _status(output_dict)
    type_ = output_dict.get('type', '')
    stage = type_.upper()[:4].ljust(4)

    status_code = ''.rjust(4)
    detail = ''
    output = None

    if type_ in ('pull_http', 'push_http'):
        status_code, detail = _http_details(output_dict)
    elif type_ in ('pull_s3', 'push_s3'):
        detail = _s3_details(output_dict)
    elif type_ == 'run':
        status_code = str(output_dict.get('data', {}).get('exit_code', '')).rjust(4)
        detail = ' '.join(output_dict.get('data', {}).get('command', []))
        output = output_dict.get('data', {}).get('output')

    duration = _duration(output_dict)

    print(f'{status} {status_code} {stage} {detail} {duration}')

    if output:
        end = '\n' if output[-1] != '\n' else ''
        print(f'\n{output}{end}')