import math
import os
import settings

import pickle

def save_dict_to_file(dictionary, file_path):
    """
    Saves the given dictionary to a file in pickle format.
    """
    with open(file_path, 'wb') as file:
        pickle.dump(dictionary, file, protocol=pickle.HIGHEST_PROTOCOL)

def load_dict_from_file(file_path):
    """
    Loads a dictionary from a pickle file.
    """
    with open(file_path, 'rb') as file:
        return pickle.load(file)
    


def coord_distance(lat1, lon1, lat2, lon2):
    # Distance between two pairs of latitude and longitude.
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def in_box(coords, box):
    # True if coordinate (tuple: lat, long) is inside a bounding box 
    # (box[0]: bottom left, box[1]: top right)
    if box[0][0] <= coords[0] <= box[1][0] and box[0][1] <= coords[1] <= box[1][1]:
        return True
    return False


def post_listing_to_slack(sc, listing, reply_description=True):
    # Post listing to slack client (sc)
    post_str = "{0} | {1} | {2} | <{3}>".format(listing["area"], listing["price"], listing["name"], listing["url"])
    post_response = sc.chat_postMessage(
        channel=settings.SLACK_CHANNEL, text=post_str,
        username=settings.BOT_NAME, icon_emoji=settings.BOT_EMOJI,
        unfurl_links=True, unfurl_media=True
    )

    # Reply to a thread with description
    post_ts = post_response.data.get('ts', None)
    if reply_description and post_ts:
        reply_response = sc.chat_postMessage(
            channel=settings.SLACK_CHANNEL,
            text='```{0}```'.format(listing["description"]),
            username='description-bot', icon_emoji=':spiral_note_pad:',
            thread_ts=post_ts, unfurl_links=True, unfurl_media=True
        )


def find_points_of_interest(geotag, location, url):
    # Returns dict with points of interest, like transit, near a result
    area = os.path.basename(os.path.dirname(url)).split('-')[0]
    # Look to see if the listing is in any of the neighborhood boxes we defined.
    for a, coords in settings.BOXES.items():
        if in_box(geotag, coords):
            area = a

    # If the listing isn't in any of the boxes we defined, check to see if the string description of the neighborhood
    # matches anything in our list of neighborhoods.
    for hood in settings.NEIGHBORHOODS:
        if hood.lower() in location.lower():
            area = hood

    return area
