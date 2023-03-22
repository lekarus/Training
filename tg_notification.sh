#!/bin/bash

TIME="10"

if [[ "$1" == "success" ]]
then
  TEXT="Deploy status: ✅%0A%0A"
elif [[ "$1" == "failed" ]]
then
  TEXT="Deploy status: ❌%0A%0A"
fi

TEXT="${TEXT}Deployment context:
Action: $GITHUB_EVENT_NAME
Repository: $GITHUB_REPOSITORY
Actor: $GITHUB_ACTOR
Branch: $GITHUB_HEAD_REF
<a href='$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_REPOSITORY'>URL</a>
"

URL="https://api.telegram.org/bot$TG_BOT_TOKEN/sendMessage"

curl -s --max-time $TIME -d "chat_id=$TG_CHAT_ID&disable_web_page_preview=1&text=$TEXT&parse_mode=HTML" "$URL"
