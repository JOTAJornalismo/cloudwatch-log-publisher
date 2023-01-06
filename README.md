# CloudWatch Log Publisher ![test status](https://github.com/lucasfacchini/cloudwatch-log-publisher/actions/workflows/test.yml/badge.svg)

This is a Lambda function for receiving CloudWatch logs and sending them in a message format to popular chat apps.

### TODO:
- Improve message structure for better visibility;
- Send messages to Google Chat;
- Send messages to Discord;

# Deploy

```bash
cp sample.env .env
npm install
sls deploy
```

# CloudWatch subscription filter

In order to receive logs add a `AWS::Logs::SubscriptionFilter` in the desired Log Group.

Example for receiving logs from a Lambda function in Serverless framework:
```yml
ErrorLogsSubscription:
    Type: AWS::Logs::SubscriptionFilter
    DependsOn:
        - <lambda-function-cf-logical-name>
    Properties:
    DestinationArn: arn:aws:lambda:${self:provider.region}:${aws:accountId}:cloudwatch-log-publisher-${self:provider.stage}-log-publisher
    FilterPattern: "${env:LOG_FILTER_PATTERN}"
    LogGroupName: '/aws/lambda/${self:service}-${self:provider.stage}-<your-function-name>'
```

Filter pattern suggestion (ignores default Lambda logs): `"-START -END -REPORT"`. Or leave an empty string for receiving all logs.

# Slack configuration

It is necessary to create a Slack app and install it in your Slack workspace, this operation generates a token (`Bot User OAuth Token`) which needs to be filled in your `.env` as the `SLACK_BOT_TOKEN` variable.

See [Slack docs for creating a basic app](https://api.slack.com/authentication/basics), then, in the app details, go to **OAuth & Permissions** and add these bot scopes: `chat:write`, `chat:write.customize`.

After installing the app in the workspace, create or choose an existing Slack channel to receive the log messages, and install the app into the channel (`Channel details > Integrations > Apps > Add apps > Choose the app you created`). Then, in your `.env` file fill `SLACK_CHANNEL` with the channel name.
