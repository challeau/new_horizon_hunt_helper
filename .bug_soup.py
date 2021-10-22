import os
import pickle
import requests
from bs4 import BeautifulSoup

# Parse web page and store data in bug_elems
page = requests.get('https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)#Northern_Hemisphere')
soup = BeautifulSoup(page.content, 'html.parser')
bug_soup = soup.find_all('div', {'id': 'mw-content-text'})
bug_soup = bug_soup[0].findAll('tbody')
bug_soup = bug_soup[1].findAll('tr')

# create the full list of bug available in game and their data
bug_list = {}
for bug in bug_soup[3:]:
    name = bug.find('a').attrs['title']
    bug_list[name] = {}
    bug_list[name]['price'] = bug.findAll('td')[2].text.strip()
    bug_list[name]['location'] = bug.findAll('td')[3].text.strip()
    bug_list[name]['time'] = bug.findAll('td')[4].text.strip()
    bug_list[name]['season'] = {}
    for month in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'}:
        if bug.findAll('td')[5 + int(month) - 1].text.strip() == '✓':
            bug_list[name]['season'][month] = 1
        else:
            bug_list[name]['season'][month] = 0

os.system('touch .bug_soup')
f = open('.bug_soup', 'wb')
pickle.dump(bug_list, f)
f.close()
