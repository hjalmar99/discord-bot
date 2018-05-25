import discord
import asyncio
import logging
import os
import random
from random import randint
import re
from ordsprak import ordsprok_list as ord_list


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


if os.path.exists('.env'):
    logging.info('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


client = discord.Client()

@client.event
async def on_ready():
    logger.info('Logged in as {} ({}).'.format(client.user.name, client.user.id))

@client.event
async def on_message(message):
    if message.content == '!ping':
        await client.send_message(message.channel, 'Pong!')

    if message.content == '!mäng':
        await client.send_message(message.channel, 'Mong!')

    if message.content.startswith ('!ordspråk'):
        random.shuffle(ord_list)
        num = randint(1, len(ord_list))
        await client.send_message(message.channel, '{}'.format(ord_list[num - 1]))


    if message.content.startswith('!throw'):
        r = re.match('^!throw (?P<num>\d+) d(?P<sides>\d+)$', message.content)

        if r is not None:
            num, sides = int(r.group('num')), int(r.group('sides'))
            dice = [str(random.randint(1, sides)) for _ in range(num)]
            logger.debug('Threw {} d{} ({})'.format(num, sides, ', '.join(dice)))
            await client.send_message(message.channel, ', '.join(dice))
        else:
            await client.send_message(message.channel, 'Syntax is:\n!throw <number of dice> d<number of sides>')



client.run(os.environ.get('TOKEN'))
