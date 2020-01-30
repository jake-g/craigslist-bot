import sys
import time
import traceback

import settings
from scraper import do_scrape

if __name__ == "__main__":
    # print("Waiting for %d seconds..." % settings.SLEEP_INTERVAL)
    # time.sleep(settings.SLEEP_INTERVAL)
    while True:
        # print("{}: Starting scrape cycle".format(time.ctime()))
        try:
            do_scrape()
        except KeyboardInterrupt:
            print("Exiting....")
            sys.exit(1)
        except Exception as exc:
            print("Error with the scraping:", sys.exc_info()[0])
            traceback.print_exc()
        else:
            pass
            # print("{}: Successfully finished scraping".format(time.ctime()))
        time.sleep(settings.SLEEP_INTERVAL)
