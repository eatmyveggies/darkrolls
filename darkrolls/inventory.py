class Broken(Exception):
    pass


class LevelError(Exception):
    pass


class MaxUpgrade(LevelError):
    pass


class NotEnoughSouls(LevelError):
    pass


class SuccessfulUpgrade(LevelError):
    def __init__(self, souls):
        self.souls = souls


class Weapon(object):
    def __init__(self, level=0, **kwargs):
        self.__attributes = kwargs
        self.__level = level

    def __getattribute__(self, item):
        if item in self.__attributes:
            return self.__attributes[item]
        else:
            return getattr(self, item)

    @property
    def durability(self):
        if getattr(self, '__durability'):
            return self.__durability
        else:
            self.__durability = self.__attributes['max_durability']
            return self.__durability

    @property
    def level(self):
        return self.__level

    def degrade(self, amount):
        if self.durability:
            self.__durability = max(self.__durability - amount, 0)
        else:
            raise Broken('{} has no durability left'.format(self))

    def __str__(self):
        return self.__name

    def level_up(self, souls):
        if self.level < self.__attributes['max_level']:
            self.__level += 1
        else:
            raise MaxUpgrade('{} has hit maximum level of upgrade'.format(self))


class Unarmed(Weapon):
    def __init__(self):
        super().__init__( **{
            'name': 'hands',
            'max_durability': 10,
            'attack': 1,
            'max_level': 1
        })
