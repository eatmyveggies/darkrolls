class InvalidRoll(Exception):
    def __init__(self, message):
        self.message = message


class __Roll(object):
    def __init__(self, author, timestamp, streak_multiplier):
        self.author = author
        self.timestamp = timestamp
        self.streak_multiplier = streak_multiplier
        self.points = getattr(self.__class__, 'BASE_VALUE', 1) * streak_multiplier

    def __str__(self):
        return '**{roll_type}** at {timestamp} for **{points}** point{plural} (x{streak_multiplier} multiplier)'.format(
            roll_type=self.__class__.__name__, timestamp=self.timestamp, points=self.points,
            plural='s' if self.points > 1 else '', streak_multiplier=self.streak_multiplier
        )


class Octs(__Roll):
    LENGTH = -8
    BASE_MULTIPLIER = 1
    BASE_VALUE = 1600

    def __init__(self, author, timestamp, streak_multiplier=1):
        super(Octs, self).__init__(author, timestamp, streak_multiplier)


class Septs(__Roll):
    LENGTH = -7
    BASE_MULTIPLIER = 1
    BASE_VALUE = 800

    def __init__(self, author, timestamp, streak_multiplier=1):
        super(Septs, self).__init__(author, timestamp, streak_multiplier)


class Sexts(__Roll):
    LENGTH = -6
    BASE_MULTIPLIER = 1
    BASE_VALUE = 400

    def __init__(self, author, timestamp, streak_multiplier=1):
        super(Sexts, self).__init__(author, timestamp, streak_multiplier)


class Quints(__Roll):
    LENGTH = -5
    BASE_MULTIPLIER = 1
    BASE_VALUE = 200

    def __init__(self, author, timestamp, streak_multiplier=1):
        super(Quints, self).__init__(author, timestamp, streak_multiplier)


class Quads(__Roll):
    LENGTH = -4
    BASE_MULTIPLIER = 1
    BASE_VALUE = 50

    def __init__(self, author, timestamp, streak_multiplier=1):
        super(Quads, self).__init__(author, timestamp, streak_multiplier)


class Trips(__Roll):
    LENGTH = -3
    BASE_MULTIPLIER = 1
    BASE_VALUE = 10

    def __init__(self, author, timestamp, streak_multiplier=1):
        super(Trips, self).__init__(author, timestamp, streak_multiplier)


class Dubs(__Roll):
    LENGTH = -2
    BASE_MULTIPLIER = 1
    BASE_VALUE = 1

    def __init__(self, author, timestamp, streak_multiplier=1):
        super(Dubs, self).__init__(author, timestamp, streak_multiplier)


PRECEDENCE = [Octs, Septs, Sexts, Quints, Quads, Trips, Dubs]


def check(timestamp):
    """Check what the author rolled.

    Args:
        timestamp: (str) a date timestamp of the format "YYMMDDHHMM".

    Returns:
        A roll type, which is a subclass of __Roll. For Example, "2017011111"
        will return Quints.

    Raises:
        InvalidRoll if the timestamp does not pass any roll check.
    """
    for roll_type in PRECEDENCE:
        if len(set(timestamp[roll_type.LENGTH:])) == 1:
            return roll_type
    raise InvalidRoll("that's not a roll, sorry")


def get_streak_multiplier(author, last_roll):
    """Increment the streak multiplier based on the previous roll.

    Args:
        author: (str) the name of the roll author.
        last_roll: (__Roll.<roll_type>) the previous roll.

    Returns:
        (int) the roll value multiplier.
    """
    try:
        if last_roll.author == author:  # if it is a subsequent roll, increase the author's multiplier
            return last_roll.streak_multiplier + last_roll.__class__.BASE_MULTIPLIER
        else:  # someone stole the multiplier from the previous author
            return 1
    except AttributeError:
        return 1
