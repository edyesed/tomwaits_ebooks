#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup as bs

BASE_DOMAIN='http://www.tomwaits.com'

if __name__ == "__main__":
    song_list_url = f"{BASE_DOMAIN}/songs/"
    song_list_html = requests.get(song_list_url)
    bs_tw = bs(song_list_html.text, 'html.parser')
    song_list = bs_tw.find_all("li")
    for song in song_list:
        song_html_url = f"{BASE_DOMAIN}{song.a.get('href')}"
        song_html = requests.get(song_html_url)
        song_bs = bs(song_html.text)
        song_name_lower = song.a.get('href').split('/')[-2].lower()
        fh = open(f"{song_name_lower}.txt", 'w')
        fh.write(song_bs.find_all("div", {"class": "songs-lyrics"})[0].text.lstrip().rstrip())
        fh.close()
        print(song_html_url)
        