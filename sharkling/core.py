import os
import discord
import logging
from . import config

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=config.LOG_PATH, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class ROLL(object):
    Endings = [
        [-8, 'octs'],
        [-7, 'septs'],
        [-6, 'sexts'],
        [-5, 'quints'],
        [-4, 'quads'],
        [-3, 'trips'],
        [-2, 'dubs'],
    ]


class InvalidRoll(Exception):
    pass


def compute_roll(timestamp):
    for depth, roll_name in ROLL.Endings:
        if len(set(timestamp[depth:])) == 1:
            return roll_name
    raise InvalidRoll("{} is an invalid roll".format(timestamp))


def run():
    client = discord.Client()

    @client.event
    async def on_ready():
        logger.info('{} ({}) logged in!'.format(client.user.name, client.user.id))

    @client.event
    async def on_message(message):
        if message.content.startswith('!roll'):
            try:
                outcome = compute_roll(message.timestamp.strftime("%Y%m%d%H%M"))
            except InvalidRoll:
                outcome = '{} is an invalid roll, sorry.'.format(message.timestamp.replace(microsecond=0))
            await client.send_message(message.channel, outcome)

    client.run(os.environ['SHARKLING_TOKEN'])


if __name__ == '__main__':
    run()
