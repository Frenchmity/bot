from asyncio import subprocess
from contextlib import redirect_stdout
import io, textwrap, traceback

from discord.ext import commands
import discord


class Admin(commands.Cog):
    """Administration of the Bot"""

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

    @commands.command()
    @commands.is_owner()
    async def upgrade(self, ctx, pm_id: int = 3):
        """Upgrade the bot"""
        gitpull = await subprocess.create_subprocess_shell("git pull --quiet")
        await gitpull.communicate()
        if gitpull.returncode != 0:  # 0 means successful
            return await ctx.send("`git pull` was unsuccessful.")
        await ctx.send("`git pull` was successful.")
        pipupgrade = await subprocess.create_subprocess_shell(
            "pip install --quiet --upgrade -r requirements.txt"
        )
        await pipupgrade.communicate()
        if gitpull.returncode != 0:  # 0 means successful
            return await ctx.send("`pip` was unsuccessful.")
        await ctx.send("`pip` was successful. Restarting...")
        await self.bot.close()
        await subprocess.create_subprocess.shell(f"pm2 restart {pm_id}")

    @commands.command()
    @commands.is_owner()
    async def sync_commands(self, ctx):
        """Synchronize slash commands to the Unmity server"""
        self.bot.tree.copy_global_to(guild=discord.Object(id=1036052928806518824))
        await self.bot.tree.sync(guild=discord.Object(id=1036052928806518824))
        await ctx.send("Commands synced!")
        print(f"[Bot] Commands synced by {ctx.author}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
    print("[Admin] Loaded")
