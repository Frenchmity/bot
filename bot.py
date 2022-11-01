"""Discord bot for Unmity"""

# To get environment variables for checking if testing mode
from os import environ

import discord
from discord.ext import commands

import config


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# For testing, use a different prefix for commands
testing_mode = environ.get("UNMITY_TESTING")
if testing_mode:
    command_prefix = "?!"
    print("[Bot] Testing Mode")
else:
    command_prefix = "!"

bot = commands.Bot(intents=intents, command_prefix=command_prefix)


@bot.event
async def setup_hook():
    """Load all the cogs"""
    cogs = ["cmds", "logs", "admin"]
    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
        except Exception as exc:
            print(
                f"Could not load extension {cog} due to {exc.__class__.__name__}: {exc}"
            )


@bot.event
async def on_ready():
    print(f"[Bot] Connected as {bot.user}")


bot.run(config.token)
