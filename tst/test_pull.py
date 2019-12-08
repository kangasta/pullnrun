from unittest import TestCase
from unittest.mock import patch, Mock

from pullnrun._pull import pull

PULL_S3 = {
    'from': 's3',
    'bucket': '__invalid',
    'object_name': 'object',
}

class PullTest(TestCase):
    @patch('boto3.client', side_effect=NameError)
    def test_pull_s3_handles_missing_boto3(self, mock):
        a = pull(**PULL_S3)
        self.assertFalse(a.get('ok'))

    @patch('boto3.client')
    def test_pull_s3_calls_download_file(self, mock):
        s3_mock = Mock()
        mock.return_value = s3_mock

        a = pull(**PULL_S3)

        s3_mock.download_file.assert_called_with('__invalid', 'object', 'object')
        self.assertTrue(a.get('ok'))


    @patch('boto3.client')
    def test_pull_s3_handles_failing_download(self, mock):
        s3_mock = Mock()
        s3_mock.download_file.side_effect = KeyboardInterrupt
        mock.return_value = s3_mock

        a = pull(**PULL_S3)

        s3_mock.download_file.assert_called()
        self.assertFalse(a.get('ok'))
