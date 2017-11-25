from . import config


class InvalidRoll(Exception):
    pass


class __roll(object):
    def __init__(self, author, timestamp, value, streak_multiplier):
        self.author = author
        self.timestamp = timestamp
        self.streak_multiplier = streak_multiplier
        self.points = value * streak_multiplier

    def __str__(self):
        return '**{roll_type}** at {timestamp} for **{points}** point{plural} (x{streak_multiplier} streak)'.format(
            roll_type=self.__class__.__name__, timestamp=self.timestamp, points=self.points,
            plural='s' if self.points > 1 else '', streak_multiplier=self.streak_multiplier
        )


class Octs(__roll):
    LENGTH = -8

    def __init__(self, roller, timestamp, value=config.BaseRollValues.Octs, streak_multiplier=1):
        super(Octs, self).__init__(roller, timestamp, value, streak_multiplier)


class Septs(__roll):
    LENGTH = -7

    def __init__(self, roller, timestamp, value=config.BaseRollValues.Septs, streak_multiplier=1):
        super(Septs, self).__init__(roller, timestamp, value, streak_multiplier)


class Sexts(__roll):
    LENGTH = -6

    def __init__(self, roller, timestamp, value=config.BaseRollValues.Sexts, streak_multiplier=1):
        super(Sexts, self).__init__(roller, timestamp, value, streak_multiplier)


class Quints(__roll):
    LENGTH = -5

    def __init__(self, roller, timestamp, value=config.BaseRollValues.Quints, streak_multiplier=1):
        super(Quints, self).__init__(roller, timestamp, value, streak_multiplier)


class Quads(__roll):
    LENGTH = -4

    def __init__(self, roller, timestamp, value=config.BaseRollValues.Quads, streak_multiplier=1):
        super(Quads, self).__init__(roller, timestamp, value, streak_multiplier)


class Trips(__roll):
    LENGTH = -3

    def __init__(self, roller, timestamp, value=config.BaseRollValues.Trips, streak_multiplier=1):
        super(Trips, self).__init__(roller, timestamp, value, streak_multiplier)


class Dubs(__roll):
    LENGTH = -2

    def __init__(self, roller, timestamp, value=config.BaseRollValues.Dubs, streak_multiplier=1):
        super(Dubs, self).__init__(roller, timestamp, value, streak_multiplier)


PRECEDENCE = [Octs, Septs, Sexts, Quints, Quads, Trips, Dubs]


def check(timestamp):
    for roll_type in PRECEDENCE:
        if len(set(timestamp[roll_type.LENGTH:])) == 1:
            return roll_type
    raise InvalidRoll("{attempt} is an invalid roll_type".format(attempt=timestamp))


def get_streak_multiplier(author, last_roll):
    try:
        if last_roll.author == author:
            return last_roll.streak_multiplier + 1
        else:
            return 1
    except AttributeError:
        return 1
