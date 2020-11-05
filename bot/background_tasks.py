import asyncio

from .models import TimusUserModel
from .services import update_group_leaderboard, notify_about_submission_verdict
from .services.parser.verdict import Verdict
from .services.parser.last_submissions import get_last_submissions


async def track_submissions(period: int) -> None:
    """
    Worker that tracks submissions from timus and notifies about them in groups.
    :param period: period in seconds between fetches of submissions
    :return:
    """
    first_submission_without_verdict = None
    while True:
        groups_to_update_leaderboard = set()
        await asyncio.sleep(period)
        last_submissions = await get_last_submissions(first_submission_without_verdict)
        first_submission_without_verdict = None
        for submission in last_submissions[::-1]:
            if submission.verdict == Verdict.compiling:
                if first_submission_without_verdict is None:
                    first_submission_without_verdict = submission
            else:
                author = await TimusUserModel.get_or_none(timus_id=submission.author.id)
                if author is None:
                    continue
                await notify_about_submission_verdict(submission, author)
                groups_to_update_leaderboard |= set(author.tracked_in)
        if first_submission_without_verdict is None:
            first_submission_without_verdict = last_submissions[0]
        for group in groups_to_update_leaderboard:
            await update_group_leaderboard(group)
