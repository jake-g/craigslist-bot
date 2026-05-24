# Development Notes - Seattle Area Refactoring & Cleanup (2023)

These notes document the experimental changes made to the scraper, settings, and utilities, which are currently checked into this branch.

## 1. What was being worked on
* **Seattle Neighborhood Geofence Expansion**:
  * Significantly expanded target `NEIGHBORHOODS` and `BOXES` in `settings.py` for Seattle.
  * Replaced underscores with spaces in area keys (e.g. `"green_lake"` -> `"green lake"`).
* **Scraper Performance Optimization & Simplification**:
  * Disabled BeautifulSoup parsing of Craigslist description pages (`scraper.py`) to bypass page requests, avoiding potential IP/rate limits and speeding up runs.
  * Commented out transit checking logic entirely.
  * Overrode the Listing `created` date to use the runner's current date: `parse(date.today().isoformat())`.
  * Removed transit/area-match filters so listings are appended/scraped unconditionally.
* **Result Caching**:
  * Added `save_dict_to_file` and `load_dict_from_file` using `pickle` in `util.py` (referenced in `craigslist_api_test.ipynb`).

---

## 2. Currently Unresolved Bugs / Issues

* **TypeError on `find_points_of_interest` call**:
  * `scraper.py` calls `find_points_of_interest` with only 2 arguments (geotag, location), but `util.py` redefined it to take 3 (geotag, location, url).
* **ValueError on Dictionary Update**:
  * `scraper.py` does `result.update(geo_data)`, but `find_points_of_interest` now returns a string (`area`) instead of a dictionary.
* **KeyError on `'area'` key**:
  * If a listing has no geotag or if `result.update(geo_data)` fails/is bypassed, `result['area']` is not populated. However, `post_listing_to_slack` accesses `listing['area']`, causing a crash.

---

## 3. Dependency Requirements
* The standard `python-craigslist` package is broken (issue #122). You must install the fork from GitHub:
  ```bash
  pip install git+https://github.com/ethan021021/python-craigslist.git
  ```
