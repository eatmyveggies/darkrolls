import time
import random
import datetime
import threading
from . import actors
from . import config
from . import inventory


def generate_weapon(undead):
    level = random.randint(0, undead.level / 6)
    return inventory.Weapon(
        level=level, **config.weapons[random.choice(
            [weapon for weapon in config.weapons if
             config.weapons[weapon]['tier'] <= min(
                 undead.level / 15, config.options['weapons']['max_tier'])])])


class Bonfire(threading.Thread):
    def __init__(self, campaign):
        super(Bonfire, self).__init__()
        self.__campaign = campaign
        self.daemon = True

    def run(self):
        while True:
            now = datetime.datetime.now()
            for undead in self.__campaign.undeads:
                if now > undead.resting:
                    undead.resting = None
            time.sleep(10)


class Campaign(object):
    def __init__(self):
        self.__start = datetime.datetime.now()
        self.__encounters = dict()
        self.__undeads = dict()

    @property
    def undeads(self):
        return self.__undeads

    @property
    def start(self):
        return self.__start

    @property
    def encounters(self):
        return self.__encounters

    def find(self, name):
        try:
            return self.__undeads[name]
        except KeyError:
            self.__undeads[name] = actors.Undead(name)
            return self.__undeads[name]


class Encounter(object):
    def __init__(self, undead, timestamp, campaign):
        self.__undead = undead
        self.__timestamp = timestamp
        self.__campaign = campaign

    @property
    def undead(self):
        return self.__undead

    def outcome(self):
        pass
