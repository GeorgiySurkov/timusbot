from dataclasses import dataclass
from typing import Optional, List
from bs4 import BeautifulSoup as bs, Tag

from .problem import Problem
from ..timus import get_profile


@dataclass(eq=False, order=False)
class TimusUser:
    """Class to represent Timus user"""
    id: int
    username: Optional[str] = None,
    country: Optional[str] = None,
    solved_problems: Optional[List[Problem]] = None
    solved_problems_amount: Optional[int] = None
    place_by_problems: Optional[int] = None
    rating: Optional[int] = None
    place_by_rating: Optional[int] = None

    async def _get_profile_data(self, parse_solved_problems: bool = False):
        html = await get_profile(self.id)
        soup = bs(html, 'html.parser')
        self.username = self._get_username(soup)
        self.country = self._get_country(soup)
        stats_table = soup.find_all('table', {'class': 'author_stats'})[0]
        self.solved_problems_amount = self._get_solved_problems_amount(stats_table)
        self.place_by_problems = self._get_place_by_problems(stats_table)
        self.rating = self._get_rating(stats_table)
        self.place_by_rating = self._get_place_by_rating(stats_table)

    @staticmethod
    def _get_username(soup: bs) -> str:
        return soup.find_all('h2', {'class': 'author_name'})[0].contents[0]

    @staticmethod
    def _get_country(soup: bs) -> str:
        return soup.find_all('div', {'class': 'author_flag'})[0].div['title']

    @staticmethod
    def _get_solved_problems_amount(stats_table: Tag) -> int:
        return int(stats_table.contents[1].contents[1].contents[0].split(maxsplit=1)[0])

    @staticmethod
    def _get_place_by_problems(stats_table: Tag) -> int:
        return int(stats_table.contents[0].contents[1].contents[0].split(maxsplit=1)[0])

    @staticmethod
    def _get_place_by_rating(stats_table: Tag) -> int:
        return int(stats_table.contents[2].contents[1].contents[0].split(maxsplit=1)[0])

    @staticmethod
    def _get_rating(stats_table: Tag) -> int:
        return int(stats_table.contents[3].contents[1].contents[0].split(maxsplit=1)[0])
