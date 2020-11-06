from aiohttp import ClientSession
from logging import getLogger
from urllib.parse import quote_plus, urlencode


TIMUS_HOST = 'acm.timus.ru'
session = ClientSession()
logger = getLogger(__name__)


async def search_profiles(username: str) -> str:
    """
    Get search page HTML.
    :param username: Username to search
    :return: HTML string
    """
    async with session.get(f'https://{TIMUS_HOST}/search.aspx?Str={quote_plus(username)}') as resp:
        logger.info(f'Accessed timus server GET /search.aspx?Str={quote_plus(username)}')
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
        logger.info(f'Accessed timus server GET /status.aspx?{urlencode(query_dict)}')
        return await resp.text()


async def get_profile(user_id: int) -> str:
    """
    Get profile page HTML.
    :param user_id: profile page owner's id
    :return: HTML string
    """
    async with session.get(f'https://{TIMUS_HOST}/author.aspx?id={user_id}&sort=difficulty') as resp:
        logger.info(f'Accessed timus server GET /author.aspx?id={user_id}&sort=difficulty')
        return await resp.text()


async def shutdown():
    global session
    await session.close()
