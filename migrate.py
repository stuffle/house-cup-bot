import ast
import os
import pickle
import mod
import marriages
import pact


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

save_participants()
