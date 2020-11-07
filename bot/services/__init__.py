from aiogram import types
from aiogram.utils import exceptions as ex
from logging import getLogger

from .. import bot
from ..models import GroupModel, TimusUserModel
from .parser.submission import Submission
from .parser.timus_user import TimusUser
from .message_formers import form_leaderboard_message, form_submission_message

logger = getLogger(__name__)


async def update_group_leaderboard_message(group: GroupModel) -> None:
    if group.leaderboard_message_id is not None:
        try:
            await bot.edit_message_text(
                await form_leaderboard_message(group),
                group.telegram_id,
                group.leaderboard_message_id,
                parse_mode=types.ParseMode.MARKDOWN_V2
            )
            logger.info(f'Updated leaderboard in group with id={group.telegram_id}')
        except ex.MessageError:
            pass


async def update_group_leaderboard(group: GroupModel) -> None:
    """
    Update group tracked users solved problems amount, then update leaderboard message
    :param group:
    :return:
    """
    await group.fetch_related('tracked_users')
    for user in group.tracked_users:
        t = TimusUser(user.timus_id)
        await t.update_profile_data()
        user.username = t.username
        user.solved_problems_amount = t.solved_problems_amount
        await user.save()
    await update_group_leaderboard_message(group)


async def notify_about_submission_verdict(submission: Submission, author_model: TimusUserModel) -> None:
    await author_model.fetch_related('tracked_in')
    for group in author_model.tracked_in:
        await bot.send_message(
            group.telegram_id,
            form_submission_message(submission),
            parse_mode=types.ParseMode.MARKDOWN_V2
        )
        logger.info(f'Notified about submission by "{submission.author.username}" in group with id={group.telegram_id}')
