from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .timus_user import TimusUser
from .problem import Problem
from .verdict import Verdict


@dataclass(eq=False, order=False)
class Submission:
    id: int
    timestamp: datetime
    author: TimusUser
    problem: Problem
    language: str
    verdict: Verdict
    test_number: Optional[int] = None
    runtime: Optional[float] = None
    memory: Optional[int] = None

    def __eq__(self, other):
        return type(other) is type(self) and other.id == self.id

