#!/usr/bin/env python3
from logging import getLogger
from os import environ
from random import randint

from discord import Intents
from discord.ext import commands

logger = getLogger(__name__)

# Environment variables and other customizable stuff
bot_token = environ.get('BOT_TOKEN', None)
bot_prefix = environ.get('BOT_PREFIX', '!')

intents = Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix=bot_prefix, intents=intents)


@bot.event
async def on_ready():
    logger.debug('Bot is ready!')


@bot.command()
async def hello(ctx):
    await ctx.send('Hi there!')


@bot.command()
async def test(ctx, pool: int, target: int):
    if pool < 2 or pool > 5:
        await ctx.send('[ERROR] Dice pool should be between 2 and 5.')
        return
    elif target < 1 or target > 20:
        await ctx.send('[ERROR] Target must be between 1 and 20.')
        return

    results = []
    successes = 0
    complications = 0

    for _ in range(pool):
        result = randint(1, 20)
        if result == 1:
            successes += 2
        elif result <= target:
            successes += 1
        elif result == 20:
            complications += 1
        results.append(str(result))

    await ctx.send(f'{successes} successes. {complications} complications. [{", ".join(results)}]')


@bot.command()
async def challenge(ctx, count: int = 1):
    total = 0
    effects = 0
    results = []
    for _ in range(count):
        roll = randint(1, 6)
        if roll > 4:
            total += 1
            effects += 1
            results.append('1 + effect')
        elif roll in (3, 4):
            results.append('0')
        else:
            total += roll
            results.append(str(roll))

    await ctx.send(f'{total} with {effects} effects [{", ".join(results)}]')


@bot.command()
async def roll(ctx, dice: str):
    """Roll die in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(randint(1, limit)) for _ in range(rolls))
    await ctx.send(result)

bot.run(bot_token)
