import os

## System settings

# How long we should sleep between scrapes of Craigslist. Too fast may get rate limited, too slow may miss listings.
SLEEP_INTERVAL = 20 * 60  # 20 minutes

# Which slack channel to post the listings into.
SLACK_CHANNEL = "#bike-bot"
BOT_NAME = 'bike-bot'
BOT_EMOJI = ':bike:'

## Location and Search preferences

# Search filters (see craigslist.CraigslistHousing filters attribute)
FILTERS = [
    # {'min_bedrooms': 2, 'max_bedrooms': 3, 'min_price': 1800, 'max_price': 3300},
    {'query': '"road" (58 | 59 | 60 | 61 | 22 | 23)', 'min_price': 100, 'max_price': 800},
]
#

# The Craigslist site you want to search on.
# Ex: https://sfbay.craigslist.org is SF and the Bay Area.
SITE = 'seattle'

# What Craigslist subdirectories to search on (three letters.
# Ex: https://sfbay.craigslist.org/eby/ is the East Bay, and https://sfbay.craigslist.org/sfc/ is San Francisco.
AREAS = ["see"]

# The Craigslist section underneath housing that you want to search in (3 letters.
# Ex https://sfbay.craigslist.org/search/apa for apartment or /bia for bike ect
CATEGORY = 'bia'
HOUSE_SEARCH = False

# A list of neighborhoods and coordinates that you want to look for apartments in.  Any listing that has coordinates
# attached will be checked to see which area it is in.  If there's a match, it will be annotated with the area name.
#  Ex: "neighborhood": [[bottom left lat, long],[top right lat, long]],
BOXES = {
    "university_district": [
        [47.652653, -122.321177],
        [47.668007, -122.290192],
    ],
    "northgate": [
        [47.686806, -122.325211],
        [47.707141, -122.304268],
    ],
    "ravenna": [
        [47.668585, -122.320404],
        [47.682686, -122.290707],
    ],
    "wallingford": [
        [47.645459, -122.345982],
        [47.664423, -122.323666],
    ],
    "green_lake": [
        [47.665001, -122.353363],
        [47.693548, -122.318344],
    ],
    "fremont": [
        [47.649623, -122.365894],
        [47.664076, -122.347870],
    ],
    "montlake": [
        [47.631464, -122.311649],
        [47.646732, -122.279549],
    ],
    "eastlake": [
        [47.632505, -122.327957],
        [47.651589, -122.317142],
    ],
    "laurelhurst": [
        [47.649700, -122.289419],
        [47.667275, -122.254829],
    ],
    "north_east": [
        [47.667564, -122.285128],
        [47.692297, -122.242899],
    ],
    "downtown": [
        [47.593360, -122.355113],
        [47.617480, -122.322546]
    ],
    "capital hill": [
        [47.606733, -122.327824],
        [47.640772, -122.301673]
    ],
    "madison valley": [
        [47.608362, -122.302016],
        [47.642400, -122.275864]
    ],
    "queen anne": [
        [47.618131, -122.417047],
        [47.647061, -122.341809]
    ],
    "central district": [
        [47.591094, -122.317495],
        [47.609313, -122.281628]
    ],
    "south seattle": [
        [47.536931, -122.337557],
        [47.593198, -122.256414]
    ],
    "west seattle": [
        [47.487232, -122.424211],
        [47.600286, -122.348608]
    ],
    "north seattle": [
        [47.755829, -122.439143],
        [47.900693, -122.091753]
    ],
    "bellevue": [
        [47.594642, -122.250895],
        [47.683973, -122.089714]
    ],
    "bothell": [
        [47.696081, -122.262352],
        [47.785239, -122.137077]
    ],
    "mercer island": [
        [47.525787, -122.246902],
        [47.593974, -122.215127]
    ]
}

# A list of neighborhood names to look for in the Craigslist neighborhood name field. If a listing doesn't fall into
# one of the boxes you defined, it will be checked to see if the neighborhood name it was listed under matches one
# of these.  This is less accurate than the boxes, because it relies on the owner to set the right neighborhood,
# but it also catches listings that don't have coordinates (many listings are missing this info).
NEIGHBORHOODS = ["wallingford", "eastlake", "fremont", "green lake", "roosevelt", "university district", "udist",
                 "montlake", "hawthorne hills", "greenlake", "greenwood", "laurelhurst", "uw", "ravenna",
                 "northgate", "ballard", "capital hill", "queen anne", "bell town", "phinny", "shoreline",
                 "madison", "lake forest"]

## Transit preferences
# The farthest you want to live from a transit stop.
MAX_TRANSIT_DIST = None  # 2  # kilometers
# Transit stations you want to check against.  Every coordinate here will be checked against each listing,
# and the closest station name will be added to the result and posted into Slack.
TRANSIT_STATIONS = {}
# TRANSIT_STATIONS = {
#     "oakland_19th_bart": [37.8118051,-122.2720873],
#     "macarthur_bart": [37.8265657,-122.2686705],
#     "rockridge_bart": [37.841286,-122.2566329],
#     "downtown_berkeley_bart": [37.8629541,-122.276594],
#     "north_berkeley_bart": [37.8713411,-122.2849758]
# }


# The token that allows us to connect to slack. Should be put in private.py, or set as an environment variable.
SLACK_TOKEN = os.getenv('SLACK_TOKEN', "")
# Any private settings are imported here.
try:
    from private import *
except Exception:
    pass

# Any external private settings are imported from here.
try:
    from config.private import *
except Exception:
    pass
