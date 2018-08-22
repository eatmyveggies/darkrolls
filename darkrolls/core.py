import os
import discord
import logging
import tabulate
import datetime
import threading
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
                undead = self.__campaign.find(name=message.content.nick)
                timestamp = backend.localize(message.timestamp)
                logger.info('[attempt] roll from "{undead}" at "{timestamp}"'.format(
                    undead=undead.name, timestamp=timestamp))
                self.__campaign.encounters.append(game.Encounter(undead, timestamp, self.__campaign))


            elif message.content.startswith('!rest'):
                pass

            elif message.content.startswith('!invade'):
                pass

            elif message.content.startswith('!loot'):
                pass

            elif message.content.startswith('!help'):

                await self.send_message(
                    message.channel,
                    '```{}```'.format(tabulate.tabulate(
                        [
                            ('!roll', 'roll for souls'),
                            ('!loot', 'search your surroundings for loot'),
                            ('!rest', 'cosy up to the warm bonfire, repair your weapon and introspect'),
                            ('!invade', 'invade the world of another undead'),
                            ('!help', 'Lordran can be unforgiving')
                        ],
                        headers=['command', 'description'])))

        super(DarkRolls, self).run(os.environ[config.options['credentials']['token_env']])


if __name__ == '__main__':
    DarkRolls().run()
