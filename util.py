import math

import settings


def coord_distance(lat1, lon1, lat2, lon2):
    # Distance between two pairs of latitude and longitude.
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def in_box(coords, box):
    # True if coordinate (tuple: lat, long) is inside a bounding box (2 tuples: first, bottom left. second, top right)
    if box[0][0] < coords[0] < box[1][0] and box[1][1] < coords[1] < box[0][1]:
        return True
    return False


def post_listing_to_slack(sc, listing):
    # Post listing to slack client (sc)
    desc = "{0} | {1} | {2} | <{3}>".format(listing["area"], listing["price"], listing["name"], listing["url"])
    sc.chat_postMessage(
        channel=settings.SLACK_CHANNEL, text=desc,
        username=settings.BOT_NAME, icon_emoji=settings.BOT_EMOJI
    )


def find_points_of_interest(geotag, location):
    # Returns dict with points of interest, like transit, near a result
    area_found = False
    area = ""
    min_dist = None
    near_transit = False
    transit_dist = "N/A"
    transit = ""
    # Look to see if the listing is in any of the neighborhood boxes we defined.
    for a, coords in settings.BOXES.items():
        if in_box(geotag, coords):
            area = a
            area_found = True

    # Check to see if the listing is near any transit stations.
    for station, coords in settings.TRANSIT_STATIONS.items():
        dist = coord_distance(coords[0], coords[1], geotag[0], geotag[1])
        if (min_dist is None or dist < min_dist) and dist < settings.MAX_TRANSIT_DIST:
            transit = station
            near_transit = True

        if (min_dist is None or dist < min_dist):
            transit_dist = dist

    # If the listing isn't in any of the boxes we defined, check to see if the string description of the neighborhood
    # matches anything in our list of neighborhoods.
    if len(area) == 0:
        for hood in settings.NEIGHBORHOODS:
            if hood in location.lower():
                area = hood

    return {
        "area_found": area_found,
        "area": area,
        "near_transit": near_transit,
        "transit_dist": transit_dist,
        "transit": transit
    }
