from dataclasses import dataclass
from typing import Optional, List

from .problem import Problem


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

    async def _get_profile_data(self):
        # TODO: write profile data parsing
        pass

    async def _get_solved_problems(self):
        # TODO: write solved problems parsing
        pass
