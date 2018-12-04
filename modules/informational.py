import discord
import aiohttp
import math
import psutil

from discord.ext import commands
from datetime import datetime
from config import webhooks, twitch_clientID


class Informational:

    def __init__(self, bot):
        self.bot = bot

    def millify(self, n):
        millnames = ['', 'k', 'M', ' Billion']
        n = float(n)
        millidx = max(0, min(len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

        return '{:.0f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])

    @commands.command()
    @commands.cooldown(1, 14400, commands.BucketType.guild)
    async def contact(self, ctx, *message):
        """Report an error to the developers."""
        if ctx.guild.id == 472302438490046494:
            return await ctx.send("Please do not use contact in the support server.")

        inv = await ctx.channel.create_invite(
            max_uses=3,
            reason="contact command in channel {} by user {}".format(ctx.channel.name, ctx.author.name)
        )

        async with aiohttp.ClientSession() as cs:
            webhook = discord.Webhook.from_url(
                url=webhooks["contact"],
                adapter=discord.AsyncWebhookAdapter(cs)
            )

            await webhook.send("<@&472304841528573962> Help has been requested in **{}** in the channel **{}** by **{}**.\n"
                               "**{}** said: **__\"{}\"__**\n\nHere is the invite: {}"
                               .format(ctx.guild.name, ctx.channel.name, ctx.author.name, ctx.author.name, ' '.join(message), inv))
            await ctx.send("Your issue has been sent. Please be patient for support.\n\ndiscord.gg/mqzcMca")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        """Ping... PONG!"""
        pingmsg = await ctx.send("Pinging so fast you won't even see this!!")
        await pingmsg.edit(content=f"Ping => {round(self.bot.latency * 1000, 2)} ms")

    @commands.command(aliases=["server", "sinfo", "guildinfo", "ginfo", "guild"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serverinfo(self, ctx):
        """Get information on the server."""
        embed = discord.Embed(colour=3553599)
        embed.set_author(name=f"{ctx.guild.name} ({ctx.guild.id})", icon_url=ctx.guild.icon_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(
            name="Owner",
            value=f"{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}"
        )
        embed.add_field(
            name="Region",
            value=ctx.guild.region
        )
        embed.add_field(
            name="Member Count",
            value=ctx.guild.member_count
        )
        embed.add_field(
            name="Channels",
            value=f"{len(ctx.guild.text_channels)} Text Channels\n{len(ctx.guild.voice_channels)} Voice Channels"
        )
        embed.add_field(
            name=f"{len(ctx.guild.roles) - 1} Roles",
            value=", ".join([str(x) for x in ctx.guild.roles][1:]),
            inline=False
        )
        embed.add_field(
            name=f"{len(ctx.guild.emojis)} Emojis",
            value=" | ".join([str(x) for x in ctx.guild.emojis]),
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["uinfo", "user"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx, user: discord.Member=None):
        """Shows information on a user or yourself."""
        if user is None:
            user = ctx.author
        try:
            playinggame = user.activity.title
        except:
            playinggame = "Not Playing Anything"

        embed = discord.Embed(colour=3553599)
        embed.set_author(name=f"{user} ({user.id})", icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(
            name="Is Bot?",
            value=str(user.bot)
        )
        embed.add_field(
            name=f"Playing ({user.status})",
            value=playinggame
        )
        embed.add_field(
            name="Account Created",
            value=user.created_at.strftime("%b %d %Y %H:%M")
        )
        embed.add_field(
            name="Joined Server",
            value=user.joined_at.strftime("%b %d %Y %H:%M")
        )
        try:
            if user.roles[1:]:
                roles = ", ".join(sorted([x.name for x in user.roles][1:], key=[x.name for x in ctx.guild.role_hierarchy][1:].index))
            else:
                roles = "No Roles"
            embed.add_field(
                name=f"({len(user.roles[1:])}) Roles",
                value=roles,
                inline=False
            )
        except:
            pass

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, user: discord.Member=None):
        """"Sends avatar of the user mentioned or you."""
        if user is None:
            user = ctx.author
        if user.avatar_url is None:
            return await ctx.send("User has no avatar.")
        embed = discord.Embed(title=f"{user.name}'s avatar:", colour=3553599)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        """Sends the bot's invite and an invite to the support server."""
        if ctx.guild.id == 472302438490046494:
            return await ctx.send(f"<https://discordapp.com/oauth2/authorize?client_id={self.bot.id}&scope=bot&permissions=0>\n"
                                  f"\nHere is my invite, make sure to give it the right permissions for what you need to use it for "
                                  f"or else it may not work properly. :heart:")
        return await ctx.send(f"<https://discordapp.com/oauth2/authorize?client_id={self.bot.id}&scope=bot&permissions=0>\n"
                              f"\nHere is my invite, make sure to give it the right permissions or else it may not work properly. "
                              f":heart:\nAlso here's the support server if you have any questions or suggestions: "
                              f"https://discord.gg/mqzcMca")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def twitch(self, ctx, account):
        """Returns information on the Twitch account you want information on."""
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://api.twitch.tv/kraken/channels/{account}?client_id={twitch_clientID}") as r:
                    res = await r.json()
                    creationdate = datetime.strptime(str(res['created_at']).split('.')[0], "%Y-%m-%dT%H:%M:%SZ").strftime("%m-%d-%Y")

                    embed = discord.Embed(colour=3553599)
                    embed.set_author(name=res["display_name"], icon_url="https://i.imgur.com/OQwQ8z0.jpg", url=res["url"])
                    embed.add_field(
                        name="Account ID",
                        value=res["_id"],
                        inline=True
                    )
                    embed.add_field(
                        name="\u200B",
                        value="\u200B",
                        inline=True
                    )
                    embed.add_field(
                        name="Followers",
                        value=res["followers"],
                        inline=True
                    )
                    embed.add_field(
                        name="Created On",
                        value=creationdate,
                        inline=True
                    )
                    embed.add_field(
                        name="\u200B",
                        value="\u200B",
                        inline=True
                    )
                    embed.add_field(
                        name="Channel Views",
                        value=res["views"],
                        inline=True
                    )

                    await ctx.send(embed=embed)
        except Exception:
            await ctx.send(f"Unable to find account: {account}. Are you sure you spelt it correctly?")

    @commands.command(aliases=["botstats"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stats(self, ctx):
        """Gives you stats on the bot."""
        memory = psutil.virtual_memory().total >> 20
        mem_usage = psutil.virtual_memory().used >> 20

        embed = discord.Embed(colour=3553599)
        embed.set_author(name=f"{self.bot.user.name}'s Statistics", icon_url=self.bot.user.avatar_url)
        embed.add_field(
            name="Server Count",
            value=f"{self.millify(len(self.bot.guilds))} ({str(len(self.bot.guilds))})"
        )
        embed.add_field(
            name="User Count",
            value=f"{self.millify(len(self.bot.users))} ({str(len(self.bot.users))})"
        )
        embed.add_field(
            name="Shard Count",
            value=self.bot.shard_count
        )
        try:
            embed.add_field(
                name="Most Used Command",
                value=self.bot.command_usage.most_common(1)[0][0],
                inline=False
            )
        except:
            embed.add_field(
                name="Most Used Command",
                value="stats",
                inline=False
            )
        embed.add_field(
            name="RAM Usage",
            value=f"{mem_usage}/{memory} MB ({int(memory - mem_usage)} MB free)",
            inline=False
        )
        embed.add_field(
            name="Uptime",
            value=self.bot.bot_uptime(),
            inline=False
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(
        Informational(bot)
    )
