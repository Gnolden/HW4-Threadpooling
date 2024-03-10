import asyncio
import aiohttp
import platform
import concurrent.futures

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_urls_in_process(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return responses

async def fetch_all_urls(urls_chunk):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, fetch_urls_in_process, chunk) for chunk in urls_chunk]
        responses = await asyncio.gather(*tasks)
        return responses

async def main():
    urls_chunks = [
        [f"https://dummyjson.com/products/{x}" for x in range(1, 21)],
        [f"https://dummyjson.com/products/{x}" for x in range(21, 41)],
        [f"https://dummyjson.com/products/{x}" for x in range(41, 61)],
        [f"https://dummyjson.com/products/{x}" for x in range(61, 81)],
        [f"https://dummyjson.com/products/{x}" for x in range(81, 101)]
    ]

    responses = await fetch_all_urls(urls_chunks)

    with open('response.json', 'w', encoding="utf-8") as f:
        jhon = ',\n'.join([response for chunk in responses for response in await chunk])
        f.write(f"[\n{jhon}\n]")

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
