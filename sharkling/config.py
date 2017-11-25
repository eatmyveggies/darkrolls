LOG_PATH = '/tmp/discord.log'
LOG_FMT = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
DISCORD_TOKEN_ENV = 'SHARKLING_TOKEN'  # environment variable to check for API token


class BaseRollValues(object):
    Dubs = 1
    Trips = 10
    Quads = 50
    Quints = 200
    Sexts = 400
    Septs = 800
    Octs = 1600
