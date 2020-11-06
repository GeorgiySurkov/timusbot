from aiogram import types
from aiogram.utils import exceptions as ex
from logging import getLogger

from . import dp, bot
from .models import GroupModel, TimusUserModel
from .services.parser.profile_search import search_timus_user
from .services.parser.timus_user import TimusUser
from .services.message_formers import form_leaderboard_message
from .services.command_parser import parse_track_command, parse_untrack_command
from .services import exceptions as exc

logger = getLogger(__name__)


@dp.message_handler(commands=['send_leaderboard'])
async def send_leaderboard(msg: types.Message) -> None:
    group, is_created = await GroupModel.get_or_create(telegram_id=msg.chat.id)
    if group.leaderboard_message_id is not None:
        try:
            await bot.delete_message(msg.chat.id, group.leaderboard_message_id)
        except ex.MessageError:
            pass
    answer = await msg.answer(await form_leaderboard_message(group))
    logger.info(f'Sent leaderboard to group with id={msg.chat.id}, title={msg.chat.title}')
    group.leaderboard_message_id = answer.message_id
    await group.save()


@dp.message_handler(lambda msg: msg.text.startswith('/track_'))
async def track(msg: types.Message) -> None:
    """
    This handler will be called when user sends command `/track12415`
    to track timus user with id 12415
    """
    try:
        timus_user_id = await parse_track_command(msg)
    except exc.TrackCommandParseError:
        return
    group, is_created = await GroupModel.get_or_create(telegram_id=msg.chat.id)
    if is_created:
        await group.save()
    timus_user = TimusUser(timus_user_id)
    try:
        await timus_user.update_profile_data()
    except exc.UserNotFound:
        await msg.answer(f'Автор с id {timus_user_id} не найден')
        return
    timus_user_model, is_created = await TimusUserModel.get_or_create(timus_id=timus_user_id)
    timus_user_model.solved_problems_amount = timus_user.solved_problems_amount
    timus_user_model.username = timus_user.username
    await timus_user_model.save()
    await group.fetch_related('tracked_users')
    if timus_user_model in group.tracked_users:
        await msg.answer(f'{timus_user.username} уже добавлен в список отслеживаемых пользователей.')
        return
    if len(group.tracked_users) == 40:
        await msg.answer(f'Нельзя отслеживать больше 40 пользователей.\n'
                         f'Отвяжите какого-нибудь пользователя, чтобы добавить нового')
        return
    await group.tracked_users.add(timus_user_model)
    logger.info(f'Started tracking user "{timus_user.username}" in group with id={group.telegram_id}')
    await msg.answer(f'Добавил {timus_user.username} к списку отслеживаемых пользователей.')


@dp.message_handler(lambda msg: msg.text.startswith('/untrack_'))
async def untrack(msg: types.Message) -> None:
    try:
        timus_user_id = await parse_untrack_command(msg)
    except exc.UntrackCommandParseError:
        return
    group, is_created = await GroupModel.get_or_create(telegram_id=msg.chat.id)
    if is_created:
        await group.save()
    timus_user = TimusUser(timus_user_id)
    try:
        await timus_user.update_profile_data()
    except exc.UserNotFound:
        await msg.answer(f'Автор с id {timus_user_id} не найден')
        return
    timus_user_model, is_created = await TimusUserModel.get_or_create(timus_id=timus_user_id)
    timus_user_model.solved_problems_amount = timus_user.solved_problems_amount
    timus_user_model.username = timus_user.username
    await group.fetch_related('tracked_users')
    if is_created or timus_user_model not in group.tracked_users:
        await msg.answer(f'{timus_user.username} не отслеживается в этом чате.')
        return
    await group.tracked_users.remove(timus_user_model)
    await timus_user_model.fetch_related('tracked_in')
    if len(timus_user_model.tracked_in) == 0 and not is_created:
        await timus_user_model.delete()
        logger.info(f'Stopped tracking user "{timus_user.username}" in group with id={group.telegram_id}')


@dp.message_handler(commands=['search'])
async def search(msg: types.Message) -> None:
    """
    This handler will be called when user searches timus profiles
    """
    # TODO: add inline keyboard for beautiful search result message
    cmd, username = msg.get_full_command()
    if username == '':
        await msg.answer('Нужно запрос для поиска пользователя\n'
                         'Например <i>/search georgiysurkov</i>', parse_mode=types.ParseMode.HTML)
        return
    search_result = await search_timus_user(username)
    # TODO: use pymorphy2 for right words' forms.
    result_text = 'Результат поиска:\n'
    result_text += str(len(search_result))
    result_text += ' пользователей' if len(search_result) % 10 != 1 else ' пользователь'
    result_text += '\n\n'
    for i, user in enumerate(search_result):
        user_s = f"{i + 1}) {user.username} - решенных задач: {user.solved_problems_amount}\n/track_{user.id}\n"
        if len(result_text) + len(user_s) > 4096:
            break
        result_text += user_s
    logger.info(f'Searched for users in group id={msg.chat.id}, title="{msg.chat.title}"')
    await msg.answer(result_text)


@dp.message_handler(
    lambda msg: any(bot.id == user.id for user in msg.new_chat_members),
    content_types=[types.ContentType.NEW_CHAT_MEMBERS]
)
@dp.message_handler(content_types=[types.ContentType.GROUP_CHAT_CREATED])
async def added_to_group(msg: types.Message) -> None:
    """
    This handler will be called when bot is added to group
    """
    group, is_created = await GroupModel.get_or_create({}, telegram_id=msg.chat.id)
    if is_created:
        await group.save()
    await msg.answer('Привет, я бот для [Тимуса](https://acm.timus.ru/)\.\n'
                     'Я могу вести рейтинг и отслеживать посылки привязанных аккаунтов\.\n'
                     'Чтобы привязать аккаунт напиши _/search \<username\>_\n'
                     'Например _/search georgiysurkov_', parse_mode=types.ParseMode.MARKDOWN_V2)
    logger.info(f'Added to group with id={msg.chat.id}, title="{msg.chat.title}"')


@dp.message_handler()
async def all_messages(msg: types.Message) -> None:
    return
