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
-------------

In general there is house scrape and for sale scrape, here are filters related

Notes on filters
```
# generic filters 
    base_filters = {
        'query': {'url_key': 'query', 'value': None},
        'search_titles': {'url_key': 'srchType', 'value': 'T'},
        'has_image': {'url_key': 'hasPic', 'value': 1},
        'posted_today': {'url_key': 'postedToday', 'value': 1},
        'bundle_duplicates': {'url_key': 'bundleDuplicates', 'value': 1},
        'search_distance': {'url_key': 'search_distance', 'value': None},
        'zip_code': {'url_key': 'postal', 'value': None},
    }

# filters for sales:
    extra_filters = {
        'min_price': {'url_key': 'min_price', 'value': None},
        'max_price': {'url_key': 'max_price', 'value': None},
        'make': {'url_key': 'auto_make_model', 'value': None},
        'model': {'url_key': 'auto_make_model', 'value': None},
        'min_year': {'url_key': 'min_auto_year', 'value': None},
        'max_year': {'url_key': 'max_auto_year', 'value': None},
        'min_miles': {'url_key': 'min_auto_miles', 'value': None},
        'max_miles': {'url_key': 'max_auto_miles', 'value': None},
    }

# filters for houses:
    extra_filters = {
        'private_room': {'url_key': 'private_room', 'value': 1},
        'private_bath': {'url_key': 'private_bath', 'value': 1},
        'cats_ok': {'url_key': 'pets_cat', 'value': 1},
        'dogs_ok': {'url_key': 'pets_dog', 'value': 1},
        'min_price': {'url_key': 'min_price', 'value': None},
        'max_price': {'url_key': 'max_price', 'value': None},
        'min_ft2': {'url_key': 'minSqft', 'value': None},
        'max_ft2': {'url_key': 'maxSqft', 'value': None},
        'min_bedrooms': {'url_key': 'min_bedrooms', 'value': None},
        'max_bedrooms': {'url_key': 'max_bedrooms', 'value': None},
        'min_bathrooms': {'url_key': 'min_bathrooms', 'value': None},
        'max_bathrooms': {'url_key': 'max_bathrooms', 'value': None},
        'no_smoking': {'url_key': 'no_smoking', 'value': 1},
        'is_furnished': {'url_key': 'is_furnished', 'value': 1},
        'wheelchair_acccess': {'url_key': 'wheelchaccess', 'value': 1},
    }
```

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
    * `docker run -d -e SLACK_TOKEN={YOUR_SLACK_TOKEN} -v {ABSOLUTE_PATH_TO_YOUR_CONFIG_FOLDER}:/opt/wwc/craigslist-bot/config craigslist`


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
* Inspect the logs using `tail -f -n 1000 /opt/wwc/logs/craigslist-bot.log`. (dockerfile has alias for this: `log`)


On Server (no docker)
--------------------
1. Install pre-reqs
```
apt-get update && apt-get -y install python3 python3-pip make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev zip git-core supervisor sqlite
```
2. Make folders `mkdir -p /opt/wwc && mkdir -p /opt/wwc/logs`
3. Clone repo in `/opt/wwc` make sure the repo folder is called `craigslist-bot`, or whatever the path in `supervisord.conf` is
4. merge `deployment/supervisord.conf` with `/etc/supervisor/supervisord.conf`, note `nodaemon=true` will not let you do other stuff on server (kinda)
5. Install python packages: `pip3 install -r requirements.txt`
6. Add alias to view log `alias cl-log="tail -f -n 1000 /opt/wwc/logs/craigslist-bot.log"`
7. Reboot and make sure it is running at boot (use alias to check log)
