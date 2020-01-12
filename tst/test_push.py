from unittest import TestCase
from unittest.mock import patch, MagicMock

from pullnrun._utils import void_fn
from pullnrun._push import push

PUSH_S3 = {
    'to': 's3',
    'bucket': '__invalid',
    'filename': 'object',
    'prefix': False,
}

class PushTest(TestCase):
    @patch('boto3.client', side_effect=NameError)
    def test_push_s3_handles_missing_boto3(self, mock):
        log_fn = MagicMock()
        self.assertFalse(push(log_fn, **PUSH_S3))
        self.assertIn('boto3 library not found', log_fn.call_args[-2][0].get('errors')[0]) # pylint: disable=unsubscriptable-object

    @patch('boto3.client')
    def test_push_s3_calls_upload_file(self, mock):
        s3_mock = MagicMock()
        mock.return_value = s3_mock

        r = push(void_fn, **PUSH_S3)

        s3_mock.upload_file.assert_called_with('object', '__invalid', 'object')
        self.assertTrue(r)

    @patch('boto3.client')
    def test_push_s3_handles_failing_upload(self, mock):
        s3_mock = MagicMock()
        s3_mock.upload_file.side_effect = Exception
        mock.return_value = s3_mock

        r = push(void_fn, **PUSH_S3)

        s3_mock.upload_file.assert_called()
        self.assertFalse(r)

    @patch('boto3.client')
    def test_prefixes_name_with_id_by_default(self, mock):
        s3_mock = MagicMock()
        mock.return_value = s3_mock

        push_s3 = {**PUSH_S3}
        del push_s3['prefix']
        r = push(void_fn, id='ID', **push_s3)

        s3_mock.upload_file.assert_called_with('object', '__invalid', 'ID-object')
        self.assertTrue(r)