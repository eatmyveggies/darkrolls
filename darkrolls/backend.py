import dill
import datetime
from . import game


def recover(path):
    try:
        return load(path)
    except Exception:
        return game.Campaign()


def load(f):
    with open(f, 'rb') as fp:
        return dill.load(fp)


def save(data, f):
    try:
        with open(f, 'wb') as fp:
            dill.dump(data, fp)
    except (IOError, OSError):
        pass


def localize(unaware):
    return unaware.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
