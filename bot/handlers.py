from aiogram import types

from . import dp, bot
from .models import Group, TimusUser
from .parser.profile_search import search_timus_user


@dp.message_handler(lambda msg: msg.text.startswith('/track_'))
async def track(msg: types.Message) -> None:
    """
    This handler will be called when user sends command `/track12415`
    to track timus user with id 12415
    """
    cmd, args = msg.get_full_command()
    if args != '':
        return
    _, timus_user_id = cmd.split('_', maxsplit=1)
    bot_user = await bot.get_me()
    if timus_user_id.endswith(f'@{bot_user.username}'):
        timus_user_id = timus_user_id[:-len(f'@{bot_user.username}')]
    if not timus_user_id.isdecimal():
        return
    timus_user_id = int(timus_user_id)
    group, is_created = await Group.get_or_create({}, telegram_id=msg.chat.id)
    if is_created:
        await group.save()
    timus_user, is_created = await TimusUser.get_or_create({}, timus_id=timus_user_id)
    if is_created:
        await timus_user.save()
    await group.tracked_users.add(timus_user)


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
    group, is_created = await Group.get_or_create({}, telegram_id=msg.chat.id)
    if is_created:
        await group.save()
    await msg.answer('Привет, я бот для [Тимуса](https://acm.timus.ru/)\.\n'
                     'Я могу вести рейтинг и отслеживать посылки привязанных аккаунтов\.\n'
                     'Чтобы привязать аккаунт напиши _/search \<username\>_\n'
                     'Например _/search georgiysurkov_', parse_mode=types.ParseMode.MARKDOWN_V2)


@dp.message_handler()
async def all_messages(msg: types.Message) -> None:
    return
