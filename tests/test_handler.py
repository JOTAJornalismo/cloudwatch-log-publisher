import base64
import gzip
import json
import unittest
from unittest import mock

from cloudwatch_log_publisher import handler

read_log_file = lambda path: open(path).read().replace('\\n', '\n').strip()

SAMPLE_LOG1 = read_log_file('tests/test-files/sample1.log')
SAMPLE_LOG2 = read_log_file('tests/test-files/sample2.log')
LOG_GROUP_NAME = 'sample-log-group'


@mock.patch('slack_sdk.WebClient.files_upload')
@mock.patch('slack_sdk.WebClient.chat_postMessage')
class HandlerTests(unittest.TestCase):

    def setUp(self) -> None:
        handler.SLACK_CHANNEL = 'testing'

    def test_receive_short_log(self, mock_post_message, mock_files_upload):
        handler.handle_log(self._generate_aws_log(SAMPLE_LOG1))

        mock_post_message.assert_called_with(
            channel=handler.SLACK_CHANNEL,
            text=f'{LOG_GROUP_NAME} ```{SAMPLE_LOG1}```'
        )
        mock_files_upload.assert_not_called()

    def test_receive_long_log(self, mock_post_message, mock_files_upload):
        handler.handle_log(self._generate_aws_log(SAMPLE_LOG2))

        mock_post_message.assert_called_with(
            channel=handler.SLACK_CHANNEL,
            text=f'{LOG_GROUP_NAME} ```{SAMPLE_LOG2[:handler.MAX_MESSAGE_LENGTH]}...```'
        )
        mock_files_upload.assert_called_once()

    def _generate_aws_log(self, data):
        log = {
            'logGroup': LOG_GROUP_NAME,
            'logEvents': [{
                'message': data
            }]
        }

        return {
            'awslogs': {
                'data': base64.b64encode(gzip.compress(json.dumps(log).encode())).decode('utf-8')
            }
        }
