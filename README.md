# CloudWatch Log Publisher

This is a Lambda function for receiving CloudWatch logs and sending them in a message format to popular chat apps.

### TODO:
- Improve message structure for better visibility;
- Send messages to Google Chat;
- Send messages to Discord;

# Deploy

```
cp sample.env .env
npm install
sls deploy
```

# Slack configuration

It is necessary to create a Slack app and install it in your Slack workspace, this operation generates a token (`Bot User OAuth Token`) which needs to be filled in your `.env` as the `SLACK_BOT_TOKEN` variable.

See [Slack docs for creating a basic app](https://api.slack.com/authentication/basics), then, in the app details, go to **OAuth & Permissions** and add these bot scopes: `chat:write`, `chat:write.customize`.

After installing the app in the workspace, create or choose an existing Slack channel to receive the log messages, and install the app into the channel (`Channel details > Integrations > Apps > Add apps > Choose the app you created`). Then, in your `.env` file fill `SLACK_CHANNEL` with the channel name.
