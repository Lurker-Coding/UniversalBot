import os
import discord
import aiohttp
import random
import time
import rethinkdb as r

from discord.ext import commands
from collections import Counter
from datetime import datetime
from pyfiglet import Figlet
from config import database, prefixes, token, webhooks


def _prefixes(bot, msg):
    return commands.when_mentioned_or(*prefixes)(bot, msg)


class UniversalBot(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(
            command_prefix=_prefixes,
            description="Bot I plan to keep adding features to.",
            status=discord.Status.dnd,
            activity=discord.Game(name="Starting up..."),
            pm_help=False,
            help_attrs={
                "hidden": True
            }
        )

        self._last_exception = None
        self.counter = Counter()
        self.command_usage = Counter()

        async def _init_rethink():
            r.set_loop_type("asyncio")
            self.r_conn = await r.connect(
                host=database["host"],
                port=database["port"],
                db=database["db"],
                user=database["user"],
                password=database["password"]
            )

        self.loop.create_task(_init_rethink())

        for file in os.listdir("modules"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.load_extension(f"modules.{name}")
                except Exception as e:
                    print(f"Failed to load {name}: {e}")

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CommandNotFound):
            return

    async def on_command(self, ctx):
        try:
            if ctx.author.id not in [227110473466773504, 302523498226647041]:
                self.command_usage[str(ctx.command)] += 1
        except:
            pass
        try:
            if ctx.author.id not in [227110473466773504, 302523498226647041]:
                async with aiohttp.ClientSession() as cs:
                    webhook = discord.Webhook.from_url(
                        url=webhooks["command"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    await webhook.send(f"[`{datetime.utcnow().strftime('%m-%d-%Y %H:%M:%S')}`] [`{ctx.guild.name} "
                                       f"({ctx.guild.id})`] User **{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})** "
                                       f"ran the command **{ctx.command.name}**.")
        except Exception as e:
            async with aiohttp.ClientSession() as cs:
                webhook = discord.Webhook.from_url(
                    url=webhooks["command"],
                    adapter=discord.AsyncWebhookAdapter(cs)
                )
                await webhook.send(f"Command Logger Failed:\n`{type(e).__name__}`\n```py\n{e}\n```")

    async def send_cmd_help(self, ctx):
        if ctx.invoked_subcommand:
            pages = await self.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await ctx.send(page)
        else:
            pages = await self.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await ctx.send(page)

    async def __level_handler(self, message):
        if not isinstance(message.channel, discord.TextChannel):
            return
        if message.content == "" or not len(message.content) > 5:
            return

        if random.randint(1, 10) == 1:
            author = message.author
            user_data = await r.table("levelSystem").get(str(author.id)).run(self.r_conn)
            if not user_data:
                data = {
                    "id": str(author.id),
                    "xp": 0,
                    "lastxp": "0",
                    "blacklisted": False,
                    "lastxptimes": []
                }

                return await r.table("levelSystem").insert(data).run(self.r_conn)

            if user_data.get("blacklisted", False):
                return

            if (int(time.time()) - int(user_data["lastxp"])) >= 120:
                lastxptimes = user_data["lastxptimes"]
                lastxptimes.append(str(int(time.time())))

                xp = user_data["xp"] + random.randint(10, 40)
                data = {
                    "xp": xp,
                    "lastxp": str(int(time.time())),
                    "lastxptimes": lastxptimes
                }

                await r.table("levelSystem").get(str(author.id)).update(data).run(self.r_conn)

        if random.randint(1, 10) == 1:
            author = message.author
            guildXP = await r.table("guildXP").get(str(author.id)).run(self.r_conn)

            if not guildXP or not guildXP.get(str(message.author.id)):
                data = {
                    str(message.author.id): {
                        "lastxp": str(int(time.time())),
                        "xp": 0
                    }
                }

                if not guildXP:
                    data["id"] = str(message.guild.id)

                return await r.table("guildXP").get(str(message.guild.id)).update(data).run(self.r_conn)

            if (int(time.time()) - int(guildXP.get(str(message.author.id))["lastxp"])) >= 120:
                xp = guildXP.get(str(message.author.id))["xp"] + random.randint(10, 40)
                data = {
                    str(message.author.id): {
                        "xp": xp,
                        "lastxp": str(int(time.time()))
                    }
                }

                await r.table("guildXP").get(str(message.guild.id)).update(data).run(self.r_conn)

    async def on_message(self, message):
        self.counter["messages_read"] += 1

        if message.author.bot:
            return

        await self.process_commands(message)
        await self.__level_handler(message)

    async def close(self):
        self.r_conn.close()
        # self.redis.close()
        await super().close()

    async def on_shard_ready(self, shard_id):
        print(f"Shard {shard_id} Connected.")

    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.uptime = datetime.utcnow()

        print(Figlet().renderText("UniversalBot"))
        print(f"Shards: {self.shard_count}")
        print(f"Servers: {len(self.guilds)}")
        print(f"Users: {len(set(self.get_all_members()))}")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"{prefixes[0]}help | {self.shard_count} Shards")
        )

    def bot_uptime(self, *, brief=False):
        now = datetime.utcnow()
        delta = now - self.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            fmt = "{h} hours, {m} minutes, and {s} seconds"
            if days:
                fmt = "{d} days, " + fmt
        else:
            fmt = "{h}h {m}m {s}s"
            if days:
                fmt = "{d}d " + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    def run(self):
        super().run(token)


if __name__ == "__main__":
    UniversalBot().run()
