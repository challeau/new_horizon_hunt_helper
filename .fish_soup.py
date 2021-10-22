import os
import pickle
import requests
from bs4 import BeautifulSoup


def get_fish_soup():
    """Parse webpage to get fish data and return the resulting soup."""
    page = requests.get('https://animalcrossing.fandom.com/wiki/'
                        'Fish_(New_Horizons)#Northern%20Hemisphere')
    soup = BeautifulSoup(page.content, 'html.parser')
    fish_soup = soup.find_all('div', {'id': 'mw-content-text'})
    fish_soup = fish_soup[0].findAll('tbody')
    fish_soup = fish_soup[1].findAll('tr')
    return fish_soup


def get_fish_rarity(name: str):
    """Return rarity of the fish represented by name."""

    rar_fish = {}
    rar_fish[1] = {
        'Bitterling', 'Crucian carp', 'Dace', 'Goldfish', 'Killifish',
        'Crawfish', 'Tadpole', 'Frog (fish)', 'Freshwater goby', 'Loach',
        'Yellow perch', 'Black bass', 'Tilapia', 'Pond smelt',
        'Sea butterfly', 'Sea horse', 'Clownfish', 'Horse mackerel',
        'Sea bass', 'Dab', 'Olive flounder', 'Squid'
    }
    rar_fish[2] = {
        'Pale chub', 'Carp', 'Koi', 'Pop-eyed goldfish', 'Snapping Turtle',
        'Catfish', 'Bluegill', 'Pike', 'Sweetfish', 'Salmon', 'Guppy',
        'Nibble fish', 'Angelfish', 'Betta', 'Neon tetra', 'Piranha',
        'Arowana', 'Butterfly fish', 'Zebra turkeyfish', 'Puffer fish',
        'Anchovy (fish)', 'Barred knifejaw', 'Red snapper',
        'Suckerfish', 'Barreleye', 'Football fish'
    }
    rar_fish[3] = {
        'Soft-shelled turtle', 'Cherry salmon', 'Golden trout',
        'King salmon', 'Mitten crab', 'Dorado', 'Gar', 'Arapaima',
        'Sturgeon', 'Surgeonfish', 'Ribbon eel', 'Ocean sunfish',
        'Ray', 'Saw shark', 'Hammerhead shark', 'Great white shark',
        'Whale shark'
    }
    rar_fish[4] = {
        'Ranchu goldfish', 'Giant snakehead', 'Rainbowfish',
        'Saddled bichir', 'Blowfish', 'Moray eel', 'Blue marlin',
        'Giant trevally', 'Oarfish', 'Coelacanth'
    }
    rar_fish[5] = {
        'Char', 'Stringfish', 'Napoleonfish', 'Tuna', 'Mahi-mahi'
    }

    for rar in rar_fish:
        if name in rar_fish[rar]:
            fish_rarity = rar
            break
    return fish_rarity


def get_fish_seasonal_availability(fish_availability):
    """Returns a dictionary representing the fish availibilty by month."""

    seasonal_availability = {}
    year = {
        '1', '2', '3', '4', '5', '6',
        '7', '8', '9', '10', '11', '12'
    }

    for month in year:
        if fish_availability[6 + int(month) - 1].text.strip() == '✓':
            seasonal_availability[month] = 1
        else:
            seasonal_availability[month] = 0
    return seasonal_availability


def get_fish_list(fish_soup):
    fish_list = {}
    for fish in fish_soup[3:]:
        name = fish.find('a').attrs['title']
        fish_list[name] = {}
        fish_list[name]['price'] = fish.findAll('td')[2].text.strip()
        fish_list[name]['rarity'] = get_fish_rarity(name)
        fish_list[name]['location'] = fish.findAll('td')[3].text.strip()
        fish_list[name]['size'] = fish.findAll('td')[4].text.strip()
        fish_list[name]['time'] = fish.findAll('td')[5].text.strip()
        fish_list[name]['season'] = get_fish_seasonal_availability(
            fish.findAll('td'))
    return fish_list


def main():
    fish_soup = get_fish_soup()
    fish_list = get_fish_list(fish_soup)
    os.system('touch .fish_soup')
    f = open('.fish_soup', 'wb')
    pickle.dump(fish_list, f)
    f.close()


if __name__ == '__main__':
    main()
