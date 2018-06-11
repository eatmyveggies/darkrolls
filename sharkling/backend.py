import pickle
import datetime


def load(f):
    try:
        with open(f, 'rb') as fp:
            return pickle.load(fp)
    except (IOError, OSError):
        return dict()


def save(data, f):
    try:
        with open(f, 'wb') as fp:
            pickle.dump(data, fp)
    except (IOError, OSError):
        pass


def localize(unaware):
    return unaware.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
