from typing import List, Tuple, Optional
from datetime import datetime
from urllib.parse import parse_qs
from bs4 import BeautifulSoup as bs, Tag
from .verdict import parse_verdict, Verdict

from .submission import Submission
from .timus_user import TimusUser
from .problem import Problem
from ..timus import get_submissions


async def get_last_submissions(prev_last_submission: Submission) -> List[Submission]:
    """
    Get last submissions from timus.
    :param prev_last_submission: First submission without verdict
    :return: List of parsed submissions
    """
    html = await get_submissions()
    last_submissions = _parse_submissions(html)
    while last_submissions[-1].id > prev_last_submission.id:
        html = await get_submissions(last_submissions[-1].id - 1)
        last_submissions.extend(_parse_submissions(html))
    return last_submissions


def _parse_submissions(html: str) -> List[Submission]:
    soup = bs(html, 'html.parser')
    table = soup.find_all('table', {'class': 'status'})[0]
    submissions = [_parse_submission_tr(submission_tr) for submission_tr in table.contents[1:-1]]
    return submissions


def _parse_submission_tr(tr: Tag) -> Submission:
    s_id = _parse_submission_id(tr)
    time = _parse_submission_time(tr)
    author = _parse_submission_author(tr)
    problem = _parse_submission_problem(tr)
    language = _parse_submission_language(tr)
    verdict = _parse_submission_verdict(tr)
    test = _parse_submission_test(tr)
    runtime = _parse_submission_runtime(tr)
    memory = _parse_submission_memory(tr)
    return Submission(s_id, time, author, problem, language,
                      verdict, test, runtime, memory)


def _parse_submission_id(tr: Tag) -> int:
    return int(tr.contents[0].contents[0])


def _parse_submission_time(tr: Tag) -> datetime:
    time_td = tr.contents[1]
    return datetime.strptime(
        f"{time_td.contents[0].contents[0]} {time_td.contents[2].contents[0]}",
        "%H:%M:%S %d %b %Y"
    )


def _parse_submission_author(tr: Tag) -> TimusUser:
    author_a = tr.contents[2].a
    author_id = int(parse_qs(author_a['href'].query)['id'][0])
    return TimusUser(author_id, author_a.contents[0])


def _parse_submission_problem(tr: Tag) -> Problem:
    problem_id = int(tr.contents[3].contents[0].contents[0])
    problem_name = tr.find_all('span', {'class': 'problemname'})[0].contents[0][2:]
    return Problem(problem_id, problem_name)


def _parse_submission_language(tr: Tag) -> str:
    return tr.contents[4].contents[0]


def _parse_submission_verdict(tr: Tag) -> Optional[Verdict]:
    return parse_verdict(tr.contents[5].contents[0])


def _parse_submission_test(tr: Tag) -> Optional[int]:
    try:
        return int(tr.contents[6].contents[0])
    except ValueError:
        return None


def _parse_submission_runtime(tr: Tag) -> Optional[int]:
    try:
        return int(tr.contents[7].contents[0])
    except ValueError:
        return None


def _parse_submission_memory(tr: Tag) -> Optional[int]:
    if isinstance(tr.contents[8].contents[0], str):
        return int(''.join(tr.contents[8].contents[0].split()[:-1]))
    else:
        return None
