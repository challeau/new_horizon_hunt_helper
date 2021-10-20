import os
import pickle
import datetime
import inquirer
from prettytable import PrettyTable

# check if the program has been run before.
# if not, parse webpage to create the fish list.
if os.path.exists(".fish_soup") is False:
    os.system('touch .fish_soup')
    print("creating fish soup...")
    os.system('python3 .fish_soup.py')

fish_list = pickle.load(open(".fish_soup", "rb"))

caught_fish_list = {}
not_caught_fish_list = {}
if os.path.exists(".tag.txt") is False:
    os.system('touch .tag.txt')
    f = open(".tag.txt", "r+")
    questions = [
        inquirer.Checkbox('fish',
                          message="Welcome! Let's see what fish you've caught so far",
                          choices=fish_list)]
    print("Navigate with ↑ and ↓, select with →, and press enter to finish.")
    answers = inquirer.prompt(questions)
    for new_catch in answers['fish']:
        f.write(new_catch)
        f.write("\n")
else:
    f = open(".tag.txt", "r+")
    caught_fish_list = f.read().splitlines()
    status = None
    while status not in ("y", "n"):
        status = input("Welcome back! Have you caught any new fish since last time ? (y/n)?\n>>> ")
        if (status == "y"):
            for fish in fish_list:
                if fish not in caught_fish_list:
                    not_caught_fish_list[fish] = fish_list[fish]
            questions = [
                inquirer.Checkbox('fish',
                                  message="What fish have you caught?",
                                  choices=not_caught_fish_list)]
            print("Navigate with ↑ and ↓, select with →, and press enter to finish.")
            answers = inquirer.prompt(questions)
            for new_catch in answers['fish']:
                f.write(new_catch)
                f.write("\n")
        elif (status != "n"):
            status = input("Please answer with y or n.\n>>> ")
f.close()
f = open(".tag.txt", "r+")
caught_fish_list = f.read().splitlines()

# create current_fish list: fish that is available right now
# today = datetime.datetime.today()
today = datetime.datetime(2021, 11, 1, 0, 10, 10)

current_fish = {}
for fish in fish_list:
    if fish_list[fish]['season'][str(today.month)] == 1:
        if fish_list[fish]['time'] == 'All day':
            current_fish[fish] = fish_list[fish]
        elif fish_list[fish]['time'] == '4 AM - 9 PM' and today.hour >= 4 and today.hour < 21:
            current_fish[fish] = fish_list[fish]
        elif fish_list[fish]['time'] == '9 AM - 4 PM' and today.hour >= 9 and today.hour < 16:
            current_fish[fish] = fish_list[fish]
        elif fish_list[fish]['time'] == '4 PM - 9 AM' and (today.hour >= 16 or today.hour < 9):
            current_fish[fish] = fish_list[fish]
        elif fish_list[fish]['time'] == '9 PM - 4 AM' and (today.hour >= 21 or today.hour < 4):
            current_fish[fish] = fish_list[fish]
        elif fish_list[fish]['time'] == '9 AM - 4 PM & 9 PM - 4 AM' and ((today.hour >= 9 and today.hour < 16) or (today.hour >= 21 or today.hour < 4)):
            current_fish[fish] = fish_list[fish]

# define status.
for fish in current_fish:
    if fish in caught_fish_list:
        current_fish[fish]['caught'] = '✔'
    else:
        current_fish[fish]['caught'] = '✘'

# formatting
B = '\033[1m'  # BOLD
C = "\33[92m"  # COLOR
N = "\033[0m"  # RESET

# create a tab with all the data and print it, with the fish already caught at the bottom.
tab = PrettyTable()
tab.field_names = ['NAME', 'PRICE', 'RARITY', 'SIZE', 'LOCATION', 'CAUGHT ?']
for fish in current_fish:
    if fish not in caught_fish_list:
        p = str(current_fish[fish]['price'])
        r = str(current_fish[fish]['rarity'])
        s = str(current_fish[fish]['size'])
        lo = current_fish[fish]['location']
        c = current_fish[fish]['caught']
        tab.add_row([B+C+fish+N, B+C+p+N, B+C+r+N, B+C+s+N, B+C+lo+N, B+C+c+N])

for fish in current_fish:
    if fish in caught_fish_list:
        p = str(current_fish[fish]['price'])
        r = str(current_fish[fish]['rarity'])
        s = str(current_fish[fish]['size'])
        lo = current_fish[fish]['location']
        c = current_fish[fish]['caught']
        tab.add_row([fish, p, r, s, lo, c])

print("\nHere's a list of available fish right now:")
print(tab)
