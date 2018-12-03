import discord

from discord.ext import commands
from .utils.paginator import HelpPaginator


class Help:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cmds", "cmd", "commands", "command", "helpme"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, command: str=None):
        """Gives you a list of all of the commands"""
        if command:
            entity = self.bot.get_cog(command) or self.bot.get_command(command)

            if entity is None:
                clean = command.replace('@', '@\u200b')
                return await ctx.send(f"Command or category \"{clean}\" not found.")
            elif isinstance(entity, commands.Command):
                p = await HelpPaginator.from_command(ctx, entity)
            else:
                p = await HelpPaginator.from_cog(ctx, entity)
            return await p.paginate()
        try:
            embed = discord.Embed(colour=3553599)
            embed.set_author(name=f"{self.bot.user.name} Commands!", icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f"{len(self.bot.commands)} Total Commands")
            try:
                embed.add_field(
                    name="Informational",
                    value=", ".join([f"`{i.name}`" for i in self.bot.commands if i.cog_name == "Informational" and not i.hidden]),
                    inline=False
                )
            except:
                pass

            try:
                if ctx.author.id == 227110473466773504:
                    embed.add_field(
                        name="Developer",
                        value=", ".join([f"`{i.name}`" for i in self.bot.commands if i.cog_name == "Developer"]),
                        inline=False
                    )
            except:
                pass

            return await ctx.send(embed=embed)
        except discord.HTTPException:
            return await ctx.send(":x: I cannot send embeds here!")
        except:
            pass


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(
        Help(bot)
    )
