import discord
import aiohttp

from discord.ext import commands


class ImageC:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def neko(self, ctx):
        """Sends a pic of a neko."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekos.life/api/neko") as r:
                res = await r.json()

        embed = discord.Embed(colour=3553599)
        embed.set_image(url=res["neko"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dog(self, ctx):
        """Sends a pic of a dog."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                res = await r.json()

        embed = discord.Embed(colour=3553599)
        embed.set_image(url=res["url"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cat(self, ctx):
        """Sends a pic of a cat."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://aws.random.cat/meow") as r:
                res = await r.json()

        embed = discord.Embed(colour=3553599)
        embed.set_image(url=res["file"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lizard(self, ctx):
        """Sends a pic of a lizard."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekos.life/api/lizard") as r:
                res = await r.json()

        embed = discord.Embed(colour=3553599)
        embed.set_image(url=res["url"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def duck(self, ctx):
        """Sends a pic of a duck."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random-d.uk/api/v1/random") as r:
                res = await r.json()

        embed = discord.Embed(colour=3553599)
        embed.set_image(url=res["url"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def panda(self, ctx):
        """Sends a pic of a panda."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://animals.anidiots.guide/panda") as r:
                res = await r.json()

        embed = discord.Embed(colour=3553599)
        embed.set_image(url=res["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def penguin(self, ctx):
        """Sends a pic of a penguin."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://animals.anidiots.guide/penguin") as r:
                res = await r.json()

        embed = discord.Embed(colour=3553599)
        embed.set_image(url=res["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tiger(self, ctx):
        """Sends a pic of a tiger."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://animals.anidiots.guide/tiger") as r:
                res = await r.json()

        embed = discord.Embed(colour=3553599)
        embed.set_image(url=res["link"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lion(self, ctx):
        """Sends a pic of a lion."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://animals.anidiots.guide/lion") as r:
                res = await r.json()

        embed = discord.Embed(colour=3553599)
        embed.set_image(url=res["link"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(
        ImageC(bot)
    )
