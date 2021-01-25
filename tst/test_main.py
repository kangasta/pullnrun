import os
from sys import stdout
from tempfile import TemporaryDirectory

from unittest import TestCase
from unittest.mock import Mock, patch

from _push_target import request_mock_implementation

from pullnrun.main import entrypoint, NO_PLAN, INVALID_PLAN
from pullnrun import __version__

TST_DIR = os.path.dirname(os.path.realpath(__file__))

class TestExit(Exception):
    def __init__(self, exit_code):
        super().__init__()
        self.exit_code = exit_code

def exit_mock_implementation(exit_code):
    raise TestExit(exit_code)

class MainTest(TestCase):
    @patch('builtins.exit')
    @patch('builtins.print')
    def test_main_version(self, print_mock, exit_mock):
        with patch('sys.argv', ['pullnrun', '--version']):
            entrypoint()

        print_mock.assert_called_with(f'pullnrun {__version__}')

    @patch('builtins.exit', side_effect=exit_mock_implementation)
    @patch('builtins.print')
    def test_main_exit_codes(self, print_mock, exit_mock):
        for args, exit_code in [
            ([], NO_PLAN),
            ([f'{TST_DIR}/invalid_plan.yml'], INVALID_PLAN),
        ]:
            with self.assertRaises(TestExit):
                with patch('sys.argv', ['pullnrun', *args]):
                    entrypoint()

            exit_mock.assert_called_with(exit_code)

    @patch('builtins.exit')
    @patch('builtins.print')
    def test_main_errors(self, print_mock, exit_mock):
        with patch('sys.argv', ['pullnrun', f'{TST_DIR}/../examples/errors.yml']):
            entrypoint()

        print_mock.assert_any_call(f'pullnrun {__version__}', file=stdout)
        exit_mock.assert_called_with(2)

    @patch('builtins.exit')
    @patch('builtins.print')
    def test_main_pull_http(self, print_mock, exit_mock):
        with TemporaryDirectory() as tmp_dir_path:
            os.chdir(tmp_dir_path)
            with patch('sys.argv', ['pullnrun', f'{TST_DIR}/../examples/fizzbuzz.json']):
                entrypoint()

            exit_mock.assert_called_with(0)

    @patch('builtins.exit')
    @patch('builtins.print')
    def test_main_pull_git(self, print_mock, exit_mock):
        with TemporaryDirectory() as tmp_dir_path:
            os.chdir(tmp_dir_path)
            with patch('sys.argv', ['pullnrun', f'{TST_DIR}/../examples/fizzbuzz_git.json']):
                entrypoint()

            exit_mock.assert_called_with(0)

    @patch('builtins.exit')
    @patch('builtins.print')
    @patch('pullnrun.push.request')
    def test_main_push_http(self, request_mock, print_mock, exit_mock):
        request_mock.side_effect = request_mock_implementation
        with TemporaryDirectory() as tmp_dir_path:
            os.chdir(tmp_dir_path)
            with open('test_file.txt', 'w') as f:
                f.write('test_content')

            with patch('sys.argv', ['pullnrun', f'{TST_DIR}/../examples/push.yml']):
                entrypoint()

        exit_mock.assert_called_with(1)
