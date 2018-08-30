import os
import signal
import logging
import discord
import tabulate
import datetime
import functools
import traceback
from . import game
from . import config
from . import backend

backend.setup_logger(
    name=config.options['logging']['name'],
    format=config.options['logging']['format'],
    path=config.options['logging']['path'])
log = logging.getLogger(__name__)


class DarkRolls(discord.Client):
    def __init__(self, gms):
        super(DarkRolls, self).__init__()
        signal.signal(signal.SIGINT, functools.partial(backend.on_exit, game=self))
        self.__gms = gms
        self.__campaign = backend.recover(config.options['db']['campaign'])

    def save(self):
        backend.save(self.__campaign, config.options['db']['campaign'])

    def run(self):
        @self.event
        async def on_ready():
            print("ready")
            log.info('{name} ({discord_id}) logged in!'.format(
                name=self.user.name, discord_id=self.user.id))
            log.info('Current campaign started {delta} ago.'.format(
                delta=datetime.datetime.now() - self.__campaign.start))

        @self.event
        async def on_message(message):
            if message.content.lower().startswith('!rol'):
                undead = self.__campaign.find(undead=message.author)
                timestamp = backend.localize(message.timestamp)
                log.info('roll attempt from "{undead}" at "{timestamp}"'.format(
                    undead=undead.name, timestamp=timestamp))
                self.__campaign.encounters.append(game.Encounter(undead, timestamp, self.__campaign))

            elif message.content.startswith('!rest'):
                raise Exception('not implemented')

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
                            ('!loot', 'search your surroundings'),
                            ('!rest', 'cosy up to the warm bonfire'),
                            ('!invade', 'invade the world of another undead'),
                            ('!help', 'Lordran can be unforgiving')
                        ],
                        headers=['command', 'description'])))

            elif message.content.startswith('!give'):
                if message.author.id in self.__gms:
                    try:
                        weapon_name = message.content.split(" ")[1]
                    except KeyError:
                        pass
                    else:
                        embed = discord.Embed(title="Tile", description="Desc", color=0x00ff00)
                        embed.add_field(name="Field1", value="hi", inline=False)
                        embed.add_field(name="Field2", value="hi2", inline=False)
                        await self.send_message(
                            message.channel, '{} is a GM.'.format(message.author), embed=embed)

        @self.event
        async def on_error(event, *args, **kwargs):
            log.error(traceback.format_exc())
            self.save()
            log.info("logging out")
            await self.logout()

        super(DarkRolls, self).run(os.environ[config.options['credentials']['token_env']])
