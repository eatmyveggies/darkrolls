import os
import discord
import logging
import asyncio
from . import config

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=config.LOG_PATH, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def run():
    client = discord.Client()

    @client.event
    async def on_ready():
        logger.info('{} ({}) logged in!'.format(client.user.name, client.user.id))

    @client.event
    async def on_message(message):
        if message.content.startswith('!test'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))

        elif message.content.startswith('!sleep'):
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping')

    client.run(os.environ['SHARKLING_TOKEN'])


if __name__ == '__main__':
    run()
