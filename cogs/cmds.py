from discord.ext import commands
import discord


class Cmds(commands.Cog):
    """The bot's slash commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)
    @discord.app_commands.describe(enable="To enable/disable invites for this server")
    async def invites(self, ctx, enable: bool):
        """Enable or Disable Invites"""
        await ctx.guild.edit(invites_disabled=not enable)
        ed = "En" if enable else "Dis"
        await ctx.send(f"{ed}abled invites", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Cmds(bot))
    print("[Commands] Loaded")
