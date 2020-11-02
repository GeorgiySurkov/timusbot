from aiohttp import ClientSession
from urllib.parse import quote_plus


TIMUS_HOST = 'acm.timus.ru'
session = ClientSession()


async def search_profiles(username: str) -> str:
    with session.get(f'https://{TIMUS_HOST}/search.aspx?Str={quote_plus(username)}') as resp:
        return await resp.text()


async def shutdown():
    global session
    await session.close()
