from unittest import TestCase
from unittest.mock import patch

from pullnrun._log import Log, log_to_console, _duration

class LogTest(TestCase):
    def test_duration_is_logged_correctly(self):
        testdata = [
            ({'meta': {'start': 0, 'end': 1, }}, ''),
            ({'meta': {'start': 1, }}, ''),
            ({'meta': {'start': 0, }}, ''),
            ({'meta': {'start': 3, 'end': 53, }}, '50 ms'),
            ({'meta': {'start': 3, 'end': 5003, }}, '5.000 s'),
        ]

        for data, output in testdata:
            duration = _duration(data)
            self.assertEqual(duration, output)

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
            ({'type': 'pull_http', 'status': 'SUCCESS', 'data': {'status_code': 200}}, ['\u2714', '200', 'PULL'], ['_HTTP']),
            ({'type': 'pull_http', 'status': 'STARTED', 'data': {}}, ['\u25B6', 'PULL'], ['_HTTP']),
            ({'type': 'run', 'status': 'FAIL', 'data': {'exit_code': 200}}, ['\u2718', '200', 'RUN'], ['_HTTP']),
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
            # Main function start and end
            ({'type': 'main', 'status': 'STARTED'}, ['Started pullnrun execution with id'], ['\u25B6']),
            ({'type': 'main', 'status': 'SUCCESS', 'data': {'success': 3, 'fail': 5}}, ['Finished pullnrun execution in', '3 out of 8 actions succeeded.'], ['\u2714', '\u2718']),
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

    @patch('builtins.print')
    def test_log_class_prints_actions(self, print_mock):
        log = Log()
        testdata = [
            (log, ({'type': 'run', 'status': 'STARTED'}, ), '\u25B6'),
            (log.start, [], 'Started pullnrun execution'),
            (log.end, (1,2,), 'Finished pullnrun execution'),
        ]

        for fn, args, result in testdata:
            fn(*args)
            output = print_mock.call_args[-2][0]

            self.assertIn(result, output)
