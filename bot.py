"""Discord bot for Unmity"""

import discord
from discord.ext import commands

from cogs import cmds, logs

import config


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="!")


@bot.event
async def on_ready():
    """When the bot is connected to Discord and ready to start doing stuff"""
    await cmds.setup(bot)
    await logs.setup(bot)
    print(f"Connected as {bot.user}")


@bot.command()
@commands.is_owner()
async def sync_commands(ctx):
    """Synchronize slash commands to the Unmity server"""
    bot.tree.copy_global_to(guild=discord.Object(id=1036052928806518824))
    await bot.tree.sync(guild=discord.Object(id=1036052928806518824))
    await ctx.send("Commands synced!")


bot.run(config.token)
