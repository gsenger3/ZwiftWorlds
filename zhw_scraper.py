# zhw_scraper.py
# George Senger
# Scrapes ZwiftHacks.com Worlds Widget and returns active Zwift Worlds as list


import requests
from bs4 import BeautifulSoup

URL = "https://zwifthacks.com/today/"
headers = {'user-agent': 'ZwiftWorlds/0.5 (Primo Studios)'}
#headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}

def get_worlds():
    try:
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="zh_zwift_world_widget-5")
        #print(results.prettify())

        # get the worlds inside the zh_zwift_world_widget div container
        # <div id="zh_zwift_world_widget-5">
        #    <div>
        #       <div>World 0</div>
        #       <div>World 1</div>
        #       <div>World 2</div>
        #    </div>
        # </div>
        zh_zwift_world_widget = results.find("div")
        worlds_widget = zh_zwift_world_widget.find_all("div")

        # add the worlds to list obj
        worlds = []
        for w in worlds_widget:
            worlds.append(w.text)

        print("Active Worlds: " + str(worlds))
        return worlds
    except:
        print("Error retrieving Zwift Worlds.")
        return None

