#! /bin/bash
docker build -t craigslist . 
docker run --name craig-bot-music --restart always -d -e SLACK_TOKENxoxp-139047967344-139832954196-470545154000-4a98d4b072a75ddbb07dee118689ba90 craigslist
docker exec -it craig-bot /bin/bash
