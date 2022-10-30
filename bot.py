"""Discord bot for Unmity"""

import discord
from discord.ext import commands

from cogs import cmds

import config


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="!")

@bot.event
async def on_ready():
    """When the bot is connected to Discord and ready to start doing stuff"""
    await cmds.setup(bot)

bot.run(config.token)
