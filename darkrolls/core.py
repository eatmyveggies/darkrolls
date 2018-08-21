import os
import discord
import logging
import tabulate
import datetime
from . import config
from . import backend
from . import game

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter(config.options['logging']['format']))
handler = logging.FileHandler(filename=config.options['logging']['path'], encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter(config.options['logging']['format']))
logger.addHandler(handler)
logger.addHandler(console)


class DarkRolls(discord.Client):
    def __init__(self):
        super(DarkRolls, self).__init__()
        self.__campaign = backend.recover(config.options['db']['path'])

    def run(self):
        @self.event
        async def on_ready():
            logger.info('{name} ({discord_id}) logged in!'.format(
                name=self.user.name, discord_id=self.user.id))
            logger.info('Current campaign started {delta} ago.'.format(
                delta=datetime.datetime.now() - self.__campaign.start))

        @self.event
        async def on_message(message):
            if message.content.lower().startswith('!rol'):
                undead = self.__campaign.get_undead(name=message.content.nick)
                timestamp = backend.localize(message.timestamp)
                logger.info('[attempt] roll from "{undead}" at "{timestamp}"'.format(
                    undead=undead.name, timestamp=timestamp))
                encounter = game.Encounter(undead, timestamp)


            elif message.content.startswith('!weapon'):
                pass

            elif message.content.startswith('!help'):

                await self.send_message(
                    message.channel,
                    '```{}```'.format(tabulate.tabulate(
                        [
                            ('!roll', 'try your luck at a roll'),
                            ('!help', 'print this message')
                        ],
                        headers=['command', 'description'])))

        super(DarkRolls, self).run(os.environ[config.options['credentials']['token_env']])


if __name__ == '__main__':
    DarkRolls().run()
