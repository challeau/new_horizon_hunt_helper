import os
import pickle
import datetime
import inquirer
from prettytable import PrettyTable

# Text formatting : bold, green and reset.
B = '\033[1m'
G = '\33[92m'
N = '\033[0m'


def get_fish_list():
    """Return a dict containing all the fish available in-game and their data.

    The list is extracted from the file .fish_soup.
    """
    if os.path.exists('.fish_soup') is False:
        print("Something went wrong... Couldn't find the fish soup")
        exit()
    all_fish = pickle.load(open('.fish_soup', 'rb'))
    return all_fish


def setup_fish_collection(all_fish: dict):
    """Return a dict containing all the fish caught by user and their data.

    Check the existence of the collection file which contains the list of
    fish caught so far:
    -if it exists, prompt user to update it.
    -if it doesn't exists, prompt user to create it.
    """
    if os.path.exists('.collection.txt') is False:
        os.system('touch .collection.txt')
        f = open('.collection.txt', 'r+')
        collection_creation_prompt = [
            inquirer.Checkbox('fish_caught',
                              message="Welcome! Let's see what fish you've "
                              "caught so far. Navigate with ↑ and ↓, select "
                              "with →, and press enter to finish",
                              choices=all_fish)
        ]
        answers = inquirer.prompt(collection_creation_prompt)
        for new_catch in answers['fish_caught']:
            f.write(new_catch + '\n')
    else:
        f = open('.collection.txt', 'r+')
        caught_fish = f.read().splitlines()
        not_caught_fish = {}
        update_list_prompt = None
        while update_list_prompt not in ('y', 'n'):
            update_list_prompt = input('Welcome back! Have you caught any new '
                                       'fish since last time ? (y/n)\n>>> ')
            if (update_list_prompt == 'y'):
                for fish in all_fish:
                    if fish not in caught_fish:
                        not_caught_fish[fish] = all_fish[fish]
                collection_update_prompt = [
                    inquirer.Checkbox('fish_caught',
                                      message='What new fish have you caught? '
                                      'Navigate with ↑ and ↓, select with →, '
                                      'and press enter to finish',
                                      choices=not_caught_fish)
                ]
                answers = inquirer.prompt(collection_update_prompt)
                for new_catch in answers['fish_caught']:
                    f.write(new_catch + '\n')
            elif (update_list_prompt != 'n'):
                update_list_prompt = input('Please answer with y or n.\n>>> ')
    f.close()
    f = open('.collection.txt', 'r+')
    caught_fish = f.read().splitlines()
    return (caught_fish)


def is_catch_time(fish_time: str, usr_time: str):
    """Return True if the fish can be caught at usr_time."""
    if (fish_time == 'All day'):
        return (True)
    elif (fish_time == '4 AM - 9 PM' and usr_time >= 4 and usr_time < 21):
        return (True)
    elif (fish_time == '9 AM - 4 PM' and usr_time >= 9 and usr_time < 16):
        return (True)
    elif (fish_time == '4 PM - 9 AM' and (usr_time >= 16 or usr_time < 9)):
        return (True)
    elif (fish_time == '9 PM - 4 AM' and (usr_time >= 21 or usr_time < 4)):
        return (True)
    elif (fish_time == '9 AM - 4 PM & 9 PM - 4 AM'
          and ((usr_time >= 9 and usr_time < 16) or (usr_time >= 21
                                                     or usr_time < 4))):
        return (True)
    else:
        return (False)


def get_available_fish_list(all_fish: dict, caught_fish: dict):
    """Return a list of all fish available at run time and their data."""
    today = datetime.datetime(2021, 11, 1, 0, 10, 10)
    # today = datetime.datetime.today()
    available_fish = {}
    for fish in all_fish:
        if (all_fish[fish]['season'][str(today.month)] == 1):
            fish_catch_time = all_fish[fish]['time']
            usr_time = today.hour
            if is_catch_time(fish_catch_time, usr_time):
                available_fish[fish] = all_fish[fish]
    for fish in available_fish:
        if fish in caught_fish:
            available_fish[fish]['caught'] = '✔'
        else:
            available_fish[fish]['caught'] = '✘'
    return available_fish


def print_tab(available_fish: dict, caught_fish: dict):
    """Create and print a tab containing the data of all available fish."""
    tab = PrettyTable()
    tab.field_names = [
        'NAME', 'PRICE', 'RARITY',
        'SIZE', 'LOCATION', 'CAUGHT ?'
    ]
    for fish in available_fish:
        if fish not in caught_fish:
            p = str(available_fish[fish]['price'])
            r = str(available_fish[fish]['rarity'])
            s = str(available_fish[fish]['size'])
            lo = available_fish[fish]['location']
            c = available_fish[fish]['caught']
            tab.add_row([B+G+fish+N, B+G+p+N, B+G+r+N,
                         B+G+s+N, B+G+lo+N, B+G+c+N])
    for fish in available_fish:
        if fish in caught_fish:
            p = str(available_fish[fish]['price'])
            r = str(available_fish[fish]['rarity'])
            s = str(available_fish[fish]['size'])
            lo = available_fish[fish]['location']
            c = available_fish[fish]['caught']
            tab.add_row([fish, p, r, s, lo, c])
    print("\nHere's a list of available fish right now:")
    print(tab)


def main():
    all_fish = get_fish_list()
    caught_fish = setup_fish_collection(all_fish)
    print(caught_fish)
    available_fish = get_available_fish_list(all_fish, caught_fish)
    print_tab(available_fish, caught_fish)


if __name__ == '__main__':
    main()
