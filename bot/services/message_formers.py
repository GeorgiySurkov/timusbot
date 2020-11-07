from aiogram.utils.markdown import escape_md

from ..models import GroupModel
from .parser.submission import Submission
from .parser.verdict import Verdict


async def form_leaderboard_message(group: GroupModel) -> str:
    await group.fetch_related('tracked_users')
    text = "Рейтинг по количеству решенных задач:\n"
    for i, user in enumerate(sorted(group.tracked_users, key=lambda user: user.solved_problems_amount, reverse=True)):
        # TODO: write correct form of word using pymorphy2
        text += f'{i + 1}\) {escape_md(user.username)} \- {user.solved_problems_amount} задач\n'
    return text


def form_submission_message(submission: Submission) -> str:
    text = f'Задача {submission.problem.id}\. *{escape_md(submission.problem.name)}*\n'
    text += f'Отправил {escape_md(submission.author.username)}\n'
    text += f'Результат проверки:\n'
    if submission.verdict == Verdict.accepted:
        text += '✅ '
    else:
        text += '❌ '
    text += f'{escape_md(submission.verdict.value)}\n'
    text += f'_Язык:_ {escape_md(submission.language)}\n'
    if submission.test_number is not None:
        text += f'_№ теста:_ {submission.test_number}\n'
    if submission.runtime is not None:
        text += f'_Время работы:_ {escape_md(str(submission.runtime))} с\n'
    if submission.memory is not None:
        text += f'_Выделено памяти:_ {submission.memory} КБ\n'
    return text


async def form_tracked_users_message(group: GroupModel) -> str:
    await group.fetch_related('tracked_users')
    if len(group.tracked_users) == 0:
        return 'В этой группе еще нет отслеживаемых пользователей.'
    text = 'Отслеживаемые пользователи\n\n'
    for i, user in enumerate(group.tracked_users):
        text += f'{i + 1}) {user.username} - /untrack_{user.timus_id}\n'
    text += '\nНажми на команду /untrack_<id> чтобы уперестать отслеживать посылки этого пользователя.'
    return text
