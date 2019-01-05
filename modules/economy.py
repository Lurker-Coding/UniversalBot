import discord
import rethinkdb as r
import math

from discord.ext import commands


class Economy:

    def __init__(self, bot):
        self.bot = bot

    def _required_exp(self, level: int):
        if level < 0:
            return 0

        return 139 * level + 65

    def _level_exp(self, level: int):
        return level * 65 + 139 * level * (level - 1) // 2

    def _find_level(self, total_exp):
        return int((1 / 278) * (9 + math.sqrt(81 + 1112 * total_exp)))

    async def __has_account(self, user: int):
        if await r.table("economy").get(str(user)).run(self.bot.r_conn):
            return True
        else:
            return False

    async def __get_balance(self, user: int):
        balance = await r.table("economy").get(str(user)).run(self.bot.r_conn)

        return int(balance["balance"])

    async def __has_level_account(self, user: int):
        if await r.table("levels").get(str(user)).run(self.bot.r_conn):
            return True
        else:
            return False

    async def __create_level_account(self, user: int):
        data = {
            "id": str(user),
            "title": "",
            "description": ""
        }

        await r.table("levels").insert(data).run(self.bot.r_conn)

    async def __check_level_account(self, user: int):
        if not await self.__has_level_account(user):
            await self.__create_level_account(user)

    async def __update_balance(self, user: int, amount: int):
        await r.table("economy").get(str(user)).update({
            "balance": int(amount)
        }).run(self.bot.r_conn)

    async def __update_payday_time(self, user: int):
        await r.table("economy").get(str(user)).update({
            "lastpayday": str(int(time.time()))
        }).run(self.bot.r_conn)

    async def __is_frozen(self, user: int):
        data = await r.table("economy").get(str(user)).run(self.bot.r_conn)
        frozen = data.get("frozen", False)
        if frozen:
            return True
        else:
            return False

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def register(self, ctx):
        """Register an account."""
        user = ctx.author
        await self.__has_level_account(user.id)

        if await self.__has_account(user.id):
            await ctx.send("You already have an account.")
        else:
            data = {
                "id": str(user.id),
                "balance": 0,
                "lastpayday": "0",
                "frozen": False
            }

            await r.table("economy").insert(data).run(self.bot.r_conn)
            await ctx.send("I hope you enjoy your new account!")

    @commands.command(aliases=["bal", "money", "$"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx, user:discord.Member=None):
        """Shows yours or another users balance"""
        if not user:
            user = ctx.author

        await self.__check_level_account(user.id)

        if await self.__has_account(user.id):
            balance = await self.__get_balance(user.id)

            await ctx.send(f"Balance: **${balance}**")
        else:
            await ctx.send("Balance: **$0**")


def setup(bot):
    bot.add_cog(
        Economy(bot)
    )
