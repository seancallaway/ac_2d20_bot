#!/usr/bin/env python3
from logging import getLogger
from os import environ

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

bot.run(bot_token)
