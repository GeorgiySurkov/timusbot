from typing import List
from bs4 import BeautifulSoup as bs, Tag
from urllib.parse import parse_qs, urlparse

from .timus_user import TimusUser
from ... import timus


async def search_timus_user(username: str) -> List[TimusUser]:
    html = await timus.search_profiles(username)
    if html == '':
        return []
    soup = bs(html, 'html.parser')
    users_table = soup.find_all('table', {'class': 'ranklist'})[0]
    users = [_parse_user_tr(user_tr) for user_tr in users_table.contents[1:]]
    return users


def _parse_user_tr(user_tr: Tag) -> TimusUser:
    username = user_tr.contents[2].a.contents[0]
    place_by_problems = int(user_tr.contents[0].contents[0])
    country = user_tr.contents[1].div['title']
    user_href = urlparse(user_tr.contents[2].a['href'])
    user_id = int(parse_qs(user_href.query)['id'][0])
    rating = int(user_tr.contents[3].contents[0])
    solved_problems_amount = int(user_tr.contents[4].contents[0])
    return TimusUser(
        id=user_id,
        username=username,
        country=country,
        solved_problems_amount=solved_problems_amount,
        place_by_problems=place_by_problems,
        rating=rating
    )
