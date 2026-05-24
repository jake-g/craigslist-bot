# Craigslist Scraping Bot

**2017 - 2023**

> [!WARNING]
> **Archived Repository & Deprecated Status**
> This repository is archived and no longer actively maintained.
> The bot has been **broken since late 2023** due to:
> 1. Major breaking updates to Craigslist's static web layout and markup.
> 2. The deprecation and abandonment of the underlying `python-craigslist` library (related to GitHub issue #122).
> 
> *An incomplete, experimental attempt to fix the bot using a custom library patch can be found on the `dev-house-2023` branch, but was abandoned.*

## Overview
This bot periodically scrapes Craigslist listings (for housing or items for sale) matching specific price and size filters, checks if they fall inside defined geographic coordinate bounding boxes, filters out blacklisted terms, and posts new matches to a Slack channel. It uses a local SQLite database to track processed listings and prevent duplicate alerts.

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

## Configuration

* Create a file called `private.py` in the root of this folder.
  * Add a variable called `SLACK_TOKEN` containing your Slack API token:
    ```python
    SLACK_TOKEN = "your-slack-bot-token"
    ```
  * You can also override any of the settings from `settings.py` inside `private.py` (e.g. customized `BOXES`, `NEIGHBORHOODS`, etc.) to keep your secrets/private configurations out of version control.

---

## Installation & Running

### Option A: Systemd Linux Service (Recommended for servers/headless hosts)
This method runs the scraper continuously in the background as a system service. Designed for DietPi/Debian servers.

1. **Setup dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
2. **Deploy the systemd service**:
   Run the helper script:
   ```bash
   sudo ./make_service.sh
   ```
   This generates the service definition file, copies it to `/etc/systemd/system/craig-bot.service`, reloads systemd, and enables the service to start automatically on boot.
3. **Verify/Control the service**:
   * Check status:
     ```bash
     systemctl status craig-bot.service
     ```
   * Stream live logs:
     ```bash
     journalctl --unit=craig-bot -n 10 -f --no-pager
     ```
     *(Note: `make_service.sh` automatically appends a shell alias `criag-bot` to your `~/.bashrc` to stream logs easily).*

### Option B: Manual Execution
To run the bot directly:
```bash
python3 main_loop.py
```
This starts the scraper, which queries Craigslist according to `SLEEP_INTERVAL` (defaults to every 40 minutes) and posts new findings to Slack.

---

## Technical Details & Troubleshooting

### Scraped History Database (`listings.db`)
* The bot uses a local SQLite database file named `listings.db` to keep track of already scraped and processed listing IDs.
* If you delete this file, the bot will treat all matching listings as new on the next run and re-post duplicate alerts to Slack.
* To inspect or clean the database manually:
  ```bash
  sqlite3 listings.db
  # Query parsed listings
  sqlite> select * from listings;
  ```

---

## Appendix: Historical Deployments
For older deployment configurations using Docker or Supervisor, see the archived documentation at [old/deployment/README_OLD.md](file:///Users/jakegarrison/Downloads/projects/craigslist-bot/old/deployment/README_OLD.md).
