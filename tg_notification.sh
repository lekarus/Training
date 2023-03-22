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
<code>Action</code>:  <a href='$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/${GITHUB_REF#*/}'>$GITHUB_EVENT_NAME</a>
<code>Repository</code>:  <a href='$GITHUB_SERVER_URL/$GITHUB_REPOSITORY'>${$GITHUB_REPOSITORY#*/}</a>
<code>Actor</code>:  <a href='$GITHUB_SERVER_URL/$GITHUB_ACTOR'>$GITHUB_ACTOR</a>
<code>Branch</code>:  <a href='$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/tree/$GITHUB_HEAD_REF'>$GITHUB_HEAD_REF</a>
<a href='$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID'>Workflow URL</a>
"

URL="https://api.telegram.org/bot$TG_BOT_TOKEN/sendMessage"

curl -s --max-time $TIME -d "chat_id=$TG_CHAT_ID&disable_web_page_preview=1&text=$TEXT&parse_mode=HTML" "$URL"
