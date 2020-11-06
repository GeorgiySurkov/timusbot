from aiogram import types

from .. import bot
from .exceptions import TrackCommandParseError, UntrackCommandParseError, CommandParseError


async def _base_tracking_command_parser(msg: types.Message) -> int:
    cmd, args = msg.get_full_command()
    if args != '':
        raise CommandParseError('not empty arguments')
    _, timus_user_id = cmd.split('_', maxsplit=1)
    bot_user = await bot.get_me()
    if timus_user_id.endswith(f'@{bot_user.username}'):
        timus_user_id = timus_user_id[:-len(f'@{bot_user.username}')]
    if not timus_user_id.isdecimal():
        raise CommandParseError('id is not int')
    return int(timus_user_id)


async def parse_track_command(msg: types.Message) -> int:
    """
    Parse /track_12124 command
    :param msg: text of the command
    :return: timus user id
    """
    if not msg.text.startswith('/track'):
        raise TrackCommandParseError('Not track command')
    try:
        return await _base_tracking_command_parser(msg)
    except CommandParseError as e:
        raise TrackCommandParseError(str(e))


async def parse_untrack_command(msg: types.Message) -> int:
    """
    Parse /untrack_12124 command
    :param msg: text of the command
    :return: timus user id
    """
    if not msg.text.startswith('/untrack'):
        raise TrackCommandParseError('Not untrack command')
    try:
        return await _base_tracking_command_parser(msg)
    except CommandParseError as e:
        raise UntrackCommandParseError(str(e))
