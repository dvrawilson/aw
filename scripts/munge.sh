#!/bin/sh

USERNAME="antiochuswilson"
USERID="1395786698961952772"

jq '[.[] |
    select(
        (.tweet.in_reply_to_screen_name == null or .tweet.in_reply_to_screen_name == "'$USERNAME'") and
        (.tweet.entities.user_mentions | length == 0) and
        (.tweet.retweeted_status == null) and
        (.tweet.in_reply_to_user_id == null or .tweet.in_reply_to_user_id == "'$USERID'") and
        (.tweet.entities.media == null) and
        (.tweet.full_text[0:1] != "@")
    ) |
    {
        content: .tweet.full_text,
        timestamp: .tweet.created_at,
        id: .tweet.id,
        urls: (.tweet.entities.urls // [] | map({
            url: .url,
            expanded: .expanded_url
        }))
    }
]' ../assets/tweets.json > ../assets/slimtweets.json

jq '[foreach .[] as $item (.;
  if $item.urls | length > 0 then
    foreach $item.urls[] as $url ( $item.content;
      sub($url.url; $url.expanded) )
  else
    $item.content
  end | {
            content: ., 
            timestamp: $item.timestamp, 
            id: $item.id,
        }  
)]' ../assets/slimtweets.json > ../assets/cleanedtweets.json
