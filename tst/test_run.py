from unittest import TestCase
from unittest.mock import patch, ANY

from subprocess import CompletedProcess

from _log_mock import LogMock
from pullnrun._utils import void_fn
from pullnrun._run import run

class RunTest(TestCase):
    @patch('subprocess.run', return_value=CompletedProcess(['cmd'], 0))
    def test_run_calls_subprocess_run(self, mock_run):
        log = LogMock()
        self.assertTrue(run(log, ['cmd']))

        mock_run.assert_called_with(['cmd'], cwd=None, stdout=ANY, stderr=ANY, text=True)
        self.assertEqual(log.last['status'], 'SUCCESS')

        data = log.last['data']
        self.assertEqual(data['command'], ['cmd'])
        self.assertEqual(data['exit_code'], 0)

    @patch('subprocess.run', return_value=CompletedProcess(['cmd'], 1))
    def test_run_checks_non_zero_exit_code(self, mock_run):
        log = LogMock()
        self.assertFalse(run(log, ['cmd']))

        self.assertEqual(log.last['status'], 'FAIL')

    @patch('subprocess.run', side_effect=KeyboardInterrupt)
    def test_run_handles_failing_subprocess_run(self, mock_run):
        log = LogMock()
        self.assertFalse(run(log, ['cmd']))

        self.assertEqual(log.last['status'], 'ERROR')

        data = log.last['data']
        self.assertEqual(data['command'], ['cmd'])
        self.assertEqual(data['exit_code'], None)