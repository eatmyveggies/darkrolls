import random
import functools
from . import config


class Invalid(Exception):
    pass

class DoubleRoll(Exception):
    def __init__(self, encounter):
        self.encounter = encounter

class InvalidRoll(Invalid):
    pass


class InvalidInvasion(Invalid):
    pass


class Outcome(object):
    def __init__(self, timestamp, message, cards, reward):
        self.__timestamp = timestamp
        self.__message = message
        self.__cards = cards
        self.__reward = reward


class Success(Outcome):
    def __init__(self, timestamp, message, reward, cards=None):
        super().__init__(timestamp, message, reward, cards)


class Failure(Outcome):
    def __init__(self, timestamp, message, reward=0, cards=None):
        super().__init__(timestamp, message, reward, cards)


class Nothing(Outcome):
    def __init__(self, timestamp, message, reward=0, cards=None):
        super().__init__(timestamp, message, reward, cards)


class __Roll(object):
    def __init__(self, undead, timestamp):
        self.undead = undead
        self.timestamp = timestamp

    @property
    def name(self):
        return self.__class__.__name__.lower()

    def combat(self, campaign):
        cards = list()
        if self.timestamp in campaign.encounters:
            if self.undead.weapon.overroll:
                if campaign.encounters[self.timestamp].undead.name != self.undead.name:
                    if getattr(self.undead.weapon.overroll.specific, self.name):
                        cards.append('agile')
                        if getattr(self.undead.weapon.overroll.durability.loss_rate.specific, self.name):
                            cards.append('fragile')
                        else:
                            # no extra durability is lost for this specific double roll
                            pass
                    else:
                        raise DoubleRoll(encounter=campaign.encounters[self.timestamp])
                else:
                    raise DoubleRoll(encounter=campaign.encounters[self.timestamp])
            else:
                raise DoubleRoll(encounter=campaign.encounters[self.timestamp])

        if self.undead.weapon.multiplier.successive != 1 or self.undead.weapon.multiplier.different != 1:
            if self.undead.last_successful_encounter:
                if self.undead.last_successful_encounter.outcome.roll.name != self.name:
                    if self.undead.weapon.multiplier.different > 1:
                        cards.append('versatile')
                    else:
                        cards.append('straining moves')
                else:
                    if self.undead.weapon.multiplier.successive > 1:
                        cards.append('momentum')
                    else:
                        cards.append('losing balance')
            else:
                print(self.undead, "doesnt have a last successful encounter")
        else:
            print(self.undead, "doesnt have benefit from successive/different rolls")


        if self.undead.weapon.soul_linked:
            cards.append('two-edged')

        if getattr(self.undead.weapon.evolve.specific, self.name):
            cards.append('evolve')

        if getattr(self.undead.weapon.devolve.specific, self.name):
            cards.append('devolve')


        # does weapon get extra multiplier for specific rolls?

        # does weapon get extra durability loss from specific rolls?

        # does weapon have a crit chance?

        # does weapon multiplier benefit from this roll?

        # does weapon have a chance to fail certain rolls?

        # does weapon have a chance to upgrade to successor?

        # does weapon have chance to steal souls?

        # does weapon have chance to burn souls?

        # does weapon roll next chronological rolls?
        pass


class Octs(__Roll):
    def __init__(self, undead, timestamp):
        super(Octs, self).__init__(undead, timestamp)


class Septs(__Roll):
    def __init__(self, undead, timestamp):
        super(Septs, self).__init__(undead, timestamp)


class Sexts(__Roll):
    def __init__(self, undead, timestamp):
        super(Sexts, self).__init__(undead, timestamp)


class Quints(__Roll):
    def __init__(self, undead, timestamp):
        super(Quints, self).__init__(undead, timestamp)


class Quads(__Roll):
    def __init__(self, undead, timestamp):
        super(Quads, self).__init__(undead, timestamp)


class Trips(__Roll):
    def __init__(self, undead, timestamp):
        super(Trips, self).__init__(undead, timestamp)


class Dubs(__Roll):
    def __init__(self, undead, timestamp):
        super(Dubs, self).__init__(undead, timestamp)


def resolve(timestamp):
    for roll_type in [Octs, Septs, Sexts, Quints, Quads, Trips, Dubs]:
        if len(set(timestamp[config.options['roll'][roll_type.__name__.lower()]['length']:])) == 1:
            return functools.partial(roll_type, timestamp=timestamp)
    raise Invalid()


def invasion(timestamp, undead, campaign):
    pass
