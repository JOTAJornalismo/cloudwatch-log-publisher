import json
import base64
import gzip
from io import BytesIO

def receive_log(event, *_):
    cw_data = str(event['awslogs']['data'])
    cw_logs = gzip.GzipFile(fileobj=BytesIO(base64.b64decode(cw_data, validate=True))).read()
    log_events = json.loads(cw_logs)

    print(log_events)