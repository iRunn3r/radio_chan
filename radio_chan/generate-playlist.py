from bs4 import BeautifulSoup
import os
import re
import urllib.request

import radio_chan.utilities

SAVE_PATH = "staging/playlist.m3u"
LOAD_PATH = "staging/thread.txt"


def generate_playlist():
    four_chan = radio_chan.utilities.read_all_text(LOAD_PATH)
    headers = {'User-Agent': 'Mozilla/5.0'}

    req = urllib.request.Request(four_chan, data=None, headers=headers)
    page = urllib.request.urlopen(req)

    links = []
    added = False
    pattern = re.compile("i.*.webm")
    soup = BeautifulSoup(page, 'lxml')
    for link in soup.findAll('a', {'href': pattern}):
        if not added:
            links.append('http://' + str(link.get('href')).replace('//', ''))
            added = True
        else:
            added = False

    radio_chan.utilities.create_directory("staging")
    with open(SAVE_PATH, 'w') as playList:
        for link in links:
            playList.write(link + "\n")

    cwd = os.getcwd()
    playlist_path = os.path.join(cwd, SAVE_PATH)
    print(playlist_path)
