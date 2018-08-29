import datetime
from . import config
from . import inventory


class NoWeapon(Exception):
    pass


class Sheet(object):
    def __init__(self):
        self.level = 0
        self.souls = 0
        self.humanity = 0
        self.resting = None

    def level_up(self):
        while True:
            if self.souls >= levels[self.level + 1]:
                self.level += 1
                self.souls -= levels[self.level + 1]
            else:
                raise inventory.NotEnoughSouls()


class Undead(object):
    def __init__(self, name):
        self.__name = name
        self.__sheet = Sheet()

    @property
    def name(self):
        return self.__name

    @property
    def weapon(self):
        if getattr(self, '__weapon'):
            return self.__weapon
        else:
            self.__weapon = inventory.Weapon(level=0, **config.weapons['unarmed'])
            return self.__weapon

    def rest(self):
        self.resting = datetime.datetime.now() + datetime.timedelta(hours=6 * self.weapon.resting_coef)
        try:
            self.__weapon.level_up(self.__sheet.souls)
        except inventory.MaxUpgrade:
            pass
        except inventory.NotEnoughSouls:
            pass
        except inventory.SuccessfulUpgrade as success:
            self.__sheet.souls -= success.souls

        try:
            self.__sheet.level_up()
        except inventory.NotEnoughSouls:
            pass
