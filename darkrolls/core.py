import os
import discord
import tabulate
import datetime
from . import game
from . import config
from . import backend


class DarkRolls(discord.Client):
    def __init__(self, gms):
        super(DarkRolls, self).__init__()
        self.__logger = backend.get_logger(
            name=config.options['logging']['name'],
            format=config.options['logging']['format'],
            path=config.options['logging']['path'])
        self.__gms = gms
        self.__campaign = backend.recover(config.options['db']['campaign'])

    @property
    def log(self):
        return self.__logger

    def run(self):
        @self.event
        async def on_ready():
            self.log.info('{name} ({discord_id}) logged in!'.format(
                name=self.user.name, discord_id=self.user.id))
            self.log.info('Current campaign started {delta} ago.'.format(
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
                            ('!loot', 'search your surroundings for valuables'),
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

        super(DarkRolls, self).run(os.environ[config.options['credentials']['token_env']])
