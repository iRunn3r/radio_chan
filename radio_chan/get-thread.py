from bs4 import BeautifulSoup
from operator import itemgetter
import json
import re
import requests

import radio_chan.utilities

# This is where the script will try to find the thread
URL = "https://boards.4channel.org/wsg/catalog"

# Thread URL, without the thread number. The number will be added by the script
THREAD_URL_INCOMPLETE = "https://boards.4channel.org/wsg/thread/"

# Key phrase that should be looked for in the thread name/teaser (case-insensitive)
SEARCH_TERM = "YGYL"

SAVE_PATH = "staging/thread.txt"


def find_most_popular(collection):
    for item in collection:
        if SEARCH_TERM.lower() in item[1].lower() or SEARCH_TERM.lower() in item[2].lower():
            return item[0]
    return None


def start():
    page = requests.get(URL, allow_redirects=False)
    soup = BeautifulSoup(page.text, "lxml")
    head = soup.find("head")

    all_threads = list()
    matches = re.findall(r'\"(\d{7,8})\":(.*?)(?=,\"\d{7,8}\")', str(head))
    for match in matches:
        # Add entries in the following parameter order:
        # Thread ID, Sub Name, Teaser, Reply Count, Image Reply Count
        thread_id = match[0]
        data = json.loads(match[1])
        all_threads.append([thread_id, data["sub"], data["teaser"], data["r"], data["i"]])

    all_threads = sorted(all_threads, key=itemgetter(4), reverse=True)
    found_id = None
    for thread in all_threads:
        if SEARCH_TERM.lower() in thread[1].lower() or SEARCH_TERM.lower() in thread[2].lower():
            found_id = thread[0]
            break

    if found_id is None:
        raise Exception("Could not find any threads matching the search term.")

    result = THREAD_URL_INCOMPLETE + found_id
    print(f"Found thread: {result}")
    radio_chan.utilities.write_to_file(result, SAVE_PATH)


if __name__ == "__main__":
    start()
