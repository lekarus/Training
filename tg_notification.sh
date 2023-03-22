#!/bin/bash

TIME="10"
URL="https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage"

if [ $1 == 'success' ]
then
  TEXT = "Deploy status: ✅%0A%0"
elif [ $1 == 'failed' ]
then
  TEXT = "Deploy status: ❌%0A%0
  Deploy failed in:%0A"
fi

TEXT = TEXT + "Action: $GITHUB_EVENT_NAME%0A
Repository: $GITHUB_REPOSITORY%0A
Actor: $GITHUB_ACTOR%0A
Branch: $GITHUB_HEAD_REF%0A
URL: $GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_REPOSITORY%0A
"

URL = "https://api.telegram.org/bot$TG_BOT_TOKEN/sendMessage"

apt update -y
apt upgrade curl -y
apt install curl -y

curl -s --max-time $TIME -d "chat_id=$TG_CHAT_ID&disable_web_page_preview=1&text=$TEXT" $URL
