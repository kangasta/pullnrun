from unittest import TestCase
from unittest.mock import patch, MagicMock

from pullnrun._utils import void_fn
from pullnrun._pull import pull

PULL_S3 = {
    'from': 's3',
    'bucket': '__invalid',
    'object_name': 'object',
}

class PullTest(TestCase):
    @patch('boto3.client', side_effect=NameError)
    def test_pull_s3_handles_missing_boto3(self, mock):
        log_fn = MagicMock()
        self.assertFalse(pull(log_fn, **PULL_S3))
        self.assertIn('boto3 library not found', log_fn.call_args[-2][0].get('errors')[0]) # pylint: disable=unsubscriptable-object

    @patch('boto3.client')
    def test_pull_s3_calls_download_file(self, mock):
        s3_mock = MagicMock()
        mock.return_value = s3_mock

        r = pull(void_fn, **PULL_S3)

        s3_mock.download_file.assert_called_with('__invalid', 'object', 'object')
        self.assertTrue(r)

    @patch('boto3.client')
    def test_pull_s3_handles_failing_download(self, mock):
        s3_mock = MagicMock()
        s3_mock.download_file.side_effect = Exception
        mock.return_value = s3_mock

        r = pull(void_fn, **PULL_S3)

        s3_mock.download_file.assert_called()
        self.assertFalse(r)
