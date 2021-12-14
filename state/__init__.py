import json

def load_state():
    with open('state/state.json', 'r') as f:
        return json.loads(f.read())
