from aiogram import types

from .. import bot
from ..models import GroupModel
from .message_formers import form_leaderboard_message


async def update_group_leaderboard(group: GroupModel) -> None:
    if group.leaderboard_message_id is not None:
        await bot.send_message(
            group.telegram_id,
            await form_leaderboard_message(group),
            parse_mode=types.ParseMode.MARKDOWN_V2
        )
