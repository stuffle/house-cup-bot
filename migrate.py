import ast
import os
import pickle
import mod
import marriages
import pact
from constants import *


IS_TEST_ENV = os.environ.get("IS_TEST_ENV")

DATA_FILE = "data.json"
if IS_TEST_ENV:
    DATA_FILE = "test_data.json"

participants = {}
voting = {}


def load_old_participants():
    global participants

    with open(DATA_FILE, 'rb') as f:
        data = pickle.load(f)
        participants = data["participants"]
        mod.imprisoned = data["imprisoned"]
        mod.voting = data["voting"]
        marriages.proposals = data["proposals"]
        marriages.marriage_info = data["marriage_info"]
        pact.pacts = data["pacts"]


def save_participants():
    with open(DATA_FILE, 'wb') as f:
        data = {
            "participants": participants,
            "imprisoned": {},
            "voting": mod.voting,
            "proposals": marriages.proposals,
            "marriage_info": marriages.marriage_info,
            "pacts": pact.pacts
        }
        pickle.dump(data, f)


load_old_participants()

to_replace = {
    STUFFLE_ID: "stuffle",
    208220191832801280: "mith",
    478970983089438760: "red",
    522514714643660820: "bluepandas"
}

for p_list in pact.pacts:
    count = 0
    for p in pact.pacts[p_list]:
        pact.pacts[p_list][count]["pact"] = p["pact"].replace(str(STUFFLE_ID), "stuffle")
        pact.pacts[p_list][count]["pact"] = p["pact"].replace("<", "")
        pact.pacts[p_list][count]["pact"] = p["pact"].replace(">", "")
        pact.pacts[p_list][count]["pact"] = p["pact"].replace("@", "")
        pact.pacts[p_list][count]["pact"] = p["pact"].replace("!", "")
        pact.pacts[p_list][count]["pact"] = p["pact"].replace(str(208220191832801280), "mith")
        pact.pacts[p_list][count]["pact"] = p["pact"].replace("478970983089438760", "red")
        pact.pacts[p_list][count]["pact"] = p["pact"].replace("522514714643660820", "bluepandas")
        count += 1

save_participants()
