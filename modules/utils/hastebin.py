import aiohttp


async def post(content):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://server.cwelch.me:7777/documents", data=str(content).encode('utf-8')) as response:
            res = await response.json()
            return f"http://server.cwelch.me:7777/{res['key']}"
