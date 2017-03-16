Settings
--------------------

Look in `settings.py` for a full list of all the configuration options.  Here's a high level overview:

* `MIN_PRICE` -- the minimum listing price you want to search for.
* `MAX_PRICE` -- the minimum listing price you want to search for.
* `CRAIGSLIST_SITE` -- the regional Craigslist site you want to search in.
* `AREAS` -- a list of areas of the regional Craiglist site that you want to search in.
* `BOXES` -- coordinate boxes of the neighborhoods you want to look in.
* `NEIGHBORHOODS` -- if the listing doesn't have coordinates, a list of neighborhoods to match on.
* `MAX_TRANSIT_DISTANCE` -- the farthest you want to be from a transit station.
* `TRANSIT_STATIONS` -- the coordinates of transit stations.
* `CRAIGSLIST_HOUSING_SECTION` -- the subsection of Craigslist housing that you want to look in.
* `SLACK_CHANNEL` -- the Slack channel you want the bot to post in.

External Setup
--------------------

Before using this bot, you'll need a Slack team, a channel for the bot to post into, and a Slack API key:

* Create a Slack team, which you can do [here](https://slack.com/create#email).  
* Create a channel for the listings to be posted into.  [Here's](https://get.slack.help/hc/en-us/articles/201402297-Creating-a-channel) help on this.  It's suggested to use `#housing` as the name of the channel.
* Get a Slack API token, which you can do [here](https://api.slack.com/docs/oauth-test-tokens).  [Here's](https://get.slack.help/hc/en-us/articles/215770388-Creating-and-regenerating-API-tokens) more information on the process.

Configuration
--------------------

## Docker

* Create a folder called `config`, then put a file called `private.py` inside.
* Specify new values for any of the settings above in `private.py`.

## Manual

* Create a file called `private.py` in this folder.
    * Add a value called `SLACK_TOKEN` that contains your Slack API token.
    * Add any other values you want to `private.py`.

Installation + Usage
--------------------

## Docker

* Make sure to do the steps in the configuration section above first.
* Install Docker by following [these instructions](https://docs.docker.com/engine/installation/).
* first build cd into this dir, run: `docker build -t craigslist . `
* you have to remove an old version image first `docker rmi craigslist`
* To run the program with the default configuration:
    * `docker run -d -e SLACK_TOKEN={YOUR_SLACK_TOKEN} craigslist`
* To run the program with your own configuration:
    * `docker run -d -e SLACK_TOKEN={YOUR_SLACK_TOKEN} -v {ABSOLUTE_PATH_TO_YOUR_CONFIG_FOLDER}:/opt/wwc/apartment-finder/config craigslist`


Troubleshooting
---------------------

## Docker
* see the `start_docker.sh` script
* Use `docker ps` to get the id of the container running the bot.
* Run `docker exec -it {YOUR_CONTAINER_ID} /bin/bash` to get a command shell inside the container.
* Run `sqlite listings.db` to run the sqlite command line tool and inspect the database state (the only table is also called `listings`).
    * `select * from listings` will get all of the stored listings.
    * If nothing is in the database, you may need to wait for a bit, or verify that your settings aren't too restrictive and aren't finding any listings.
    * You can see how many listings are being found by looking at the logs.
* Inspect the logs using `tail -f -n 1000 /opt/wwc/logs/afinder.log`. (dockerfile has alias for this: `log`)
