import discord
import traceback
import io
import textwrap
import aiohttp
import subprocess
import re
import rethinkdb as r

from discord.ext import commands
from config import webhooks, prefixes
from contextlib import redirect_stdout
from .utils.chat_formatting import pagify, box


class Developer:

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith("```") and content.endswith("```"):
            return '\n'.join(content.split("\n")[1:-1])
        return content.strip("` \n")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(f"modules.{module}")
        except Exception:
            for page in pagify(traceback.format_exc()):
                await ctx.send(box(text=page, lang="py"))
        else:
            await ctx.send(f"Loaded module: {module}"
                           .replace("modules.", ""))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module):
        """Unload a module."""
        try:
            self.bot.unload_extension(f"modules.{module}")
        except Exception:
            for page in pagify(traceback.format_exc()):
                await ctx.send(box(text=page, lang="py"))
        else:
            await ctx.send(f"Unloaded module: {module}"
                           .replace("modules.", ""))

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, module):
        """Reload a module."""
        try:
            self.bot.unload_extension(f"modules.{module}")
            self.bot.load_extension(f"modules.{module}")
        except Exception:
            for page in pagify(traceback.format_exc()):
                await ctx.send(box(text=page, lang="py"))
        else:
            await ctx.send(f"Reloaded module: {module}"
                           .replace("modules.", ""))

    @commands.command(hidden=True, aliases=["off", "shutoff"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot."""
        await ctx.send("Shutting off...")
        await self.bot.close()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def speedtest(self, ctx):
        """Return the vps' speedtest results"""
        await ctx.trigger_typing()

        data = subprocess.getoutput("speedtest --share --simple")
        data = re.search("(?P<url>https?://[^\s]+)", str(data)).group("url")
        embed = discord.Embed(colour=3553599)
        embed.set_image(url=data)

        await ctx.send(embed=embed)

    @commands.command(name="eval", hidden=True, aliases=["ev"])
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
        """Evaluate Python Code."""
        env = {
            'self': self,
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
            'r': r,
            'r_conn': self.bot.r_conn
        }

        env.update(globals())
        code = self.cleanup_code(code)
        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(code, " ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'`{e.__class__.__name__}`\n```py\n{e}\n```')

        func = env['func']

        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(hidden=True, aliases=["tc"])
    @commands.is_owner()
    async def traceback(self, ctx, public: bool=False):
        """
        Sends the last command exception.

            public: default False
        """
        if not public:
            destination = ctx.author
        else:
            destination = ctx.channel

        if self.bot._last_exception:
            for page in pagify(self.bot._last_exception):
                await destination.send(box(text=page, lang="py"))
        else:
            await ctx.send("No exception has yet to occur.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def force(self, ctx, user: discord.Member, *, command):
        """Forces a user to run the specified command."""
        message = ctx.message
        message.author = user
        message.content = f"{prefixes[0]}{''.join(command)}"

        await self.bot.process_commands(message)
        await ctx.message.add_reaction(u"\U0001F44C")

    async def on_guild_join(self, guild):
        embed = discord.Embed(colour=3553599, title="Guild Joined")
        embed.add_field(
            name="Name:",
            value="",
            inline=True
        )
        embed.add_field(
            name="Members:",
            value="",
            inline=True
        )
        embed.add_field(
            name="Owner:",
            value=f"{guild.owner.name}#{guild.owner.discriminator} ({guild.owner.id})",
            inline=True
        )
        try:
            embed.set_thumbnail(url=guild.icon_url)
        except: pass
        async with aiohttp.ClientSession() as cs:
            webhook = discord.Webhook.from_url(
                url=webhooks["guildjoin"],
                adapter=discord.AsyncWebhookAdapter(cs)
            )
            await webhook.send(embed=embed)

    async def on_guild_remove(self, guild):
        embed = discord.Embed(colour=3553599, title="Guild Left")
        embed.add_field(
            name="Name:",
            value="",
            inline=True
        )
        embed.add_field(
            name="Members:",
            value="",
            inline=True
        )
        embed.add_field(
            name="Owner:",
            value=f"{guild.owner.name}#{guild.owner.discriminator} ({guild.owner.id})",
            inline=True
        )
        try:
            embed.set_thumbnail(url=guild.icon_url)
        except: pass
        async with aiohttp.ClientSession() as cs:
            webhook = discord.Webhook.from_url(
                url=webhooks["guildleave"],
                adapter=discord.AsyncWebhookAdapter(cs)
            )
            await webhook.send(embed=embed)


def setup(bot):
    bot.add_cog(
        Developer(bot)
    )
