import base64
import gzip
import json
import os
from hashlib import md5

from slack_sdk import WebClient

SLACK_BOT_TOKEN=os.getenv('SLACK_BOT_TOKEN')
SLACK_CHANNEL=os.getenv('SLACK_CHANNEL')
MAX_MESSAGE_LENGTH=int(os.getenv('MAX_MESSAGE_LENGTH', 500))


def handle_log(event, *_):
    encoded_data = str(event['awslogs']['data'])
    json_logs = gzip.decompress(base64.b64decode(encoded_data, validate=True))
    log_data = json.loads(json_logs)

    client = WebClient(token=SLACK_BOT_TOKEN)

    message = log_message = '\n'.join([log['message'].strip() for log in log_data['logEvents']])

    if long_message := len(log_message) > MAX_MESSAGE_LENGTH:
        message = f'{log_message[:MAX_MESSAGE_LENGTH]}...'

    response = client.chat_postMessage(channel=SLACK_CHANNEL,
                                       text=f"{log_data['logGroup'].split('/')[-1]} ```{message}```")

    if long_message:
        filename = f'/tmp/{md5(log_message.encode()).hexdigest()}.log'
        with open(filename, 'w') as log_file:
            log_file.write(log_message)

        client.files_upload(channels=SLACK_CHANNEL, file=filename, thread_ts=response['ts'])

