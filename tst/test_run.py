from unittest import TestCase
from unittest.mock import patch, ANY

from subprocess import CompletedProcess

from pullnrun._run import run

class RunTest(TestCase):
    @patch('subprocess.run', return_value=CompletedProcess(['cmd'], 0))
    def test_run_calls_subprocess_run(self, mock_run):
        a = run(['cmd'])

        mock_run.assert_called_with(['cmd'], cwd=None, stdout=ANY, stderr=ANY, text=True)
        self.assertEqual(a['ok'], True)

        data = a['data']
        self.assertEqual(data['command'], ['cmd'])
        self.assertEqual(data['exit_code'], 0)
    
    @patch('subprocess.run', side_effect=KeyboardInterrupt)
    def test_run_handles_failing_subprocess_run(self, mock_run):
        a = run(['cmd'])

        self.assertEqual(a['ok'], False)

        data = a['data']
        self.assertEqual(data['command'], None)
        self.assertEqual(data['exit_code'], None)