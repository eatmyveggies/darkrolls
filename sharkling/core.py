import os
import discord
import logging
import tabulate
from . import roll
from . import config

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter(config.LOG_FMT))
handler = logging.FileHandler(filename=config.LOG_PATH, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(config.LOG_FMT))
logger.addHandler(handler)
logger.addHandler(console)


class Sharkling(discord.Client):
    def __init__(self):
        super(Sharkling, self).__init__()
        self.__last_roll = None
        self.__scores = dict()

    def run(self):
        @self.event
        async def on_ready():
            logger.info('{} ({}) logged in!'.format(self.user.name, self.user.id))

        @self.event
        async def on_message(message):
            if message.content.startswith('!rol'):
                message.timestamp = message.timestamp.replace(microsecond=0)
                logger.info('[attempt] roll from "{user}" at "{timestamp}"'.format(
                    user=message.author, timestamp=message.timestamp
                ))
                try:
                    latest_roll = roll.check(message.timestamp.strftime("%Y%m%d%H%M"))(
                        roller=message.author, timestamp=message.timestamp,
                        streak_multiplier=roll.get_streak_multiplier(message.author, self.__last_roll)
                    )

                    try:
                        self.__scores[message.author] += latest_roll.points
                    except KeyError:
                        self.__scores[message.author] = latest_roll.points
                    finally:
                        self.__last_roll = latest_roll

                    reply = '{reply}. **{author}** now has {total} point{plural}.'.format(
                        reply=latest_roll, author=message.author, total=self.__scores[message.author],
                        plural='s' if self.__scores[message.author] > 1 else '')
                    logger.info('[success] {reply}'.format(reply=reply))

                except roll.InvalidRoll:
                    reply = '[failure] {} is an invalid roll, sorry'.format(message.timestamp)
                    logger.info(reply)

                await self.send_message(message.channel, reply)

            elif message.content.startswith('!score'):
                score = '```{table}```\n'.format(table=tabulate.tabulate(
                    sorted(self.__scores.items(), key=lambda x: x[1], reverse=True), headers=['user', 'points'])
                )
                await self.send_message(message.channel, score)

        super(Sharkling, self).run(os.environ[config.DISCORD_TOKEN_ENV])


if __name__ == '__main__':
    Sharkling().run()
