import ast


DATA_FILE = "data.json"


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
with open("data_backup_migration", 'w', encoding='utf-8') as f:
        f.write(str(participants))

for p in participants:
    if "art" not in participants[p]:
        participants[p]["art"] = 0
save_participants()
