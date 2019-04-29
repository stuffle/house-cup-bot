import ast


DATA_FILE = "data.json"
participants = {}

def load_old_participants(dfile):
    global participants

    with open(dfile, encoding='utf-8') as f:
        file_text = f.read()
        participants = ast.literal_eval(file_text)

    return participants


def save_participants():
    print("in save")
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        data = {
            "participants": str(participants)
        }
        f.write(str(data))


participants = load_old_participants(DATA_FILE)
save_participants()
