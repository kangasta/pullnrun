from unittest import TestCase
from unittest.mock import patch

from pullnrun._log import log_to_console

class LogTest(TestCase):
    @patch('builtins.print')
    def test_log_to_console_does_not_crash_on_empty_input(self, print_mock):
        log_to_console({})
        print_mock.assert_called()

    @patch('builtins.print')
    def test_log_to_console_prints_type_and_status(self, print_mock):
        testdata = [
            ({'type': 'pull', 'ok': True, 'data': {'status': 200}}, ['\u2714', '200', 'PULL']),
            ({'type': 'run', 'ok': False, 'data': {'exit_code': 200}}, ['\u2718', '200', 'RUN']),
        ]

        for data, results in testdata:
            log_to_console(data)
            output = print_mock.call_args.args[0]

            for result in results:
                self.assertIn(result, output)

    @patch('builtins.print')
    def test_log_to_console_prints_run_output(self, print_mock):
        data = {'type': 'run', 'data': {'output': 'banana'}}
        result = 'banana'

        log_to_console(data)
        output = print_mock.call_args.args[0]

        self.assertIn(result, output)