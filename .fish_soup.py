import pickle
import requests
from bs4 import BeautifulSoup

# define fish rarity
rar_fish = {}
rar_fish['1'] = {'Bitterling', 'Crucian carp', 'Dace', 'Goldfish', 'Killifish', 'Crawfish', 'Tadpole', 'Frog (fish)', 'Freshwater goby', 'Loach', 'Yellow perch', 'Black bass', 'Tilapia', 'Pond smelt', 'Sea butterfly', 'Sea horse', 'Clownfish', 'Horse mackerel', 'Sea bass', 'Dab', 'Olive flounder', 'Squid'}
rar_fish['2'] = {'Pale chub', 'Carp', 'Koi', 'Pop-eyed goldfish', 'Snapping Turtle', 'Catfish', 'Bluegill', 'Pike', 'Sweetfish', 'Salmon', 'Guppy', 'Nibble fish', 'Angelfish', 'Betta', 'Neon tetra', 'Piranha', 'Arowana', 'Butterfly fish', 'Zebra turkeyfish', 'Puffer fish', 'Anchovy (fish)', 'Barred knifejaw', 'Red snapper', 'Suckerfish', 'Barreleye', 'Football fish'}
rar_fish[3] = {'Soft-shelled turtle', 'Cherry salmon', 'Golden trout', 'King salmon', 'Mitten crab', 'Dorado', 'Gar', 'Arapaima', 'Sturgeon', 'Surgeonfish', 'Ribbon eel', 'Ocean sunfish', 'Ray', 'Saw shark', 'Hammerhead shark', 'Great white shark', 'Whale shark'}
rar_fish[4] = {'Ranchu goldfish', 'Giant snakehead', 'Rainbowfish', 'Saddled bichir', 'Blowfish', 'Moray eel', 'Blue marlin', 'Giant trevally', 'Oarfish', 'Coelacanth'}
rar_fish[5] = {'Char', 'Stringfish', 'Napoleonfish', 'Tuna', 'Mahi-mahi'}

# parse web page and store data in fish_elems
page = requests.get('https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)#Northern%20Hemisphere')
soup = BeautifulSoup(page.content, 'html.parser').find(title='Northern Hemisphere').findAll('table')[1]
fish_elems = soup.findAll('tr')

# create the full list of fish available in game and their data
fish_list = {}
for fish in fish_elems[1:]:
    name = fish.find('a').attrs['title']
    fish_list[name] = {}
    for rar in rar_fish:
        if name in rar_fish[rar]:
            fish_list[name]['rarity'] = int(rar)
            break
    fish_list[name]['price'] = fish.findAll('td')[2].text.strip()
    fish_list[name]['location'] = fish.findAll('td')[3].text.strip()
    fish_list[name]['size'] = fish.findAll('td')[4].text.strip()
    fish_list[name]['time'] = fish.findAll('td')[5].text.strip()
    fish_list[name]['season'] = {}
    for month in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'}:
        if fish.findAll('td')[6 + int(month) - 1].text.strip() == '✓':
            fish_list[name]['season'][month] = 1
        else:
            fish_list[name]['season'][month] = 0

f = open(".fish_soup", "wb")
pickle.dump(fish_list, f)
f.close()
