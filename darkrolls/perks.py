class __Perk(object):
    def __init__(self):
        pass

    def apply(self):
        raise Exception('implement me')


class Versatile(__Perk):
    def __init__(self, ):
        super(Versatile, self).__init__()
