import ast
import os
import pickle
import mod
import marriages


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


def save_participants():
    with open(DATA_FILE, 'wb') as f:
        data = {
            "participants": participants,
            "voting": mod.voting,
            "proposals": {},
            "marriage_info": {}
        }
        pickle.dump(data, f)


load_old_participants()

save_participants()
