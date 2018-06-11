DISCORD_TOKEN_ENV = 'SHARKLING_TOKEN'  # environment variable to check for API token
LOG_FMT = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
LOG_PATH = '/var/log/sharkling/discord.log'
SCORE_DATA_PATH = '/var/data/sharkling/rolls.pickle'  # path to serialize score of players
ROLL_COOLDOWN = 60  # seconds to wait between consecutive rolls
