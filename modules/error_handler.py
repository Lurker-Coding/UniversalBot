"""Need to completely rewrite this"""

import discord
import aiohttp
import traceback

from discord.ext import commands
from config import webhooks


class ErrorHandler:

    def __init__(self, bot):
        self.bot = bot

    async def send_cmd_help(self, ctx):
        if ctx.invoked_subcommand:
            pages = await self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await ctx.send(page)
        else:
            pages = await self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await ctx.send(page)

    async def on_command_error(self, ctx, exception):
        error = getattr(exception, "original", exception)

        if isinstance(error, discord.NotFound):
            return
        elif isinstance(error, discord.Forbidden):
            return
        elif isinstance(error, discord.HTTPException) or isinstance(error, aiohttp.ClientConnectionError):
            log = f"HTTPException or ClientConnectionError in command {ctx.command.qualified_name}\n"
            log += "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            self.bot._last_exception = log

            async with aiohttp.ClientSession() as cs:
                webhook = discord.Webhook.from_url(
                    url=webhooks["error"],
                    adapter=discord.AsyncWebhookAdapter(cs)
                )
                embed = discord.Embed(colour=discord.Colour.red())
                embed.title = f"Error in command {ctx.command.qualified_name}"
                embed.description = "HTTPException"

                await webhook.send(embed=embed)
        if isinstance(exception, commands.NoPrivateMessage):
            return
        elif isinstance(exception, commands.DisabledCommand):
            await ctx.send(f"{ctx.command.qualified_name} is currently disabled. Please try again at a later time.")
        elif isinstance(exception, commands.CommandInvokeError):
            log = f"HTTPException or ClientConnectionError in command {ctx.command.qualified_name}\n"
            log += "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            self.bot._last_exception = log

            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f"Error in command: **{ctx.command.qualified_name}**",
                url="https://discord.gg/mqzcMca",
                description=f"If this error continues please tell the developers in the [Support Server](https://discord.gg/mqzcMca)."
                f"\n```py\n{exception}\n```"
            )
            await ctx.send(embed=embed)

            async with aiohttp.ClientSession() as cs:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f"Error in Command: **{ctx.command.qualified_name}**",
                    description=f"Error created by user: `{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})`"
                    f"\n```py\n{exception}\n```"
                )
                webhook = discord.Webhook.from_url(
                    url=webhooks["error"],
                    adapter=discord.AsyncWebhookAdapter(cs)
                )
                await webhook.send(embed=embed)
        elif isinstance(exception, commands.BadArgument):
            await self.send_cmd_help(ctx)
        elif isinstance(exception, commands.MissingRequiredArgument):
            await self.send_cmd_help(ctx)
        elif isinstance(exception, commands.CheckFailure):
            await ctx.send("You are not allowed to use that command.")
        elif isinstance(exception, commands.CommandOnCooldown):
            await ctx.send(':x: Command is on cooldown... {:.2f} seconds left.'.format(exception.retry_after), delete_after=10)
        elif isinstance(exception, commands.NotOwner):
            await ctx.send(":x: This command is for the owner of the bot, so please do not try to use it again.")
        elif isinstance(exception, commands.BotMissingPermissions):
            await ctx.send("The bot is missing the permissions needed for this command.")
        elif isinstance(exception, commands.CommandNotFound):
            return
        else:
            return


def setup(bot):
    bot.add_cog(
        ErrorHandler(bot)
    )
