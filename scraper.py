import time

from craigslist import CraigslistHousing, CraigslistForSale
from dateutil.parser import parse
from slack import WebClient
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
import settings
from util import post_listing_to_slack, find_points_of_interest
import os
from datetime import date

engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()


class Listing(Base):
    # Table to store data on craigslist listings.
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)
    area = Column(String)
    transit_stop = Column(String)
    # description = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def scrape_job(area, filter):
    # Scrapes craigslist area, and returns list of latest listings.
    if settings.HOUSE_SEARCH:
        cl_ = CraigslistHousing(site=settings.SITE, area=area, category=settings.CATEGORY, filters=filter)
    else:
        cl_ = CraigslistForSale(site=settings.SITE, area=area, category=settings.CATEGORY, filters=filter)
    approx_count = cl_.get_results_approx_count()
    print(f'Got approximately {approx_count} results')
    results = []
    gen = cl_.get_results(sort_by='newest', geotagged=True, limit=300)
    max_results = min(200,approx_count)
    n = 0
    # for n in range(max_results)
    while True:
        n+=1
        if n > max_results:
            break
        try:
            result = next(gen)

        except StopIteration:
            break
        except Exception as e:
            print(e)
            continue

        # print(result)
        
        # Don't store the listing if it already exists.
        if session.query(Listing).filter_by(cl_id=result["id"]).first() is None:
            if result["where"] is None:
                # If there is no string identifying which neighborhood the result is from, skip it.
                print('where is none: continue?', result)

                # continue
            if any(tok in result["name"].lower() for tok in settings.BLACKLIST_TOKENS):
                print(f'blacklisted: {result["name"].lower()}')
                continue

            lat = 0
            lon = 0
            if result.get("geotag", None) is not None:
                # Assign the coordinates.
                lat = result["geotag"][0]
                lon = result["geotag"][1]

                # Annotate the result with information about the area it's in and points of interest near it.
                geo_data = find_points_of_interest(result["geotag"], result["where"])
                result.update(geo_data)
            else:
                pass
                # result["area"] = ""
                # result["transit"] = ""

            # Try parsing the price.
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            # # Try parsing description.
            # result["description"] = ''
            # try:
            #     response = requests.get(result["url"], headers={'User-Agent': settings.USERAGENT})
            #     soup = BeautifulSoup(response.text, 'html.parser')
            #     # TODO can also parse image urls here and other in post content.
            #     desc = str(soup.find('section', {'id': 'postingbody'}).text)
            #     result["description"] = desc.replace('QR Code Link to This Post', '').strip()
            #     if any(tok in desc.lower() for tok in settings.BLACKLIST_TOKENS):
            #         continue
            # except Exception:
            #     pass
            
            # Create the listing object.
            try:
                listing = Listing(
                    link=result["url"],
                    created=parse(date.today().isoformat()), #parse(result["datetime"]),
                    lat=lat,
                    lon=lon,
                    name=result["name"],
                    price=price,
                    location=result["where"],
                    cl_id=result["id"],
                    # area=result["area"],
                    # transit_stop=result["transit"],
                    # description=result["description"]
                )

                # Save the listing so we don't grab it again.
                session.add(listing)
                session.commit()
            except Exception as e:
                print(f'Skipping making listing for {result["name"]}, Exception: {e}')

            # Return the result if it's near a transit station, or if it is in an area we defined.
            # if len(result["transit"]) > 0 or len(result["area"]) > 0:
            results.append(result)
        # else:
        # results.append(result)
    return results


def do_scrape():
    # Posts craigslist scraper results to slack.
    sc = WebClient(token=settings.SLACK_TOKEN)

    # Get all the results from craigslist.
    all_results = []
    for area in settings.AREAS:
        for filter in settings.FILTERS:
            all_results += scrape_job(area, filter)

    print("{}: Got {} results".format(time.ctime(), len(all_results)))

    # Post to slack.
    for result in all_results:
        post_listing_to_slack(sc, result, reply_description=False)
