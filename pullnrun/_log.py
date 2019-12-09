def _http_details(output_dict):
    type_ = output_dict.get('type', '')
    status = str(output_dict.get('data', {}).get('status', '')).rjust(4)

    file_ = output_dict.get('data', {}).get('file', '')
    direction = 'to' if 'push' in type_ else 'from'
    url = output_dict.get('data', {}).get('url', '')

    detail = f'{file_} {direction} {url}'

    return (status, detail, )

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

def log_to_console(output_dict):
    ok = '\u2714' if output_dict.get('ok') else '\u2718'
    type_ = output_dict.get('type', '')
    stage = type_.upper()[:4].ljust(4)

    status = ''.rjust(4)
    detail = ''
    output = None

    if type_ in ('pull_http', 'push_http'):
        status, detail = _http_details(output_dict)
    elif type_ in ('pull_s3', 'push_s3'):
        detail = _s3_details(output_dict)
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