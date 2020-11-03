from aiohttp import ClientSession
from urllib.parse import quote_plus, urlencode


TIMUS_HOST = 'acm.timus.ru'
session = ClientSession()


async def search_profiles(username: str) -> str:
    """
    Get search page HTML.
    :param username: Username to search
    :return: HTML string
    """
    async with session.get(f'https://{TIMUS_HOST}/search.aspx?Str={quote_plus(username)}') as resp:
        return await resp.text()


async def get_submissions(offset: int = None, count: int = 100) -> str:
    """
    Get submissions page HTML.
    :param count: Number of submissions on the page
    :param offset: Id of the first submission on the page
    :return: HTML string
    """
    query_dict = {'count': count, 'space': 1}
    if offset is not None:
        query_dict['from'] = offset
    async with session.get(f'https://{TIMUS_HOST}/status.aspx?{urlencode(query_dict)}') as resp:
        return await resp.text()


async def shutdown():
    global session
    await session.close()
