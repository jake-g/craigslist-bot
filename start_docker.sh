#! /bin/bash

docker run --name craigslist-bot -d -e SLACK_TOKEN=xoxp-139047967344-139832954196-153246389329-865763cff4c1680419bcfd1a9005dac1 craigslist
docker exec -it craigslist-bot /bin/bash
