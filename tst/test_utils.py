from unittest import TestCase
from time import time

from pullnrun._utils import timestamp, as_list, create_meta, filter_dict, void_fn

class UtilsTest(TestCase):
    def test_as_list_ensures_variable_is_list(self):
        for i in [0, [0], ]:
            a = as_list(i)
            self.assertIsInstance(a, list)
            self.assertEqual(len(a), 1)
            self.assertEqual(a[0], 0)

    def test_as_list_returns_empty_list_for_None_input(self):
        a = as_list(None)

        self.assertIsInstance(a, list)
        self.assertEqual(len(a), 0)

    def test_timestamp_return_timestamp_as_milliseconds(self):
        a = int(time() * 1000)
        b = timestamp()

        self.assertLessEqual(a, b)
        self.assertAlmostEqual(a, b, delta=250)

    def test_create_meta_raises_value_error_with_invalid_kwargs(self):
        with self.assertRaises(ValueError):
            create_meta(1, 2, function=print)

    def test_create_meta_adds_timestamps_to_meta(self):
        a = create_meta(1, 2)

        self.assertEqual(a['start'], 1)
        self.assertEqual(a['end'], 2)

    def test_filter_dict_filters_dict_by_keys(self):
        a = {1:2, 3:4, 5:6}
        b = filter_dict(a, (1,5))

        self.assertEqual(len(b), 2)
        self.assertIsNone(b.get(3))

        c = filter_dict(a, [])
        self.assertEqual(len(c), 0)

    def test_void_fn_returns_none(self):
        self.assertIsNone(void_fn())
        self.assertIsNone(void_fn(1, 2, 3))
        self.assertIsNone(void_fn(asd=123))
        self.assertIsNone(void_fn(1, 2, 3, asd=123))