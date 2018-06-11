import random


class Invalid(Exception):
    def __init__(self, message):
        self.message = message


class OnCooldown(Exception):
    def __init__(self, message):
        self.message = message


class Duplicate(Exception):
    def __init__(self, message):
        self.message = message


class __OnRollEvent(Exception):
    def __init__(self, roll):
        self.roll = roll


class BadRng(__OnRollEvent):
    TAG = 'REKT'
    REACTION = '\U0001F61F'

    def __init__(self, roll):
        super(BadRng, self).__init__(roll)


class GoodRng(__OnRollEvent):
    TAG = 'TURBO'
    REACTION = '\U0001F525'

    def __init__(self, roll):
        super(GoodRng, self).__init__(roll)


class __Roll(object):
    def __init__(self, owner, timestamp, streak_multiplier):
        self.owner = owner
        self.timestamp = timestamp
        self.streak_multiplier = streak_multiplier

    @property
    def points(self):
        return getattr(self.__class__, 'BASE_VALUE', 1) * \
               self.streak_multiplier * getattr(self, 'rng_points_multiplier', 1)

    def __str__(self):
        return '**{roll_type}** at {timestamp} for **{points}** point{plural} ' \
               '({streak_multiplier}x from streak{rng_points_multiplier}) by {owner}'.format(
            roll_type=self.__class__.__name__, timestamp=self.timestamp, points=self.points,
            plural='s' if self.points > 1 else '', streak_multiplier=self.streak_multiplier,
            rng_points_multiplier=' and {digit}x from RNG'.format(digit=getattr(
                self, 'rng_points_multiplier')) if getattr(self, 'rng_points_multiplier', None) else '',
            owner=self.owner
        )


class Octs(__Roll):
    LENGTH = -8
    BASE_MULTIPLIER = 1
    BASE_VALUE = 1600

    def __init__(self, owner, timestamp, streak_multiplier=1):
        super(Octs, self).__init__(owner, timestamp, streak_multiplier)


class Septs(__Roll):
    LENGTH = -7
    BASE_MULTIPLIER = 1
    BASE_VALUE = 800

    def __init__(self, owner, timestamp, streak_multiplier=1):
        super(Septs, self).__init__(owner, timestamp, streak_multiplier)


class Sexts(__Roll):
    LENGTH = -6
    BASE_MULTIPLIER = 1
    BASE_VALUE = 400

    def __init__(self, owner, timestamp, streak_multiplier=1):
        super(Sexts, self).__init__(owner, timestamp, streak_multiplier)


class Quints(__Roll):
    LENGTH = -5
    BASE_MULTIPLIER = 1
    BASE_VALUE = 200

    def __init__(self, owner, timestamp, streak_multiplier=1):
        super(Quints, self).__init__(owner, timestamp, streak_multiplier)


class Quads(__Roll):
    LENGTH = -4
    BASE_MULTIPLIER = 1
    BASE_VALUE = 50

    def __init__(self, owner, timestamp, streak_multiplier=1):
        super(Quads, self).__init__(owner, timestamp, streak_multiplier)


class Trips(__Roll):
    LENGTH = -3
    BASE_MULTIPLIER = 1
    BASE_VALUE = 10

    def __init__(self, owner, timestamp, streak_multiplier=1):
        super(Trips, self).__init__(owner, timestamp, streak_multiplier)


class Dubs(__Roll):
    LENGTH = -2
    BASE_VALUE = 1
    BASE_MULTIPLIER = 1

    BAD_RNG_BASE_PERCENT = 5
    BAD_RNG_POINT_MULTIPLIER = -2
    BAD_RNG_MULTIPLIER_MODIFIER = -2

    GOOD_RNG_BASE_PERCENT = 5
    GOOD_RNG_POINT_MULTIPLIER = 2
    GOOD_RNG_MULTIPLIER_MODIFIER = 1

    def __init__(self, owner, timestamp, streak_multiplier=1):
        super(Dubs, self).__init__(owner, timestamp, streak_multiplier)

        rng = random.randint(1, 100)
        if rng <= min((streak_multiplier - 1) * Dubs.BAD_RNG_BASE_PERCENT, 50):
            self.rng_points_multiplier = Dubs.BAD_RNG_POINT_MULTIPLIER
            self.streak_multiplier += Dubs.BAD_RNG_MULTIPLIER_MODIFIER

            # hacky way to make sure the multiplier doesn't go below 1
            self.streak_multiplier = max(self.streak_multiplier, 1)
            raise BadRng(roll=self)

        elif rng > max(100 - (streak_multiplier - 1) * Dubs.GOOD_RNG_BASE_PERCENT, 50):
            self.rng_points_multiplier = Dubs.GOOD_RNG_POINT_MULTIPLIER
            self.streak_multiplier += Dubs.GOOD_RNG_MULTIPLIER_MODIFIER
            raise GoodRng(roll=self)


PRECEDENCE = [Octs, Septs, Sexts, Quints, Quads, Trips, Dubs]


def check(timestamp):
    """Check what the owner rolled.

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
    raise Invalid("that's not a roll, sorry")


def get_streak_multiplier(owner, last_roll):
    """Increment the streak multiplier based on the previous roll.

    Args:
        owner: (str) the name of the roll owner.
        last_roll: (__Roll.<roll_type>) the previous roll.

    Returns:
        (int) the roll value multiplier.
    """
    try:
        if last_roll.owner == owner:  # if it is a subsequent roll, increase the owner's multiplier
            return last_roll.streak_multiplier + last_roll.__class__.BASE_MULTIPLIER
        else:  # someone stole the multiplier from the previous owner
            return 1
    except AttributeError:
        return 1
