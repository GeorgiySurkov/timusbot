from aiogram import types

from . import dp
from .parser.profile_search import search_timus_user


@dp.message_handler(commands=['search'])
async def search(msg: types.Message) -> None:
    """
    This handler is called when user searches timus profiles
    """
    cmd, username = msg.get_full_command()
    if username == '':
        await msg.answer('Нужно запрос для поиска пользователя\n'
                         'Например <i>/search georgiysurkov</i>', parse_mode=types.ParseMode.HTML)
        return
    search_result = await search_timus_user(username)
    result_text = 'Результат поиска:\n'
    result_text += str(len(search_result))
    result_text += ' пользователей' if len(search_result) % 10 != 1 else ' пользователь'
    result_text += '\n\n'
    for i, user in enumerate(search_result):
        result_text += f"{i + 1}) {user.username} - решенных задач: {user.solved_problems_amount}\n/track{user.id}\n"
    await msg.answer(result_text)
