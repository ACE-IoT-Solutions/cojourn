from os.path import exists
from pathlib import Path
from shutil import copyfile
import json

def load_state():
    if not exists('state.json'):
        copyfile(f"{Path(__file__).parent / 'example-state.json'}", '/tmp/state.json')

    with open('/tmp/state.json', 'r') as f:
        return json.loads(f.read())

def save_state(state):
    with open('/tmp/state.json', 'w+') as f:
        f.write(json.dumps(state, sort_keys=True, indent=2))
