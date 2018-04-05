"""
name: program.py
desc: script to implement the logic of the team-names program
date: 03/31/18
author: Angelina Li
"""

import csv
import json
import os
import random

# reusable global dirnames / filenames / vars

BASEDIR = os.path.abspath(os.path.dirname(__file__))
INPUTDIR = os.path.join(BASEDIR, "input")
OUTPUTDIR = os.path.join(BASEDIR, "output")
STORDIR = os.path.join(BASEDIR, "storage")

UNUSEDFILE = os.path.join(STORDIR, "unused.json")
USEDFILE = os.path.join(STORDIR, "used.json")
TEAMSFILE = os.path.join(STORDIR, "teams_storage.json")
OUTPUTFILE = os.path.join(OUTPUTDIR, "team_names.csv")

HEADINGS = ["team_name", "d1_name", "d1_school", "d2_name", "d2_school"]

# helper functions to write and read data #

def get_txt_data(filename):
    """ get data from text file where data is delimited by each new line """
    with open(filename, "r") as fl:
        return fl.read().strip().split("\n")

def get_json_data(filepath):
    with open(filepath, "r") as fl:
        return json.loads(fl.read())

def save_json_data(filepath, data):
    with open(filepath, "w") as fl:
        fl.write(json.dumps(data))

# initialize program storage files #

def get_fish_names(filename):
    """
    generate a unique list of fish names from a potentially non 
    unique list of fish names
    """
    filename = os.path.join(INPUTDIR, filename)
    all_names = get_txt_data(filename)
    fish_names = []
    for name in all_names:
        name = " ".join([w.capitalize() for w in name.split()])
        if name not in fish_names:
            fish_names.append(name)
    return fish_names

def init_files():
    unused_names = get_fish_names("fish_names.txt")
    save_json_data(UNUSEDFILE, unused_names)
    save_json_data(USEDFILE, [])
    save_json_data(TEAMSFILE, [])

    with open(OUTPUTFILE, "w") as fl:
        writer = csv.writer(fl)
        writer.writerow(HEADINGS)

# program functions #

def add_new_fish_names(filename):
    new_names = get_fish_names(filename)
    unused_names = get_json_data(UNUSEDFILE)
    used_names = get_json_data(USEDFILE)
    num_unused = len(unused_names)
    for name in new_names:
        if name not in unused_names and name not in used_names:
            unused_names.append(name)
    save_json_data(UNUSEDFILE, unused_names)
    print("{} new fish names added".format(len(unused_names) - num_unused))


def get_teams(filepath):
    """ Load all teams from csvfile as dictionaries """
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        headings = [ head.lower() for head in next(reader) ]
        return [ dict(zip(headings, data)) for data in reader ]

def get_processed_debaters():
    """
    Return a list of all the names of debaters who have already been processed
    """
    old_teams = get_json_data(TEAMSFILE)
    names = []
    for team_dict in old_teams:
        names.append(team_dict["d1_name"])
        names.append(team_dict["d2_name"])
    return names

def get_last_initials(team_dict):
    first = team_dict["d1_name"].split()[-1][0]
    second = team_dict["d2_name"].split()[-1][0]
    return "".join(sorted([first, second])).upper()

def get_data_list(team_dict):
    return [team_dict[varname] for varname in HEADINGS]

def get_team_names(filepath):
    teams = get_teams(filepath)
    processed = get_processed_debaters()
    unused_names = get_json_data(UNUSEDFILE)
    used_names = get_json_data(USEDFILE)
    
    if len(unused_names) < len(teams):
        raise Exception("Need to add more fish names")
    
    for i, team_dict in enumerate(teams):
        d1_name = team_dict["d1_name"]
        d2_name = team_dict["d2_name"]
        if d1_name in processed or d2_name in processed:
            print("Team consisting of {} and {} has been processed before!".format(
                d1_name, d2_name))
            continue
        index = random.randint(0, len(unused_names) - 1) # inclusive index range
        fish_name = unused_names.pop(index)
        team_name = get_last_initials(team_dict) + " " + fish_name
        team_dict["team_name"] = team_name
        used_names.append(fish_name)
        teams[i] = team_dict

    save_json_data(UNUSEDFILE, unused_names)
    save_json_data(USEDFILE, used_names)
    return teams

def add_processed(teams):
    all_processed = get_json_data(TEAMSFILE) + teams
    save_json_data(TEAMSFILE, all_processed)

def make_team_names(filename):
    filepath = os.path.join(INPUTDIR, filename)
    teams = get_team_names(filepath)
    add_processed(teams)
    team_lists = [get_data_list(team_dict) for team_dict in teams]
    with open(OUTPUTFILE, "a") as fl:
        writer = csv.writer(fl)
        for row in team_lists:
            writer.writerow(row)
    print("Added {} new teams!".format(len(team_lists)))

if __name__ == "__main__":
    # initialize
    # init_files()
    # add_new_fish_names("fish_names2.txt")
    
    # add teams
    make_team_names("input1.csv")
