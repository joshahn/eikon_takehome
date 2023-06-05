#/usr/bin/env python

import csv
import json
import random

from db.database import check_exists, create_table, fetch_all, fetch_one, write_to
from models.Compound import Compound
from models.User import User
from models.UserExperiment import UserExperiment

DATA_DIR = "data"
USERS_CSV = "{}/users.csv".format(DATA_DIR)
COMPOUNDS_CSV = "{}/compounds.csv".format(DATA_DIR)
USER_EXPERIMENT_CSV = "{}/user_experiments.csv".format(DATA_DIR)
USERS = "users"
COMPOUNDS = "compounds"
USER_EXPERIMENTS = "user_experiments"


def run_etl():
    users = extract_csv(USERS_CSV, User)
    load_users = load(users, USERS)

    compounds = extract_csv(COMPOUNDS_CSV, Compound)
    load_compounds = load(compounds, COMPOUNDS)

    user_experiments = extract_csv(USER_EXPERIMENT_CSV, UserExperiment)
    load_user_experiments = load(user_experiments, USER_EXPERIMENTS)

    return load_users and load_compounds and load_user_experiments


def extract_csv(csv_filename, model):
    lst = []
    with open(csv_filename, "r") as f:
        data = csv.reader(f,  quotechar='"')
        next(data, None) 
        for line in data:
            if line:
                item = model(line)
                if item:
                    lst.append(item.as_list())
    return lst

def load(objects, tablename):
    if check_exists(tablename):
        return write_to(objects, tablename)
    else:
        print("Table {} doesn't exist".format(tablename))
        return False

def get_total_experiments(user_id):
    query = "SELECT * FROM user_experiments WHERE user_id = {id}".format(id=user_id)
    response = fetch_all(query)
    num_exp = len(response)
    print("DEBUG: User {} ran {} experiments".format(user_id, num_exp))
    return num_exp

def get_average_experiment_per_user():
    query = "SELECT user_id FROM users"
    ids = fetch_all(query) 
    if ids:
        counts_per_user = []
        user_count = len(ids)
        for i in ids:
            counts_per_user.append(get_total_experiments(i[0]))
        avg_run = sum(counts_per_user) / user_count
        print("DEBUG: Average number of experiments ran per user: {}".format(avg_run))
        return avg_run
    else:
        return None

def get_most_commonly_used_compound(user_id):
    query = "SELECT experiment_compounds_ids FROM user_experiments WHERE user_id = {id}".format(id=user_id)
    experiments = fetch_all(query)
    if experiments:
        all_compounds = []
        for experiment in experiments:
            all_compounds += experiment[0]
        # This is a bit superfluous. Having fun returning a random compound
        # if there are multiple most commonly used compounds since the requirement
        # only asks for one compound
        compound_counter = {}
        for compound in all_compounds:
            if compound in compound_counter.keys():
                compound_counter[compound] += 1
            else:
                compound_counter[compound] = 1
        most_common = []
        mode = max(compound_counter.values())
        for compound, count in compound_counter.items():
            if count == mode:
                most_common.append(compound)
        random_compound = random.choice(most_common)
        print("DEBUG: Randomly returning {} from most commonly used compounds {}".format(random_compound, most_common))
        return get_compound_name(random_compound)
    else:
        print("DEBUG: No experiments ran for user {}".format(user_id))
        return None

def user_id_exists(user_id):
    query = "SELECT user_id FROM users WHERE id = {i}".format(i=user_id)
    ids = fetch_all(query)
    id_len = len(ids)
    if id_len < 1:
        print("DEBUG: No user found for user id: {}".format(user_id))
        return 0
    elif id_len > 1:
        print("ERROR: Multiple users found for user id: {}".format(user_id))
        return  -1
    else:
        print(ids)
        return ids[0][0]


def get_user_id_from_email(email):
    query = "SELECT user_id FROM users WHERE email = '{email}'".format(email=email.strip())
    ids = fetch_all(query)
    id_len = len(ids)
    if id_len < 1:
        print("DEBUG: No user found for email: {}".format(email))
        return 0
    elif id_len > 1:
        print("ERROR: Multiple users found for email: {}".format(email))
        return  -1
    else:
        print(ids)
        return ids[0][0]

def get_compound_name(compound_id):
    query = "SELECT compound_name FROM compounds WHERE compound_id = '{id}'".format(id=compound_id)
    compound_name = fetch_one(query)[0]
    print("DEBUG: Compound id {} is compound name: {}".format(compound_id, compound_name))
    return compound_name
