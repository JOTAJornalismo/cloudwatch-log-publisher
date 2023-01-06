import json
import unittest
from unittest import mock

from cloudwatch_log_publisher import handler

SAMPLE_EVENT = json.loads(open('tests/test-files/sample-event.json').read())


class HandlerTests(unittest.TestCase):

    @mock.patch('slack_sdk.WebClient.chat_postMessage')
    def test_receive_log(self, mock_post_message):
        handler.SLACK_CHANNEL = 'testing'

        handler.handle_log(SAMPLE_EVENT)

        mock_post_message.assert_called_with(
            channel=handler.SLACK_CHANNEL,
            text='ta-alert-dev-b3-history ```START RequestId: 10f72fb6-ca96-4c3a-b82e-32ffd5a47050 Version: $LATEST\nDownloading started```'
        )
