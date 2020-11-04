import asyncio

from . import bot
from .models import TimusUserModel
from .services import update_group_leaderboard
from .services.message_formers import form_submission_message
from .services.parser.verdict import Verdict
from .services.parser.submission import Submission
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
        current_first_submission_without_verdict = None
        for submission in last_submissions:
            if submission.verdict == Verdict.compiling:
                if current_first_submission_without_verdict is None:
                    current_first_submission_without_verdict = submission
            else:
                author = await TimusUserModel.get_or_none(timus_id=submission.author.id)
                if author is None:
                    continue
                await _notify_about_submission_verdict(submission, author)
                groups_to_update_leaderboard |= set(author.tracked_in)
        for group in groups_to_update_leaderboard:
            await update_group_leaderboard(group)


async def _notify_about_submission_verdict(submission: Submission, author_model: TimusUserModel) -> None:
    await author_model.fetch_related('tracked_in')
    for group in author_model.tracked_in:
        await bot.send_message(
            group.telegram_id,
            form_submission_message(submission)
        )
