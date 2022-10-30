from discord.ext import commands
import discord

class Cmds(commands.Cog):
    """The description for Commands goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def hello(self, ctx):
        """Testing commands"""
        await ctx.send("Hello, world!")

async def setup(bot):
    await bot.add_cog(Cmds(bot))
