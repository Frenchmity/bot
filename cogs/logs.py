from discord.ext import commands
import discord

class Logs(commands.Cog):
    """Logs for everything"""

    def __init__(self, bot):
        self.bot = bot
        self.command_logging_channel = 1036077455108218921

    @commands.Cog.listener()
    async def on_command(self, ctx):
        embed = discord.Embed(title="Text Command", url=ctx.message.jump_url, description=ctx.message.content).set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url).add_field(name="Channel", value=ctx.channel.mention)
        await self.bot.get_channel(self.command_logging_channel).send(embed=embed)

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction, command):
        if interaction.type != discord.InteractionType.application_command:
            return
        command_name = f"</{command.qualified_name}:{interaction.id}> " + " ".join([f"{name}={value}" for name, value in tuple(interaction.namespace)])
        embed = discord.Embed(title="Slash Command", description=command_name).set_author(name=str(interaction.user), icon_url=interaction.user.display_avatar.url).add_field(name="Channel", value=interaction.channel.mention)
        await self.bot.get_channel(self.command_logging_channel).send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))
