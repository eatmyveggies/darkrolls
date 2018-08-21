import datetime
from . import actors
from . import roll


class FightError(Exception):
    pass


class Campaign(object):
    def __init__(self):
        self.__start = datetime.datetime.now()
        self.__undeads = list()

    @property
    def undeads(self):
        return self.__undeads

    @property
    def start(self):
        return self.__start

    def get_undead(self, name):
        for undead in self.__undeads:
            if name == undead.name:
                return undead
        return actors.Undead(name)


class Encounter(object):
    def __init__(self, undead, timestamp):
        self.__undead = undead
        self.__timestamp = timestamp

    def outcome(self):
        if getattr(self, '__outcome'):
            raise FightError('fight of {} at {} has already been resolved once'
                             .format(self.__undead.name, self.__timestamp))
        else:
            self.__outcome = roll.verify(self.__timestamp)(self.__undead).resolve()


class Outcome(object):
    pass

class Victory(Outcome):
    def __init__(self):
        pass

class Failure(Outcome):
    def __init__(self):
        pass