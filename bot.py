"""Discord bot for Unmity"""

# To get environment variables for checking if testing mode
from os import environ

import discord
from discord.ext import commands

from cogs import cmds, logs

import config


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# For testing, use a different prefix for commands
testing_mode = environ.get("UNMITY_TESTING")
if testing_mode:
    command_prefix="?!"
    print("[Bot] Testing Mode")
else:
    command_prefix="!"

bot = commands.Bot(intents=intents, command_prefix=command_prefix)


@bot.event
async def on_ready():
    """When the bot is connected to Discord and ready to start doing stuff"""
    await cmds.setup(bot)
    await logs.setup(bot)
    print(f"[Bot] Connected as {bot.user}")


@bot.command(hidden=True)
@commands.is_owner()
async def sync_commands(ctx):
    """Synchronize slash commands to the Unmity server"""
    bot.tree.copy_global_to(guild=discord.Object(id=1036052928806518824))
    await bot.tree.sync(guild=discord.Object(id=1036052928806518824))
    await ctx.send("Commands synced!")
    print(f"[Bot] Commands synced by {ctx.author}")

bot.run(config.token)
