from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError, ClientConnectionError
from logging import getLogger
from urllib.parse import quote_plus, urlencode


TIMUS_HOST = 'acm.timus.ru'
session = ClientSession()
logger = getLogger(__name__)


async def search_profiles(username: str, retries: int = 5) -> str:
    """
    Get search page HTML.
    :param username: Username to search
    :param retries: retries to connect to timus
    :return: HTML string
    """
    try:
        async with session.get(f'https://{TIMUS_HOST}/search.aspx?Str={quote_plus(username)}') as resp:
            logger.info(f'Accessed timus server GET {resp.status} /search.aspx?Str={quote_plus(username)}')
            return await resp.text()
    except ClientConnectionError:
        if retries > 1:
            return await search_profiles(username, retries - 1)
        raise


async def get_submissions(offset: int = None, count: int = 100, retries: int = 5) -> str:
    """
    Get submissions page HTML.
    :param count: Number of submissions on the page
    :param offset: Id of the first submission on the page
    :param retries: retries to connect to timus
    :return: HTML string
    """
    try:
        query_dict = {'count': count, 'space': 1}
        if offset is not None:
            query_dict['from'] = offset
        async with session.get(f'https://{TIMUS_HOST}/status.aspx?{urlencode(query_dict)}') as resp:
            logger.info(f'Accessed timus server GET {resp.status} /status.aspx?{urlencode(query_dict)}')
            return await resp.text()
    except ClientConnectionError:
        if retries > 1:
            return await get_submissions(offset, count, retries - 1)
        raise


async def get_profile(user_id: int, retries: int = 5) -> str:
    """
    Get profile page HTML.
    :param user_id: profile page owner's id
    :param retries: retries to connect to timus
    :return: HTML string
    """
    try:
        async with session.get(f'https://{TIMUS_HOST}/author.aspx?id={user_id}&sort=difficulty') as resp:
            logger.info(f'Accessed timus server GET {resp.status} /author.aspx?id={user_id}&sort=difficulty')
            return await resp.text()
    except ClientConnectionError:
        if retries > 1:
            return await get_profile(user_id, retries - 1)
        raise


async def shutdown():
    global session
    await session.close()
