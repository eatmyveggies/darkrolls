from . import inventory

class NoWeapon(Exception):
    pass

class Undead(object):
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def weapon(self):
        if getattr(self, '__weapon'):
            return self.__weapon
        else:
            self.__weapon = inventory.Unarmed()
            return self.__weapon
