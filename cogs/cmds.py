from contextlib import redirect_stdout
import io, textwrap, traceback, typing

from discord.ext import commands
import discord


class Cmds(commands.Cog):
    """The bot's slash commands"""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def cleanup_code(self, content: str) -> str:
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])

        # remove `foo`
        return content.strip("` \n")

    @commands.hybrid_command()
    @commands.has_permissions(manage_guild=True)
    @discord.app_commands.describe(enable="To enable/disable invites for this server")
    async def invites(self, ctx, enable: bool):
        """Enable or Disable Invites"""
        await ctx.guild.edit(invites_disabled=not enable)
        ed = "En" if enable else "Dis"
        await ctx.send(f"{ed}abled invites", ephemeral=True)

    @commands.hybrid_command(hidden=True, name="eval")
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("\u2705")
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f"```py\n{value}\n```")
            else:
                self._last_result = ret
                await ctx.send(f"```py\n{value}{ret}\n```")


async def setup(bot):
    await bot.add_cog(Cmds(bot))
    print("[Commands] Loaded")
