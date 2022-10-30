import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="!")

bot.run(config.token)
