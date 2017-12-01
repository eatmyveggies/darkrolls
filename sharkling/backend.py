import json


def load(f):
    try:
        with open(f, 'r') as fp:
            return json.load(fp)
    except (IOError, OSError):
        return {}


def save(data, f):
    try:
        with open(f, 'w') as fp:
            json.dump(data, fp)
    except (IOError, OSError):
        pass
