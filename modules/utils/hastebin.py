import aiohttp


async def post(content):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://server.cwelch.me/documents", data=str(content).encode('utf-8')) as response:
            res = await response.json()
            return f"http://server.cwelch.me/{res['key']}"
