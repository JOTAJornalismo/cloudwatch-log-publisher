import base64
import gzip
import json
import os
from io import BytesIO

from slack_sdk import WebClient

SLACK_BOT_TOKEN=os.getenv('SLACK_BOT_TOKEN')
SLACK_CHANNEL=os.getenv('SLACK_CHANNEL')
MAX_MESSAGE_LENGTH=int(os.getenv('MAX_MESSAGE_LENGTH'))


def handle_log(event, *_):
    encoded_data = str(event['awslogs']['data'])
    json_logs = gzip.decompress(base64.b64decode(encoded_data, validate=True))
    log_data = json.loads(json_logs)

    client = WebClient(token=SLACK_BOT_TOKEN)

    message = '\n'.join([log['message'].strip() for log in log_data['logEvents']])

    if len(message) > MAX_MESSAGE_LENGTH:
        message = f'{message[:MAX_MESSAGE_LENGTH]}...'

    client.chat_postMessage(channel=SLACK_CHANNEL,
                            text=f"{log_data['logGroup'].split('/')[-1]} ```{message}```")
