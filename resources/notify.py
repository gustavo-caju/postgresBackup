from logging import getLogger, CRITICAL
from .log import logRecord
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Disable for now
class notify():
    def __init__(self, confNotify):
        getLogger('slack_sdk').setLevel(CRITICAL) # do not log messages
        if confNotify: # checks if notifier has been set
            self.confNotify = confNotify
            if self.confNotify.get('type') == 'slack':
                self.messenger = 'slack'
                self.ts = None
            elif self.confNotify.get('type') == 'telegram':
                self.messenger = 'telegram'
            else:
                self.messenger = None
        else:
            self.messenger = None

    def notify(self, message, messageType=None ):
        if not self.messenger:
            pass
        elif self.messenger == 'slack': self.notifySlack(self.confNotify, message, messageType)
        elif self.messenger == 'telegram': self.notifyTelegram(self.confNotify, message)


    def notifySlack(self, confNotify, message, messageType):
        slackMessageHeader = [{
            "color": "#f2c744",
            "blocks": [{
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Banco",
                    "emoji": True}}]}]
        try:
            slack = WebClient(token=confNotify.get('token'))
            response = slack.chat_postMessage(
                channel=confNotify.get('channel'),
                icon_emoji=':database:',
                username='Postgres Backup',
                thread_ts=self.ts,
                attachments=slackMessageHeader if messageType == 'header' else None,
                blocks=slackMessage if messageType == 'text' else None,
                text=f'{message}' if not messageType == 'header' else None
                )
            self.ts = response.get('ts')
        except (Exception, SlackApiError) as e:
            message = f'An error occurred when notify by slack - {e}'
            logRecord('error', message)

    def notifyTelegram(self, message):
        pass
