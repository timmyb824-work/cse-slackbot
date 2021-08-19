## Summary

A simple slackbot for sending Opsgenie alert or page requests. To initiate an alert simply enter `/sendpage` in a Slack workspace where the bot has been added.

## Dependicies

```
brew install pyenv # python version manager
brew install pyenv-virtualenv # recommend using virtual environments
pyenv install 3.9.5 # installs python
pip install slack_bolt
pip install requests
```

## Authentication

Three environement variables must be set to authenticate the bot:

`SLACK_BOT_TOKEN` - Slack bot token
`SLACK_APP_TOKEN` - Slack app token
`OPSGENIE_INTEGRATION_KEY` - Opsgenie integration API key
