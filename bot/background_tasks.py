from logging import getLogger
import asyncio

from .models import TimusUserModel
from .services import update_group_leaderboard, notify_about_submission_verdict
from .services.parser.verdict import Verdict
from .services.parser.last_submissions import get_last_submissions

logger = getLogger(__name__)


async def track_submissions(period: int) -> None:
    """
    Worker that tracks submissions from timus and notifies about them in groups.
    :param period: period in seconds between fetches of submissions
    :return:
    """
    last_handled_submission = None
    while True:
        try:
            groups_to_update_leaderboard = set()
            await asyncio.sleep(period)
            last_submissions = await get_last_submissions(last_handled_submission)
            for i, submission in enumerate(last_submissions):
                if submission.verdict == Verdict.compiling:
                    if i - 1 >= 0:
                        last_handled_submission = last_submissions[i - 1]
                    break
                else:
                    author = await TimusUserModel.get_or_none(timus_id=submission.author.id)
                    last_handled_submission = submission
                    if author is None:
                        continue
                    await notify_about_submission_verdict(submission, author)
                    groups_to_update_leaderboard |= set(author.tracked_in)
            for group in groups_to_update_leaderboard:
                await update_group_leaderboard(group)
        except Exception as e:
            logger.error(e, exc_info=True)
