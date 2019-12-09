from unittest import TestCase
from unittest.mock import patch

from pullnrun._log import log_to_console

class LogTest(TestCase):
    @patch('builtins.print')
    def test_log_to_console_does_not_crash_on_empty_input(self, print_mock):
        log_to_console({})
        print_mock.assert_called()

    @patch('builtins.print')
    def test_log_to_console_prints_logs_as_specified(self, print_mock):
        url = 'example.com'
        f = 'filename'

        testdata = [
            # Type and status
            ({'type': 'pull_http', 'data': {
                'file': f,
                'url': url,
            }}, [f, 'from', url], []),
            ({'type': 'push_http', 'data': {
                'file': f,
                'url': url,
            }}, [f, 'to', url], []),
            # HTTP details
            ({'type': 'pull_http', 'ok': True, 'data': {'status': 200}}, ['\u2714', '200', 'PULL'], ['_HTTP']),
            ({'type': 'run', 'ok': False, 'data': {'exit_code': 200}}, ['\u2718', '200', 'RUN'], ['_HTTP']),
            # S3 details
            ({'type': 'pull_s3', 'data': {
                'bucket': 'b',
                'object_name': 'a',
                'filename': 'c',
            }}, ['PULL', 'a from S3 bucket b as c'], ['_S3']),
            ({'type': 'push_s3', 'data': {
                'bucket': 'b',
                'object_name': 'a',
                'filename': 'a',
            }}, ['PUSH', 'a to S3 bucket b'], ['as a', '_S3']),
        ]

        for data, p_results, n_results in testdata:
            log_to_console(data)
            output = print_mock.call_args[-2][0]

            for result in p_results:
                self.assertIn(result, output)
            for result in n_results:
                self.assertNotIn(result, output)


    @patch('builtins.print')
    def test_log_to_console_prints_run_output(self, print_mock):
        data = {'type': 'run', 'data': {'output': 'banana'}}
        result = 'banana'

        log_to_console(data)
        output = print_mock.call_args[-2][0]

        self.assertIn(result, output)
