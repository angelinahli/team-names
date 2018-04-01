"""
name: program.py
desc: script to implement the logic of the team-names program
date: 03/31/18
author: Angelina Li
"""

import csv
import json
import os

# reusable global dirnames / filenames

BASEDIR = os.path.abspath(os.path.dirname(__file__))
INPUTDIR = os.path.join(BASEDIR, "input")
OUTPUTDIR = os.path.join(BASEDIR, "output")
STORDIR = os.path.join(BASEDIR, "storage")

UNUSEDFILE = os.path.join(STORDIR, "unused.json")
USEDFILE = os.path.join(STORDIR, "used.json")
DB_FILE = os.path.join(OUTPUTDIR, "team_names.csv")

# initialize program storage files #

def get_fish_names():
    """
    generate a unique list of fish names from a potentially non 
    unique list of fish names
    """
    filename = os.path.join(INPUTDIR, "fish_names.txt")
    with open(filename, "r") as fl:
        all_names = fl.read().split("\n")
    fish_names = []
    for name in all_names:
        if name not in fish_names:
            fish_names.append(name)
    return fish_names

def store_unused_names():
    """ generate a list of used and unused fish names in json format """
    unused_names = get_fish_names()
    used_names = []
    with open(UNUSEDFILE, "w") as fl:
        fl.write(json.dumps(unused_names))
    with open(USEDFILE, "w") as fl:
        fl.write(json.dumps(used_names))


# program functions #

def get_teams(filename):
    """ Load all teams from csvfile as dictionaries """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        headings = next(reader)
        return [ dict(zip(headings, data)) for data in reader ]


# * store a list of used and unused fish names in json format
# * store already generated team names in json format
# * generate a new team name from either: (a) a csv file or (b) manually enterred
# * generate a csv file mapping names and schools to team names

if __name__ == "__main__":
    store_unused_names()