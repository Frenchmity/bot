from datetime import datetime, timezone

from discord.ext import commands
import discord


class Logs(commands.Cog):
    """Logs for everything"""

    def __init__(self, bot):
        self.bot = bot
        self.command_logging_channel = 1036077455108218921
        self.logging_channel = 1036059407332675705

    def date(self):
        """Get the current datetime"""
        return datetime.now(timezone.utc)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        embed = (
            discord.Embed(
                title="Text Command",
                url=ctx.message.jump_url,
                description=ctx.message.content,
            )
            .set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
            .add_field(name="Channel", value=ctx.channel.mention)
        )
        await self.bot.get_channel(self.command_logging_channel).send(embed=embed)

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction, command):
        if interaction.type != discord.InteractionType.application_command:
            return
        command_name = f"</{command.qualified_name}:{interaction.id}> " + " ".join(
            [f"{name}={value}" for name, value in tuple(interaction.namespace)]
        )
        embed = (
            discord.Embed(title="Slash Command", description=command_name)
            .set_author(
                name=str(interaction.user), icon_url=interaction.user.display_avatar.url
            )
            .add_field(name="Channel", value=interaction.channel.mention)
        )
        await self.bot.get_channel(self.command_logging_channel).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        info = ""
        modlogs = self.bot.get_channel(self.logging_channel)
        try:
            async for entry in member.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.kick
            ):
                if member.id == entry.target.id:
                    info = f"{entry.user.mention} ({entry.user}) kicked {entry.target}"
                    if entry.reason:
                        info += f"\nReason: `{entry.reason}`"
        except discord.errors.Forbidden:
            info = ""
        if info:
            info = f"Info: {info}"
        timestay = "<t:" + str(int(member.joined_at.timestamp()))
        msg = discord.Embed(
            description=f"`{member}` just left the server.\n\nThey joined your server {timestay}:R>, on {timestay}>.\n\n{info}",
            timestamp=self.date(),
        ).set_footer(
            text=f"User ID: {member.id}",
            icon_url=member.avatar.url if member.avatar else None,
        )
        await modlogs.send(embed=msg)
        await self.bot.get_channel(1036325466954551316).edit(
            name=f"Members: {len(member.guild.members)}"
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            event = [
                i
                async for i in await member.guild.audit_logs(
                    limit=1, action=discord.AuditLogAction.bot_add
                )
            ][0]
            inviter = event[0].user
        else:
            inviter = None
        embd = discord.Embed(
            description=f"{member.mention} (`{member}`) just joined the server!",
            timestamp=self.date(),
        ).set_footer(
            text=f"User ID: {member.id}",
            icon_url=member.avatar.url if member.avatar else None,
        )
        if inviter:
            embd.add_field(
                name="Invited by",
                value=f"{inviter.mention if inviter else 'Unknown'} ({inviter})",
            )
        embd.add_field(
            name="Info",
            value=f"Account created at: <t:{int(member.created_at.timestamp())}>",
        )
        modlogs = self.bot.get_channel(self.logging_channel)
        await modlogs.send(embed=embd)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        log = [
            i
            async for i in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban)
        ][0]
        reason = ""
        if log.reason:
            reason = f"\nReason: {log.reason}"
        msg = discord.Embed(
            title="Banned",
            description=f"{user} was just banned by {log.user.mention} ({log.user.id}).{reason}",
            timestamp=self.date(),
        )
        modlogs = self.bot.get_channel(self.logging_channel)
        await modlogs.send(embed=msg)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log = [
            i
            async for i in guild.audit_logs(
                limit=1, action=discord.AuditLogAction.unban
            )
        ][0]
        reason = ""
        if log.reason:
            reason = f"\nReason: {log.reason}"
        msg = discord.Embed(
            title="Unbanned",
            description=f"{user} was just unbanned by {log.user.mention} ({log.user.id}).{reason}",
            timestamp=self.date(),
        )
        modlogs = self.bot.get_channel(self.logging_channel)
        await modlogs.send(embed=msg)


async def setup(bot):
    await bot.add_cog(Logs(bot))
    print("[Logs] Loaded")
