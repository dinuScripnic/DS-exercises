import aiohttp
import asyncio
import sys


async def main(url: str) -> None:
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url) as response:
                status = response.status
                if status >= 400:
                    raise aiohttp.ClientError(f"Error {status} while fetching {url}")
                headers = response.headers
                print(f"Headers: {headers}")
                html = await response.text()
                print(f"Body: {html} ")
    except asyncio.TimeoutError:
        raise asyncio.TimeoutError(f"Timeout while fetching {url}")
    except aiohttp.ClientError:
        raise aiohttp.ClientError(f"Error while fetching {url}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if sys.argv[1] is None:
        print("Usage: python webclient.py <url>")
        sys.exit(1)
    loop.run_until_complete(main(sys.argv[1]))