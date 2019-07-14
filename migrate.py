import ast
import os


IS_TEST_ENV = os.environ.get("IS_TEST_ENV")

DATA_FILE = "data.json"
if IS_TEST_ENV:
    DATA_FILE = "test_data.json"

participants = {}


def load_old_participants():
    global participants

    with open(DATA_FILE, encoding='utf-8') as f:
        file_text = f.read()
        data = ast.literal_eval(file_text)
        participants = ast.literal_eval(data["participants"])


def save_participants():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        data = {
            "participants": str(participants)
        }
        f.write(str(data))

load_old_participants()

for k, v in list(participants.items()):
    participants[int(k)] = participants.pop(k)

save_participants()
