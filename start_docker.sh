#! /bin/bash
echo 'probably need a new token: https://api.slack.com/custom-integrations/legacy-tokens'
docker build -t craigslist . 
docker run --name craig-bot-music --restart always -d -e SLACK_TOKEN=xoxp-139047967344-139832954196-470683201665-7f1af731ddbcd0a6390e86f352aae108 craigslist
docker exec -it craig-bot /bin/bash
