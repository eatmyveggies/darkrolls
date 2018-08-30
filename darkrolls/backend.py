import sys
import dill
import logging
import datetime
from . import game

log = logging.getLogger(__name__)


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
        log.info('successfully saved state')
    except (IOError, OSError):
        log.exception('could not save state because')


def localize(unaware):
    return unaware.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

def on_exit(sig, frame, game):
    log.critical('entered signal handler')
    game.save()
    sys.exit(0)


def setup_logger(name, format, path):
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(format))
    console.setLevel(logging.INFO)
    file = logging.FileHandler(filename=path, encoding='utf-8', mode='a')
    file.setFormatter(logging.Formatter(format))
    file.setLevel(logging.INFO)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(file)
    root.addHandler(console)
