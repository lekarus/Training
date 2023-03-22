#!/bin/bash

TIME="10"

if [[ "$1" == "success" ]]
then
  TEXT="Deploy status ✅%0A%0A"
elif [[ "$1" == "failed" ]]
then
  TEXT="Deploy status ❌%0A%0A"
fi

if [[ "$GITHUB_EVENT_NAME" == "pull_request" ]]
then
  Action="<b>Action</b>:  <a href='$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/${GITHUB_REF#*/}'>$GITHUB_EVENT_NAME</a>"
  Branch=$GITHUB_HEAD_REF
else
  Branch=$GITHUB_REF_NAME
  Action="<b>Action</b>: <code>Push</code>"
fi

TEXT="${TEXT}Deployment context:
<b>Actor</b>:  <a href='$GITHUB_SERVER_URL/$GITHUB_ACTOR'>$GITHUB_ACTOR</a>
${Action}
<b>Branch</b>:  <a href='$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/tree/$Branch'>$Branch</a>
<b>Repository</b>:  <a href='$GITHUB_SERVER_URL/$GITHUB_REPOSITORY'>${GITHUB_REPOSITORY#*/}</a>
<a href='$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID'>Pipeline URL</a>
"

URL="https://api.telegram.org/bot$TG_BOT_TOKEN/sendMessage"

curl -s --max-time $TIME -d "chat_id=$TG_CHAT_ID&disable_web_page_preview=1&text=$TEXT&parse_mode=HTML" "$URL"
