from flask import Flask, request
from requests import Response

app = Flask(__name__)

@app.route('/file', methods=['PUT'])
def file_route():
    f = request.files['file']
    if f.read() == b'test_content' and f.filename == 'test_file.txt':
        return '', 200

    return '', 400

@app.route('/json', methods=['POST'])
def json_route():
    test_data = request.get_json()
    if test_data.get('test_key') == 'test_value':
        return '', 200

    return '', 400

test_client = app.test_client()

def request_mock_implementation(method, *args, **kwargs):
    fn = getattr(test_client, method.lower())

    files = kwargs.pop('files', None)
    if files:
        kwargs['data'] = files

    r = Response()
    r.status_code = fn(*args, **kwargs).status_code
    return r
