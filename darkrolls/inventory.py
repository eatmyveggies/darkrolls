class Broken(Exception):
    pass


class LevelError(Exception):
    pass


class MaxUpgrade(LevelError):
    pass


class __Weapon(object):
    def __init__(self, name, **kwargs):
        self.__name = name
        self.__attributes = kwargs

    @property
    def durability(self):
        if getattr(self, '__durability'):
            return self.__durability
        else:
            self.__durability = self.__attributes['max_durability']
            return self.__durability

    @property
    def level(self):
        if getattr(self, '__level'):
            return self.__level
        else:
            self.__level = 1
            return self.__level

    def degrade(self, amount):
        if self.durability:
            self.__durability = max(self.__durability - amount, 0)
        else:
            raise Broken('{} has no durability left'.format(self))

    def __str__(self):
        return self.__name

    def upgrade(self):
        if self.level < self.__attributes['max_level']:
            self.__level += 1
        else:
            raise MaxUpgrade('{} has hit maximum level of upgrade'.format(self))


class Unarmed(__Weapon):
    def __init__(self):
        super().__init__('hands', **{
            'max_durability': 10,
            'attack': 1,
            'max_level': 1
        })
