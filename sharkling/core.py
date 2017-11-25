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
            logger.info('{name} ({discord_id}) logged in!'.format(
                name=self.user.name, discord_id=self.user.id))

        @self.event
        async def on_message(message):
            if message.content.startswith('!rol'):
                message.timestamp = message.timestamp.replace(microsecond=0)
                logger.info('[attempt] roll from "{user}" at "{timestamp}"'.format(
                    user=message.author, timestamp=message.timestamp
                ))
                try:
                    # check if this roll has been rolled before
                    attempted_roll = message.timestamp.strftime("%Y%m%d%H%M")
                    if self.__last_roll and self.__last_roll.timestamp.strftime("%Y%m%d%H%M")[
                                            roll.PRECEDENCE[0].LENGTH:] == attempted_roll[roll.PRECEDENCE[0].LENGTH:]:
                        raise roll.InvalidRoll(
                            '**{author}** already rolled that one, you\'re too slow'.format(
                                author=self.__last_roll.author))

                    # check if it is a roll to begin with, and not a failed attempt
                    latest_roll = roll.check(attempted_roll)(
                        author=message.author, timestamp=message.timestamp,
                        streak_multiplier=roll.get_streak_multiplier(message.author, self.__last_roll)
                    )

                    # increment author's score
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

                except roll.InvalidRoll as e:
                    reply = '[failure] {error}'.format(message.timestamp, error=e.message)
                    logger.info(reply)

                await self.send_message(message.channel, reply)

            elif message.content.startswith('!score'):
                # build a table of the scores and a short line with who is the author of the last roll
                score = '```{table}\n\n{note}```'.format(table=tabulate.tabulate(
                    sorted(self.__scores.items(), key=lambda x: x[1], reverse=True), headers=['user', 'points']),
                    note='{streaker} is currently riding the {multiplier}x streak'.format(
                        streaker=self.__last_roll.author,
                        multiplier=self.__last_roll.streak_multiplier
                    ) if self.__last_roll else ''
                )
                await self.send_message(message.channel, score)

            elif message.content.startswith('!help'):
                help_message = '```{help_message}```'.format(help_message=tabulate.tabulate(
                    [
                        ('!roll', 'try your luck at a roll'),
                        ('!score', 'see the top rollers'),
                        ('!help', 'print this message')
                    ],
                    headers=['command', 'description']
                ))
                await self.send_message(message.channel, help_message)

        super(Sharkling, self).run(os.environ[config.DISCORD_TOKEN_ENV])


if __name__ == '__main__':
    Sharkling().run()
