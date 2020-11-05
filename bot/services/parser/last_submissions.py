from typing import List, Optional
from datetime import datetime
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup as bs, Tag
from .verdict import parse_verdict, Verdict

from .submission import Submission
from .timus_user import TimusUser
from .problem import Problem
from ...timus import get_submissions


async def get_last_submissions(prev_last_handled_submission: Optional[Submission] = None) -> List[Submission]:
    """
    Get last submissions from timus. Guaranteed that first submission doesn't have verdict Compiling
    :param prev_last_handled_submission: last handled submission
    :return: List of parsed submissions
    """
    html = await get_submissions(count=10)
    last_submissions = _parse_submissions(html)
    while prev_last_handled_submission is not None and \
            last_submissions[-1].id > prev_last_handled_submission.id and \
            last_submissions[-1].verdict != Verdict.compiling:
        html = await get_submissions(last_submissions[-1].id - 1, count=10)
        last_submissions.extend(_parse_submissions(html))
    if prev_last_handled_submission is not None:
        last_submissions = last_submissions[:last_submissions.index(prev_last_handled_submission)]
    return last_submissions[::-1]


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
    author_id = int(parse_qs(urlparse(author_a['href']).query)['id'][0])
    return TimusUser(author_id, author_a.contents[0])


def _parse_submission_problem(tr: Tag) -> Problem:
    problem_id = int(tr.contents[3].contents[0].contents[0])
    problem_name = tr.find_all('span', {'class': 'problemname'})[0].contents[0][2:]
    return Problem(problem_id, problem_name)


def _parse_submission_language(tr: Tag) -> str:
    return tr.contents[4].contents[0]


def _parse_submission_verdict(tr: Tag) -> Optional[Verdict]:
    verdict = tr.contents[5].contents[0]
    if isinstance(verdict, Tag):
        verdict = verdict.contents[0]
    return parse_verdict(verdict)


def _parse_submission_test(tr: Tag) -> Optional[int]:
    if isinstance(tr.contents[6].contents[0], str):
        return int(tr.contents[6].contents[0])
    return None


def _parse_submission_runtime(tr: Tag) -> Optional[float]:
    if isinstance(tr.contents[7].contents[0], Tag):
        return None
    return float(tr.contents[7].contents[0])


def _parse_submission_memory(tr: Tag) -> Optional[int]:
    if isinstance(tr.contents[8].contents[0], str):
        return int(''.join(tr.contents[8].contents[0].split()[:-1]))
    return None
