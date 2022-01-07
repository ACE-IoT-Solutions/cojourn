from os.path import exists
from shutil import copyfile
import json

def load_state():
    if not exists('state/state.json'):
        copyfile('state/example-state.json', 'state/state.json')

    with open('state/state.json', 'r') as f:
        return json.loads(f.read())

def save_state(state):
    with open('state/state.json', 'w+') as f:
        f.write(json.dumps(state, sort_keys=True, indent=2))
