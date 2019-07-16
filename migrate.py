import ast
import os
import pickle


IS_TEST_ENV = os.environ.get("IS_TEST_ENV")

DATA_FILE = "data.json"
if IS_TEST_ENV:
    DATA_FILE = "test_data.json"

participants = {}
voting = {}


def load_old_participants():
    global participants

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        file_text = f.read()
        data = ast.literal_eval(file_text)
        participants = ast.literal_eval(data["participants"])


def save_participants():
    with open(DATA_FILE, 'wb') as f:
        data = {
            "participants": participants,
            "voting": {}
        }
        pickle.dump(data, f)


load_old_participants()

save_participants()
