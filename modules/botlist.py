import asyncio
import aiohttp
import discord
from config import botlists, webhooks


class BotList:

    def __init__(self, bot):
        self.bot = bot
        self.guildcount = len(bot.guilds)
        self.botid = bot.user.id

    async def updatebotlists(self):
        while True:
            async with aiohttp.ClientSession() as cs:
                webhook = discord.Webhook.from_url(
                    url=webhooks["botlist"],
                    adapter=discord.AsyncWebhookAdapter(cs)
                )

                await webhook.send(f"Attempting to push guild count of {len(self.bot.guilds)} to each botlist.")

            # discordbotlabs.com is possibly shutting down February 1
            # I'm commenting this out then deleting it if they do shut down

            # try:
            #     url = f"https://discordbotlabs.com/api/" # discordbotlabs.com doesn't have its api finished yet
            #     payload = {
            #         "shard_id": self.bot.shard_count,
            #         "guilds": int(self.guildcount)
            #     }
            #     headers = {
            #         "Authorization": "Bot " + botlists["discordbotlabscom"],
            #         "Content-Type": "application/json"
            #     }
            #
            #     async with aiohttp.ClientSession() as cs:
            #         await cs.post(
            #             url=url,
            #             json=payload,
            #             headers=headers
            #         )
            #         webhook = discord.Webhook.from_url(
            #             url=webhooks["botlist"],
            #             adapter=discord.AsyncWebhookAdapter(cs)
            #         )
            #         await webhook.send(f"Posted guild count of {self.guildcount} for botlist discordbotlabs.com")
            # except Exception as e:
            #     async with aiohttp.ClientSession() as cs:
            #         webhook = discord.Webhook.from_url(
            #             url=webhooks["botlist"],
            #             adapter=discord.AsyncWebhookAdapter(cs)
            #         )
            #         webhook.send(f"Failed to post guild count to discordbotlabs.com\n`{type(e).__name__}`\n```py\n{e}\n```")

            try:
                url = f"https://discordbotlist.com/api/bots/{self.botid}/stats"
                payload = {
                    "guilds": int(self.guildcount),
                    "users": len(set(self.bot.get_all_members()))
                }
                headers = {
                    "Authorization": botlists["discordbotlistcom"],
                    "Content-Type": "application/json"
                }

                async with aiohttp.ClientSession() as cs:
                    await cs.post(
                        url=url,
                        json=payload,
                        headers=headers
                    )
                    webhook = discord.Webhook.from_url(
                        url=webhooks["botlist"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    await webhook.send(f"Posted guild count of {self.guildcount} for botlist discordbotlist.com")
            except Exception as e:
                async with aiohttp.ClientSession() as cs:
                    webhook = discord.Webhook.from_url(
                        url=webhooks["botlist"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    webhook.send(f"Failed to post guild count to discordbotlist.com\n`{type(e).__name__}`\n```py\n{e}\n```")

            try:
                url = f"https://discord.boats/api/bot/{self.bot.id}"
                payload = {
                    "guilds": int(self.guildcount)
                }
                headers = {
                    "Authorization": botlists["discordboats"],
                    "Content-Type": "application/json"
                }

                async with aiohttp.ClientSession() as cs:
                    await cs.post(
                        url=url,
                        json=payload,
                        headers=headers
                    )
                    webhook = discord.Webhook.from_url(
                        url=webhooks["botlist"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    await webhook.send(f"Posted guild count of {self.guildcount} for botlist discord.boats")
            except Exception as e:
                async with aiohttp.ClientSession() as cs:
                    webhook = discord.Webhook.from_url(
                        url=webhooks["botlist"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    webhook.send(f"Failed to post guild count to discord.boats\n`{type(e).__name__}`\n```py\n{e}\n```")

            try:
                url = f"https://discordbots.org/api/bots/{self.botid}/stats"
                payload = {
                    "server_count": int(self.guildcount),
                    "shard_count": self.bot.shard_count
                }
                headers = {
                    "Authorization": botlists["discordbotsorg"]
                }

                async with aiohttp.ClientSession() as cs:
                    await cs.post(
                        url=url,
                        json=payload,
                        headers=headers
                    )
                    webhook = discord.Webhook.from_url(
                        url=webhooks["botlist"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    await webhook.send(f"Posted guild count of {self.guildcount} for botlist discordbots.org")
            except Exception as e:
                async with aiohttp.ClientSession() as cs:
                    webhook = discord.Webhook.from_url(
                        url=webhooks["botlist"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    webhook.send(f"Failed to post guild count to discordbots.org\n`{type(e).__name__}`\n```py\n{e}\n```")

            try:
                url = f"https://bots.discord.pw/api/bots/{self.botid}/stats"
                payload = {
                    "server_count": int(self.guildcount),
                    "shard_count": self.bot.shard_count
                }
                headers = {
                    "Authorization": botlists["botsdiscordpw"]
                }

                async with aiohttp.ClientSession() as cs:
                    await cs.post(
                        url=url,
                        json=payload,
                        headers=headers
                    )
                    webhook = discord.Webhook.from_url(
                        url=webhooks["botlist"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    await webhook.send(f"Posted guild count of {self.guildcount} for botlist bots.discord.pw")
            except Exception as e:
                async with aiohttp.ClientSession() as cs:
                    webhook = discord.Webhook.from_url(
                        url=webhooks["botlist"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    webhook.send(f"Failed to post guild count to bots.discord.pw\n`{type(e).__name__}`\n```py\n{e}\n```")

            try:
                url = f"https://botlist.space/api/bots/{self.botid}"
                payload = {
                    "server_count": int(self.guildcount)
                }
                headers = {
                    "Authorization": botlists["botlistspace"],
                    "Content-Type": "application/json"
                }

                async with aiohttp.ClientSession() as cs:
                    await cs.post(
                        url=url,
                        json=payload,
                        headers=headers
                    )
                    webhook = discord.Webhook.from_url(
                        url=webhooks["botlist"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    await webhook.send(f"Posted guild count of {self.guildcount} for botlist botlist.space")
            except Exception as e:
                async with aiohttp.ClientSession() as cs:
                    webhook = discord.Webhook.from_url(
                        url=webhooks["botlist"],
                        adapter=discord.AsyncWebhookAdapter(cs)
                    )
                    webhook.send(f"Failed to post guild count to botlist.space\n`{type(e).__name__}`\n```py\n{e}\n```")

            await asyncio.sleep(43200)

    async def on_ready(self):
        await self.updatebotlists()


def setup(bot):
    bot.add_cog(
        BotList(bot)
    )
