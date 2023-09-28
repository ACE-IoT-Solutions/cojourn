from os.path import exists
from pathlib import Path
from shutil import copyfile
import json
import uuid

def generate_new_state():
    copyfile(f"{Path(__file__).parent / 'example-state.json'}", 'state.json')
    with open('state.json', 'r', encoding='utf-8') as statefile:
        state = json.loads(statefile.read())
    state['home']['id'] = str(uuid.uuid1())
    with open('state.json', 'w', encoding='utf-8') as statefile:
        statefile.write(json.dumps(state))

def load_state():
    if not exists('state.json'):
        generate_new_state()

    with open('state.json', 'r', encoding='utf-8') as statefile:
        data = statefile.read()
        return json.loads(data)

def save_state(state):
    if not state or len(state) == 0:
        print("attempting to save empty state. aborting")
        return

    state_string = json.dumps(state, sort_keys=True, indent=2)
    if len(state_string) == 0:
        return
    with open('state.json', 'w+', encoding='utf-8') as statefile:
        statefile.write(state_string)
