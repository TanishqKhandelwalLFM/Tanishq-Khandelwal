import asyncio
import aiohttp


async def fetch_data():
    async with aiohttp.ClientSession() as session:

        async with session.get(
            "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow"
        ) as response:

            data = await response.json()

            return data

async def main():
    data = await fetch_data()
    print(data)


asyncio.run(main())