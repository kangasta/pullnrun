from unittest import TestCase
from unittest.mock import patch, Mock

from subprocess import CompletedProcess

from jsonschema.exceptions import ValidationError

from pullnrun import main

class MainTest(TestCase):
    def test_main_validates_input_json(self):
        with self.assertRaises(ValidationError):
            main({'run': 'invalid'})

    @patch('builtins.print')
    @patch('subprocess.run')
    def test_main_executes_valid_input(self, run_mock, print_mock):
        run = {'command': ['main']}
        for i in [0, 1]:
            run_mock.return_value=CompletedProcess(['main'], i)

            success, error = main({'run': run}, quiet=True)
            self.assertEqual(success, (i + 1) % 2)
            self.assertEqual(error, i)

            run_mock.assert_called()
            print_mock.assert_not_called()
