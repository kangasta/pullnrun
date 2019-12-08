from unittest import TestCase
from unittest.mock import patch, Mock

from pullnrun._push import push

PUSH_S3 = {
    'to': 's3',
    'bucket': '__invalid',
    'filename': 'object',
}

class PushTest(TestCase):
    @patch('boto3.client', side_effect=NameError)
    def test_push_s3_handles_missing_boto3(self, mock):
        a = push(**PUSH_S3)
        self.assertFalse(a.get('ok'))

    @patch('boto3.client')
    def test_push_s3_calls_upload_file(self, mock):
        s3_mock = Mock()
        mock.return_value = s3_mock

        a = push(**PUSH_S3)

        s3_mock.upload_file.assert_called_with('object', '__invalid', 'object')
        self.assertTrue(a.get('ok'))


    @patch('boto3.client')
    def test_push_s3_handles_failing_upload(self, mock):
        s3_mock = Mock()
        s3_mock.upload_file.side_effect = KeyboardInterrupt
        mock.return_value = s3_mock

        a = push(**PUSH_S3)

        s3_mock.upload_file.assert_called()
        self.assertFalse(a.get('ok'))
