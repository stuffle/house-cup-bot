import ast


BACKUP = ""
DATA_FILE = "test_data.json"


def load_participants(dfile):
    participants = {}

    with open(dfile, encoding='utf-8') as f:
        file_text = f.read()
        participants = ast.literal_eval(file_text)

    return participants


def save_participants():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(str(participants))


participants = load_participants(DATA_FILE)
backup = load_participants(BACKUP)
for p in backup:
    participants[p]["word_count"] = backup[p]["word_count"]
    participants[p]["wc"] = backup[p]["wc"]
save_participants()
