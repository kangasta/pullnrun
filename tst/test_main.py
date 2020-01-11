from unittest import TestCase
from unittest.mock import patch, Mock

from jsonschema.exceptions import ValidationError

from pullnrun._main import main

class MainTest(TestCase):
    def test_main_validates_input_json(self):
        with self.assertRaises(ValidationError):
            main({'run': 'invalid'})
